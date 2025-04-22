import random

import aiohttp

pexels_api_key = '1flAeLrtSoQxHwykmOftkfvVVJ3aD6d58AooSseIGzFPhD3aPS8Z4ak8'

async def get_random_image(query: str):
    url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': pexels_api_key
    }
    params = {
        'query': query,
        'per_page': 1,
        'page': random.randint(1, 100)
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data['photos']:
                    return data['photos'][0]['src']['medium']
                else:
                    return None
            else:
                return None

async def get_random_fox_image():
    url = 'https://randomfox.ca/floof/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['image']
            else:
                return None

async def get_goose_image(x):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://nekos.life/api/v2/img/{x}') as response:
            if response.status == 200:
                data = await response.json()
                return data['url']
            else:
                return None
