import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import hikari
import lightbulb
import miru

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from utils.check_all_hooks import check_info_view, check_ticket_view
from utils.localization_provider import localization_provider

config_manager = ConfigManager()
bot = hikari.GatewayBot(
    intents=hikari.Intents.ALL,
    token=config_manager.get_config_value("BOT_TOKEN")
    )
client = lightbulb.client_from_app(bot, localization_provider=localization_provider)

bot.subscribe(hikari.StartingEvent, client.start)

registry = client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
registry.register_factory(miru.Client, lambda: miru.Client(bot))

log_dir = 'other/logs'
os.makedirs(log_dir, exist_ok=True)

log_format = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s'

log_file = os.path.join(log_dir, 'logging.log')
handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@bot.listen(hikari.StartedEvent)
async def start_views(event: hikari.StartedEvent) -> None:
    database_manager = DatabaseManager()
    await database_manager.init_db()
    await check_info_view(client, miru.Client(bot))
    await check_ticket_view(client, miru.Client(bot))

async def main():
    await client.load_extensions("cogs.fun.cutie", "cogs.fun.emotions", "cogs.fun.neko", "cogs.user.top_bumps", "cogs.user.top_messages", "cogs.user.top_voice", "cogs.user.user_profile", "cogs.user.private_voice", "cogs.utils.tech", "cogs.utils.information",  "cogs.events.logging", "cogs.fun.nuclear",)


if __name__ == '__main__':
    asyncio.run(main())
    bot.subscribe(hikari.StartingEvent, client.start)
    bot.run(
        asyncio_debug=True,
        coroutine_tracking_depth=True,
    )
