import logging
import os
from logging.handlers import TimedRotatingFileHandler

import arc
import hikari
import miru

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from utils.check_all_hooks import check_info_view, check_ticket_view
from utils.localization_provider import COMMAND_LOCALES, OPTION_LOCALES

config = ConfigManager()
db = DatabaseManager()

bot = hikari.GatewayBot(
    intents=hikari.Intents.ALL,
    token=config.get_config_value("BOT_TOKEN")
    )

arc_client = arc.GatewayClient(
    bot,
    provided_locales=[hikari.Locale.EN_US, hikari.Locale.RU, hikari.Locale.UK]
    )

arc_client.set_type_dependency(ConfigManager, config)
arc_client.set_type_dependency(DatabaseManager, db)

log_dir = "other/logs"
os.makedirs(log_dir, exist_ok=True)

log_format = "%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s"  # noqa: E501
log_file = os.path.join(log_dir, "logging.log")

handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@arc_client.set_command_locale_provider
def command_locale_provider(req: arc.CommandLocaleRequest) -> arc.LocaleResponse:
    return COMMAND_LOCALES[" ".join(req.qualified_name)][req.locale]


@arc_client.set_option_locale_provider
def option_locale_provider(req: arc.OptionLocaleRequest) -> arc.LocaleResponse:
    return OPTION_LOCALES[" ".join(req.qualified_name)][req.option.name][req.locale]


# — Miru
miru_client = miru.Client.from_arc(arc_client)

@arc_client.listen()
async def on_started(_: hikari.StartedEvent) -> None:
    try:
        await db.init_db()
        logger.info("Database initialized successfully")

        await check_info_view(arc_client, miru_client)
        logger.info("Info view checked successfully")

        await check_ticket_view(arc_client, miru_client)
        logger.info("Ticket view checked successfully")
    except Exception as e:
        logger.error(f"Error in on_started: {e}", exc_info=True)

if __name__ == '__main__':
    arc_client.load_extensions_from("cogs")
    bot.run(
        asyncio_debug=True,
        coroutine_tracking_depth=True,
    )
