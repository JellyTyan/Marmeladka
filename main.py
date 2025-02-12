import asyncio
import hikari
import lightbulb
import miru

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from utils.check_all_hooks import check_info_view, check_ticket_view

config_manager = ConfigManager()
bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=config_manager.get_config_value("BOT_TOKEN"))
client = lightbulb.client_from_app(bot)

bot.subscribe(hikari.StartingEvent, client.start)

registry = client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
registry.register_factory(miru.Client, lambda: miru.Client(bot))

@bot.listen(hikari.StartedEvent)
async def start_views(event: hikari.StartedEvent) -> None:
    await check_info_view(client, miru.Client(bot))
    await check_ticket_view(client, miru.Client(bot))

async def main():
    database_manager = DatabaseManager()
    await database_manager.init_db()

    await client.load_extensions("cogs.fun.cutie", "cogs.fun.emotions", "cogs.fun.neko", "cogs.user.top_bumps", "cogs.user.top_messages", "cogs.user.top_voice", "cogs.user.user_profile", "cogs.utils.tech", "cogs.utils.information", "cogs.events.logging", "cogs.fun.nuclear")


if __name__ == '__main__':
    asyncio.run(main())
    bot.subscribe(hikari.StartingEvent, client.start)
    bot.run(
        asyncio_debug=True,
        coroutine_tracking_depth=True,
    )
