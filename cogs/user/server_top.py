import logging
import re

import arc
import hikari
import pendulum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.database_manager import DatabaseManager
from database.models import UserData
from functions.top_func import (
    format_duration,
    update_bump_count,
    update_message_count,
    update_voice_time,
)

database_manager = DatabaseManager()

plugin = arc.GatewayPlugin("TopBumps", invocation_contexts=[hikari.ApplicationContextType.GUILD])
top = plugin.include_slash_group("top", "Server Tops", autodefer=arc.AutodeferMode.ON)

logger = logging.getLogger(__name__)

voice_start_times = {}
voice_channel_users = {}

@top.include
@arc.slash_subcommand("bumps", "Top users by bump.")
async def topbumps_command(ctx: arc.GatewayContext) -> None:
    session = async_sessionmaker(database_manager.engine, expire_on_commit=False)
    async with session() as session:
        stmt = select(UserData).order_by(UserData.bump_count.desc()).limit(10)
        top_users_list = await session.scalars(stmt)
        await session.aclose()

    title = "**Top 10 users by number of bumps on the server:**\n\n"

    guild = ctx.get_guild()
    if guild is None:
        return

    for index, user in enumerate(top_users_list, start=1):
        if user.bump_count == 0:
            continue

        member = guild.get_member(user.user_id)
        if member is not None:
            user_ping = member.mention
        else:
            user_ping = f"<@{user.user_id}>"

        title += f"{index}. {user_ping} - {user.bump_count} bumps\n"
    embed = hikari.Embed(description=title, color=0x2B2D31)

    await ctx.respond(embed=embed)


@top.include
@arc.slash_subcommand("messages", "Top users by messages.")
async def topmessages_command(ctx: arc.GatewayContext) -> None:
    session = async_sessionmaker(database_manager.engine, expire_on_commit=False)
    async with session() as session:
        stmt = select(UserData).order_by(UserData.message_count.desc()).limit(10)
        top_users_list = await session.scalars(stmt)
        await session.aclose()

    title = "**Top 10 users by number of messages on the server:**\n\n"

    guild = ctx.get_guild()
    if guild is None:
        return

    for index, user in enumerate(top_users_list, start=1):
        if user.message_count == 0:
            continue

        member = guild.get_member(user.user_id)
        if member is not None:
            user_ping = member.mention
        else:
            user_ping = f"<@{user.user_id}>"
        title += f"{index}. `{user.message_count} messages` - {user_ping}\n"
    embed = hikari.Embed(description=title, color=0x2b2d31)

    await ctx.respond(embed=embed)

@top.include
@arc.slash_subcommand("voice", "Top users by length of time in voice channel.")
async def topvoice_command(ctx: arc.GatewayContext) -> None:
    session = async_sessionmaker(database_manager.engine, expire_on_commit=False)
    async with session() as session:
        stmt = select(UserData).order_by(UserData.voice_time.desc()).limit(10)
        top_users_list = await session.scalars(stmt)
        await session.aclose()

    title = "**Top 10 users by voice acitivity:**\n\n"

    guild_id = ctx.guild_id
    if guild_id is None:
        return

    guild = await ctx.client.rest.fetch_guild(guild_id)
    if guild is None:
        return

    for index, user in enumerate(top_users_list, start=1):
        if user.voice_time == 0:
            continue

        voice_time = format_duration(user.voice_time)
        member = guild.get_member(user.user_id)
        if member is not None:
            user_ping = member.mention
        else:
            user_ping = f"<@{user.user_id}>"
        title += f"{index}. `{voice_time}` - {user_ping}\n"
    embed = hikari.Embed(description=title, color=0x2B2D31)
    await ctx.respond(embed=embed)


@plugin.listen(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    # -> Message Count
    if not event.message.attachments:
        if not event.author.is_bot:
            channel = await event.app.rest.fetch_channel(event.channel_id)
            if channel is None:
                return
            if not isinstance(channel, hikari.GuildTextChannel):
                return

            await update_message_count(event.author.id, event.author.username)
    # -> Message Bumps
    try:
        if event.author.is_bot:
            embed = event.embeds[0]

            if embed.description and "Reaction time" in embed.description:
                if embed.author is None:
                    return
                user_name = embed.author.name

                guild = event.get_guild()
                if guild is None:
                    return

                members = guild.get_members()

                user = None

                for member in members:
                    member = guild.get_member(member)
                    if member is None:
                        continue
                    if member.username == user_name:
                        user = member
                        break

                if user is None or user_name is None:
                    return

                await update_bump_count(user.id, user_name)

                session = async_sessionmaker(database_manager.engine, expire_on_commit=True)
                async with session() as session:
                    async with session.begin():
                        stmt = select(UserData.bump_count).where(UserData.user_id == user.id)
                        bump_count = await session.scalar(stmt)

                embed_success = hikari.Embed(
                    description=f"Hey, {user.mention}, thank u!\n Your total bumps: `{bump_count}`",
                    color=0x2B2D31,
                )
                channel = event.get_channel()
                if isinstance(channel, hikari.GuildTextChannel):
                    await channel.send(embed=embed_success)

    except Exception as e:
        logger.error(e)
        pass


@plugin.listen(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    before = event.old_state
    after = event.state
    member = event.state.member

    if member is None:
        return

    if member.is_bot:
        return

    guild = await event.app.rest.fetch_guild(event.guild_id)
    if guild is None:
        return

    # Пользователь присоединился к каналу
    if before is None and after is not None:
        channel_id = after.channel_id
        if channel_id not in voice_channel_users:
            voice_channel_users[channel_id] = set()
        voice_channel_users[channel_id].add(member.id)

        # Начинаем отсчет только если в канале больше одного пользователя
        if len(voice_channel_users[channel_id]) > 1:
            if member.id not in voice_start_times:
                voice_start_times[member.id] = pendulum.now("Europe/Warsaw")
            # Запускаем отсчет для всех остальных в канале, если они еще не начали
            for user_id in voice_channel_users[channel_id]:
                if user_id != member.id and user_id not in voice_start_times:
                    voice_start_times[user_id] = pendulum.now("Europe/Warsaw")

    # Пользователь покинул канал
    elif before is not None and after.channel_id is None:
        old_channel_id = before.channel_id
        if old_channel_id in voice_channel_users:
            voice_channel_users[old_channel_id].discard(member.id)

            # Сохраняем время если пользователь был в отсчете
            if member.id in voice_start_times:
                duration = (pendulum.now("Europe/Warsaw") - voice_start_times[member.id]).total_seconds()
                duration = round(duration)
                await update_voice_time(member.id, member.username, duration)
                del voice_start_times[member.id]

            # Останавливаем отсчет для остальных если в канале остался только один человек
            if len(voice_channel_users[old_channel_id]) == 1:
                remaining_user = next(iter(voice_channel_users[old_channel_id]))
                if remaining_user in voice_start_times:
                    duration = (pendulum.now("Europe/Warsaw") - voice_start_times[remaining_user]).total_seconds()
                    duration = round(duration)
                    remaining_member = event.app.rest.fetch_member(event.guild_id, remaining_user)
                    if not isinstance(remaining_member, hikari.Member):
                        return
                    if remaining_member:
                        await update_voice_time(remaining_user, remaining_member.username, duration)
                    del voice_start_times[remaining_user]

            # Удаляем канал из отслеживания если он пустой
            if len(voice_channel_users[old_channel_id]) == 0:
                del voice_channel_users[old_channel_id]

    # Пользователь переключился между каналами
    elif before is not None and after is not None and before.channel_id != after.channel_id:
        old_channel_id = before.channel_id
        new_channel_id = after.channel_id

        # Обработка старого канала
        if old_channel_id in voice_channel_users:
            voice_channel_users[old_channel_id].discard(member.id)

            if member.id in voice_start_times:
                duration = (pendulum.now("Europe/Warsaw") - voice_start_times[member.id]).total_seconds()
                duration = round(duration)
                await update_voice_time(member.id, member.username, duration)
                del voice_start_times[member.id]

            if len(voice_channel_users[old_channel_id]) == 1:
                remaining_user = next(iter(voice_channel_users[old_channel_id]))
                if remaining_user in voice_start_times:
                    duration = (pendulum.now("Europe/Warsaw") - voice_start_times[remaining_user]).total_seconds()
                    duration = round(duration)
                    remaining_member = event.app.rest.fetch_member(event.guild_id, remaining_user)
                    if not isinstance(remaining_member, hikari.Member):
                        return
                    if remaining_member:
                        await update_voice_time(remaining_user, remaining_member.username, duration)
                    del voice_start_times[remaining_user]

            if len(voice_channel_users[old_channel_id]) == 0:
                del voice_channel_users[old_channel_id]

        # Обработка нового канала
        if new_channel_id not in voice_channel_users:
            voice_channel_users[new_channel_id] = set()
        voice_channel_users[new_channel_id].add(member.id)

        if len(voice_channel_users[new_channel_id]) > 1:
            if member.id not in voice_start_times:
                voice_start_times[member.id] = pendulum.now("Europe/Warsaw")
            for user_id in voice_channel_users[new_channel_id]:
                if user_id != member.id and user_id not in voice_start_times:
                    voice_start_times[user_id] = pendulum.now("Europe/Warsaw")


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
