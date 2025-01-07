import asyncio
import hikari
import lightbulb
import miru

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from utils.check_all_hooks import check_info_view, check_ticket_view

config_manager = ConfigManager()
bot = lightbulb.BotApp(intents=hikari.Intents.ALL, token=config_manager.get_config_value("BOT_TOKEN"), prefix="!")

bot.d.miru = miru.Client(bot)

@bot.listen()
async def start_views(event: hikari.StartedEvent) -> None:
    await check_info_view(bot)
    await check_ticket_view(bot)

async def main():
    database_manager = DatabaseManager()
    await database_manager.create_table(
        "user_data",
        """
        id INTEGER PRIMARY KEY,
        username TEXT,
        message_count INTEGER DEFAULT 0,
        invite_count INTEGER DEFAULT 0,
        voice_time INTEGER DEFAULT 0,
        bump_count INTEGER DEFAULT 0,
        tag TEXT,
        biography TEXT,
        birthday_date TEXT
        """
    )

    await database_manager.create_table(
        "nuclear_data",
        """
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        new_user INTEGER DEFAULT 1,
        nuclear_mode INTEGER DEFAULT 0,
        bomb_start_count INTEGER DEFAULT 0,
        mivina_start_count INTEGER DEFAULT 0,
        bomb_cd TEXT DEFAULT 0,
        mivina_cd TEXT DEFAULT 0
        """
    )
    await database_manager.create_table(
        "bomb_logs",
        """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        date TEXT DEFAULT 0,
        used BOOLEAN DEFAULT 0
        """
    )
    await database_manager.create_table(
        "mivina_logs",
        """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        date TEXT DEFAULT 0,
        used BOOLEAN DEFAULT 0
        """
    )

if __name__ == '__main__':
    asyncio.run(main())
    bot.load_extensions_from("./cogs/fun")
    bot.load_extensions_from("./cogs/utils")
    bot.load_extensions_from("./cogs/events")
    bot.load_extensions_from("./cogs/user")
    bot.load_extensions_from("./cogs/notifications")
    bot.run(
        asyncio_debug=True,
        coroutine_tracking_depth=True,
    )
