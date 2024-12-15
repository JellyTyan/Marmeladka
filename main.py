import hikari
import lightbulb

from config.config_manager import ConfigManager

config_manager = ConfigManager()
bot = lightbulb.BotApp(intents=hikari.Intents.ALL, token=config_manager.get_config_value("BOT_TOKEN"), prefix="!")


if __name__ == '__main__':
    bot.load_extensions_from("./cogs/fun")
    bot.load_extensions_from("./cogs/utils")
    bot.run(
        asyncio_debug=True,
        coroutine_tracking_depth=True,
    )
