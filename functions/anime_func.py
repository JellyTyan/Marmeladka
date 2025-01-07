import aiohttp
from config.config_manager import ConfigManager

config_manager = ConfigManager()

async def get_anime_image(x):
    token = config_manager.get_config_value("WAIFU_TOKEN")
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://waifu.it/api/v4/{x}', headers={"Authorization": token}) as response:
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
