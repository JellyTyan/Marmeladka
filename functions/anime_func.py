import aiohttp

async def get_anime_image(x):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://nekos.life/api/v2/img/{x}') as response:
            if response.status == 200:
                data = await response.json()
                return data['url']
            else:
                return None

async def get_waifu_image():
    url = 'https://api.waifu.im/search'
    params = {
        # 'included_tags': ['raiden-shogun', 'maid'],
        'height': '>=2000'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data['images'][0]['url']
            else:
                return None
