import asyncio
from datetime import datetime, timedelta

import hikari
import lightbulb
import pendulum

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager

plugin = lightbulb.Plugin("BirthdayNotification")

class BirthdayNotification:
    def __init__(self, bot: lightbulb.BotApp):
        self.bot = bot
        self.config_manager = ConfigManager()
        self.database_manager = DatabaseManager()
        self.post_check_task = bot.create_task(self.schedule_birth_check())

    async def birth_check(self):
        rows = await self.database_manager.fetchall("SELECT id, birthday_date FROM user_data")

        for row in rows:
            try:
                user_id, birthday_date = row
                today = pendulum.now().strftime("%m-%d")
                if today == birthday_date:
                    birthday_channel_id = self.config_manager.get_config_value("BIRTHDAY_CHANNEL_ID")
                    message = f"У <@{user_id}> сегодня день рождения! Поздравляем! https://cdn.discordapp.com/attachments/1108629194788847637/1265283297827881012/Happy_Birthday.mp4?ex=66a0f266&is=669fa0e6&hm=0b568445807e5efce7ff5e22b77fb58951f973c3dcff443012e89f7be3d0cac5&"
                    await self.bot.rest.create_message(int(birthday_channel_id), message, user_mentions=True)
            except Exception as e:
                print(e)
                continue

    async def schedule_birth_check(self):
        while True:
            try:
                now = datetime.now()
                target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)

                if now >= target_time:
                    target_time += timedelta(days=1)

                delta = target_time - now
                await asyncio.sleep(delta.total_seconds())

                await self.birth_check()
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(300)


@plugin.listener(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    global birthday_notification
    birthday_notification = BirthdayNotification(plugin.bot)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
