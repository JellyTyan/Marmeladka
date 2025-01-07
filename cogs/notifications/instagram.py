import asyncio
import json
import os
from datetime import datetime, timedelta

import aiohttp
import hikari
import lightbulb

from config.config_manager import ConfigManager
from utils.create_embed import create_embed

plugin = lightbulb.Plugin("InstagramNotification")

class InstagramNotification:
    def __init__(self, bot: lightbulb.BotApp):
        self.bot = bot
        self.config_manager = ConfigManager()
        self.json_file = "last_post_id.json"
        self.post_check_task = bot.create_task(self.schedule_post_check())

    async def post_check(self):
        INSTAGRAM_API_URL = "https://instagram-scraper-api2.p.rapidapi.com/v1/highlight_info"
        INSTAGRAM_API_HEADERS = {
            "X-RapidAPI-Key": self.config_manager.get_config_value("X-RapidAPI-Key"),
            "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(INSTAGRAM_API_URL, headers=INSTAGRAM_API_HEADERS) as response:
                    if response.status != 200:
                        raise Exception(f"API request failed with status {response.status}")
                    last_post_json = await response.json()

            post_data = last_post_json['data']['items'][0]
            last_post_shortcode = str(post_data['code'])
            photo_url = str(post_data['image_versions']['items'][0]['url'])

            news_channel_id = int(self.config_manager.get_config_value("NEWS_CHANNEL_ID"))
            insta_notif_role_id = self.config_manager.get_config_value("INSTAGRAM_ROLE_ID")

            old_post_id = self._read_last_post_id()
            if last_post_shortcode == old_post_id:
                return

            embed = create_embed(
                title=f"Желешка сделал новый пост в Инстаграм\n https://www.instagram.com/p/{last_post_shortcode}/",
                image_url=photo_url
            )

            await self.bot.rest.create_message(news_channel_id, content=f"<@&{insta_notif_role_id}>", embed=embed, role_mentions=True)

            self._save_last_post_id(last_post_shortcode)

        except Exception as e:
            print(f"Error in post_check: {e}")

    def _read_last_post_id(self) -> str:
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                data = json.load(file)
                return data.get("last_post_id", "")
        return ""

    def _save_last_post_id(self, post_id: str) -> None:
        with open(self.json_file, "w") as file:
            json.dump({"last_post_id": post_id}, file)

    async def schedule_post_check(self):
        while True:
            try:
                now = datetime.now()
                target_time = now.replace(hour=18, minute=0, second=0, microsecond=0)

                if now >= target_time:
                    target_time += timedelta(days=1)

                delta = target_time - now
                await asyncio.sleep(delta.total_seconds())

                await self.post_check()
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(300)


@plugin.listener(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    global instagram_notification
    instagram_notification = InstagramNotification(plugin.bot)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
