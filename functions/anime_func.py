import aiohttp
from config.config_manager import ConfigManager

config_manager = ConfigManager()

async def get_nekos_gif(x):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://nekos.best/api/v2/{x}') as response:
            if response.status == 200:
                data = await response.json()
                return data["results"][0]["url"]
            else:
                return None

async def get_waifu_gif(x):
    print(x)
    token = config_manager.get_config_value("WAIFU_TOKEN")
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://waifu.it/api/v4/{x}', headers={"Authorization": token}) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data["url"]
            else:
                print(response.status)
                return None
