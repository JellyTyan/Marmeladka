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

bot = hikari.GatewayBot(
    intents=hikari.Intents.ALL,
    token=config.get_config_value("BOT_TOKEN")
    )

arc_client = arc.GatewayClient(
    bot,
    provided_locales=[hikari.Locale.EN_US, hikari.Locale.RU, hikari.Locale.UK]
    )

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
    db = DatabaseManager()
    await db.init_db()

    await check_info_view(arc_client, miru_client)
    await check_ticket_view(arc_client, miru_client)

if __name__ == '__main__':
    arc_client.load_extensions_from("cogs")
    bot.run(
        asyncio_debug=True,
        coroutine_tracking_depth=True,
    )
