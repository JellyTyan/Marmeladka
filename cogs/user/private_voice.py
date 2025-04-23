import arc
import hikari
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.init import db
from database.models import GuildConfig
from utils.guild import get_channels_in_category, get_guild_categories

plugin = arc.GatewayPlugin("PrivateVoice", invocation_contexts=(hikari.ApplicationContextType(0), ))

private_channels = {}
create_channels_ids = {}

@plugin.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    async with async_sessionmaker(db.engine)() as session:
        result = await session.execute(select(GuildConfig))
        configs = result.scalars().all()

        for config in configs:
            if config.private_voice_id:
                create_channels_ids[config.guild_id] = config.private_voice_id

@plugin.include
# @arc.with_hook(arc.channel_limiter(10.0, 1))
@arc.with_hook(arc.bot_has_permissions(hikari.Permissions.MANAGE_CHANNELS))
@arc.slash_command(
    "setup-private-voice",
    "Setup private voice channels",
    default_permissions=hikari.Permissions.MANAGE_GUILD,
    autodefer=arc.AutodeferMode.EPHEMERAL,
    invocation_contexts=[hikari.ApplicationContextType.GUILD]
)
async def setup_voice_command(ctx: arc.GatewayContext) -> None:
    guild = ctx.get_guild()
    if not guild:
        return

    private_category = await get_or_create_private_category(ctx, guild)
    create_channel = await get_or_create_create_voice_channel(ctx, guild, private_category)

    create_channels_ids[guild.id] = create_channel.id

    await save_config_to_db(
        guild_id=guild.id,
        guild_name=guild.name,
        category_id=private_category.id,
        create_channel_id=create_channel.id,
    )

    await ctx.respond(
        f"✅ Приватные голосовые каналы настроены!\n"
        f"Категория: <#{private_category.id}>\n"
        f"Канал создания: <#{create_channel.id}>"
    )


async def get_or_create_private_category(ctx: arc.GatewayContext, guild: hikari.Guild) -> hikari.GuildCategory:
    categories = [
        ch for ch in await ctx.client.rest.fetch_guild_channels(guild.id)
        if isinstance(ch, hikari.GuildCategory) and "private" in ch.name.lower()
    ]

    if categories:
        return categories[0]

    return await ctx.client.rest.create_guild_category(guild.id, "Private Channels")


async def get_or_create_create_voice_channel(ctx: arc.GatewayContext, guild: hikari.Guild, category: hikari.GuildCategory) -> hikari.GuildVoiceChannel:
    channels = [
        ch for ch in await ctx.client.rest.fetch_guild_channels(guild.id)
        if isinstance(ch, hikari.GuildVoiceChannel) and ch.parent_id == category.id and "create" in ch.name.lower()
    ]

    if channels:
        return channels[0]

    return await ctx.client.rest.create_guild_voice_channel(guild.id, "Join to Create", category=category)


async def save_config_to_db(guild_id: int, guild_name: str, category_id: int, create_channel_id: int) -> None:
    session = async_sessionmaker(db.engine, expire_on_commit=True)
    async with session() as session:
        stmt = insert(GuildConfig).values(
            guild_id=guild_id,
            guild_name=guild_name,
            private_category_id=category_id,
            private_voice_id=create_channel_id,
        ).on_conflict_do_update(
            index_elements=["guild_id"],
            set_={
                "private_category_id": category_id,
                "private_voice_id": create_channel_id,
            }
        )
        await session.execute(stmt)
        await session.commit()


@setup_voice_command.set_error_handler
async def voice_error_handler(
    ctx: arc.GatewayContext, error: Exception
) -> None:
    if isinstance(error, arc.UnderCooldownError):
        await ctx.respond(
            "Command is on cooldown!"
            f"\nTry again in `{error.retry_after}` seconds."
        )
    elif isinstance(error, hikari.ForbiddenError):
        await ctx.respond("❌ Не удалось создать канал. Убедись, что у меня есть права.", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        raise error


@plugin.listen(hikari.VoiceStateUpdateEvent)
async def voice_event(event: hikari.VoiceStateUpdateEvent):
    guild_id = event.guild_id
    new_channel = event.state.channel_id
    old_channel = event.old_state.channel_id if event.old_state else None

    if guild_id not in create_channels_ids:
        return

    async with async_sessionmaker(db.engine)() as session:
        config = await session.get(GuildConfig, guild_id)

    if not config or not config.private_category_id:
        return

    if new_channel == create_channels_ids[guild_id]:
        await handle_join_trigger_channel(event, config)
    elif old_channel and old_channel in private_channels.values():
        await handle_leave_private_channel(event, old_channel)


async def handle_join_trigger_channel(event: hikari.VoiceStateUpdateEvent, config: GuildConfig):
    user_id = event.state.user_id
    guild_id = event.guild_id

    if user_id in private_channels:
        await plugin.client.rest.edit_member(
            guild_id,
            user_id,
            voice_channel=private_channels[user_id],
            reason="Перемещение в уже созданный канал"
        )
        return

    member = event.state.member
    display_name = member.nickname or member.username if member is not None else "Unknown"

    try:
        category = await plugin.client.rest.fetch_channel(config.private_category_id)
    except hikari.NotFoundError:
        return

    try:
        new_voice = await plugin.client.rest.create_guild_voice_channel(
            guild_id,
            name=f"{display_name}'s Room",
            category=category.id,
            reason="Создание приватного голосового канала"
        )
    except hikari.ForbiddenError:
        await plugin.client.rest.edit_member(
            guild_id,
            user_id,
            voice_channel=None,
            reason="Не удалось создать приватный канал"
        )
        return

    await plugin.client.rest.edit_permission_overwrite(
        channel=new_voice.id,
        target=event.state.member.id,
        target_type=hikari.PermissionOverwriteType.MEMBER,
        allow=hikari.Permissions.MANAGE_CHANNELS,
        reason="Выдача прав владельцу канала"
    )

    private_channels[user_id] = new_voice.id

    await plugin.client.rest.edit_member(
        guild_id,
        user_id,
        voice_channel=new_voice.id,
        reason="Перемещение в новый приватный канал"
    )


async def handle_leave_private_channel(event: hikari.VoiceStateUpdateEvent, old_channel_id: int):
    owner_id = next((uid for uid, cid in private_channels.items() if cid == old_channel_id), None)
    if not owner_id:
        return

    try:
        voice_states = plugin.client.cache.get_voice_states_view_for_guild(event.guild_id)
    except Exception:
        return

    members_in_channel = [
        state for state in voice_states.values()
        if state.channel_id == old_channel_id
    ]

    if not members_in_channel:
        try:
            await plugin.client.rest.delete_channel(old_channel_id, reason="Приватный канал пуст")
        except hikari.ForbiddenError:
            pass

@plugin.listen(hikari.GuildChannelDeleteEvent)
async def voice_channel_delete(event: hikari.GuildChannelDeleteEvent):
    channel_id = event.channel_id
    if channel_id in private_channels.values():
        user_id = next(uid for uid, cid in private_channels.items() if cid == channel_id)
        del private_channels[user_id]

@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
