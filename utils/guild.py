from typing import Union

import hikari


async def get_guild_categories(bot: hikari.RESTAware, guild_id: int) -> list[hikari.GuildCategory]:
    channels = await bot.rest.fetch_guild_channels(guild_id)
    return [ch for ch in channels if isinstance(ch, hikari.GuildCategory)]

async def get_channels_in_category(
    bot: hikari.RESTAware,
    guild_id: int,
    category_id: Union[int, hikari.Snowflake]
) -> list[hikari.GuildChannel]:
    channels = await bot.rest.fetch_guild_channels(guild_id)
    return [ch for ch in channels if ch.parent_id == category_id]
