from typing import Union

import hikari


async def get_guild_categories(cache: hikari.api.Cache, guild_id: int) -> list[hikari.GuildCategory]:
    channels = cache.get_guild_channels_view_for_guild(guild_id)
    return [ch for ch in channels if isinstance(ch, hikari.GuildCategory)]

async def get_channels_in_category(
    cache: hikari.api.Cache,
    guild_id: int,
    category_id: Union[int, hikari.Snowflake]
) -> list[hikari.GuildChannel]:
    channels = cache.get_guild_channels_view_for_guild(guild_id).values()
    return [ch for ch in channels if ch.parent_id == category_id]
