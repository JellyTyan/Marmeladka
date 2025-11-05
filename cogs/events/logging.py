import typing

import arc
import hikari
import pendulum

from config.config_manager import ConfigManager

plugin = arc.GatewayPlugin("Logger")

# <--------------------------------------------------### Message Events

@plugin.listen(hikari.GuildMessageDeleteEvent)
async def on_message_delete(event: hikari.GuildMessageDeleteEvent) -> None:
    deleted_message = event.old_message
    if deleted_message:
        if deleted_message.author.is_bot:
            return

        log_channel = get_log_channel()

        if isinstance(log_channel, hikari.GuildTextChannel):
            embed = hikari.Embed(
                title="Delete message",
                color=0xFF0000,
                description=f"**Message:**\n ```{deleted_message.content}```",
                timestamp=pendulum.now("Europe/Warsaw")
                )

            event_channel = await deleted_message.fetch_channel()

            if isinstance(event_channel, hikari.GuildTextChannel):
                embed.add_field(name="Channel", value=event_channel.mention)
                embed.add_field(name="Author", value=deleted_message.author.mention)

                if deleted_message.attachments:
                    if deleted_message.attachments:
                        embed.set_image(deleted_message.attachments[0].url)

                await log_channel.send(embed=embed)


@plugin.listen(hikari.GuildMessageUpdateEvent)
async def on_message_edit(event: hikari.GuildMessageUpdateEvent) -> None:
    old_message = event.old_message
    new_message = event.message

    if old_message and new_message:
        if not old_message.author:
            return

        if old_message.author.is_bot:
            return

        if old_message.content == new_message.content:
            return

        log_channel = get_log_channel()

        if isinstance(log_channel, hikari.GuildTextChannel):
            embed = hikari.Embed(
                title="Edit message",
                description=f"""**Original:**\n ```{old_message.content}```\n **Edited:**\n ```{new_message.content}```""",  # noqa: E501
                color=0x0062FF,
                timestamp=pendulum.now("Europe/Warsaw")
                )

            event_channel = await old_message.fetch_channel()

            if isinstance(event_channel, hikari.GuildTextChannel):

                embed.add_field(name="Channel", value=event_channel.mention)
                embed.add_field(name="Author", value=old_message.author.mention)

                await log_channel.send(embed=embed)

# <--------------------------------------------------### Member events

@plugin.listen(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    member = event.member

    if member.is_bot:
        return

    if member:
        log_channel = get_log_channel()

        if isinstance(log_channel, hikari.GuildTextChannel):
            embed = hikari.Embed(
                title="User joined to the server",
                color=0x0000FF,
                timestamp=pendulum.now("Europe/Warsaw")
                )

            embed.set_author(name=member.display_name, icon=member.make_avatar_url())
            embed.add_field(name="User", value=member.mention)
            embed.add_field(name="Username", value=f"{member.display_name}:{member.nickname}")

            await log_channel.send(embed=embed)

@plugin.listen(hikari.MemberDeleteEvent)
async def on_member_leave(event: hikari.MemberDeleteEvent) -> None:
    member = event.old_member

    if member is None:
        return

    if member.is_bot:
        return

    log_channel = get_log_channel()

    if isinstance(log_channel, hikari.GuildTextChannel):
        embed = hikari.Embed(
            title="User left the server",
            color=0x0000FF,
            timestamp=pendulum.now("Europe/Warsaw")
            )

        embed.set_author(name=member.display_name, icon=member.make_avatar_url())
        embed.add_field(name="User", value=member.mention)
        embed.add_field(name="Username", value=f"{member.display_name}:{member.nickname}")

        await log_channel.send(embed=embed)

# <--------------------------------------------------### Voice events

@plugin.listen(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    before = event.old_state
    after = event.state
    member = event.state.member

    if member is None:
        return

    if member.is_bot:
        return

    log_channel = get_log_channel()

    if isinstance(log_channel, hikari.GuildTextChannel):
        if before is None and after is not None:
            after_channel_id = after.channel_id
            if not after_channel_id:
                return

            after_channel = plugin.client.cache.get_guild_channel(after_channel_id)

            channel_mention = getattr(after_channel, "mention", "Unknown")

            embed = hikari.Embed(
                title="Join to voice channel",
                color=0x00FF00,
                timestamp=pendulum.now("Europe/Warsaw")
                )
            embed.set_author(name=member.display_name, icon=member.make_avatar_url())
            embed.add_field(name="Channel", value=channel_mention)
            embed.add_field(name="User", value=member.mention)
            await log_channel.send(embed=embed)

        elif before is not None and after.channel_id is None:
            before_channel_id = before.channel_id
            if not before_channel_id:
                return

            before_channel = plugin.client.cache.get_guild_channel(before_channel_id)

            channel_mention = getattr(before_channel, "mention", "Unknown")

            embed = hikari.Embed(
                title="Left from voice channel",
                color=0x00FF00,
                timestamp=pendulum.now("Europe/Warsaw")
                )
            embed.set_author(name=member.display_name, icon=member.make_avatar_url())
            embed.add_field(name="Channel", value=channel_mention)
            embed.add_field(name="User", value=member.mention)
            await log_channel.send(embed=embed)

        elif before is not None and before.channel_id != after.channel_id:
            before_channel_id = before.channel_id
            after_channel_id = after.channel_id

            if not before_channel_id or not after_channel_id:
                return

            before_channel = plugin.client.cache.get_guild_channel(before_channel_id)
            after_channel = plugin.client.cache.get_guild_channel(after_channel_id)

            embed = hikari.Embed(
                title="Moving between voice channels",
                color=0x00FF00,
                timestamp=pendulum.now("Europe/Warsaw")
                )
            embed.set_author(name=member.display_name, icon=member.make_avatar_url())
            embed.add_field(
                name="Start",
                value=before_channel.mention if before_channel else "Unknown"
                )
            embed.add_field(
                name="End",
                value=after_channel.mention if after_channel else "Unknown"
                )
            embed.add_field(name="User", value=member.mention)
            await log_channel.send(embed=embed)

# <--------------------------------------------------### Channel Events
@plugin.listen(hikari.GuildChannelCreateEvent)
async def on_channel_create(event: hikari.GuildChannelCreateEvent) -> None:
    log_channel = get_log_channel()

    channel_name = event.channel.name
    if channel_name is None:
        channel_name = "Undefined"

    if isinstance(log_channel, hikari.GuildTextChannel):
        embed = hikari.Embed(
            title="Create guild channel",
            color=0x0000FF,
            timestamp=pendulum.now("Europe/Warsaw")
            )

        embed.add_field(name="Name", value=channel_name)

        await log_channel.send(embed=embed)

@plugin.listen(hikari.GuildChannelDeleteEvent)
async def on_channel_remove(event: hikari.GuildChannelDeleteEvent) -> None:
    log_channel = get_log_channel()

    channel_name = event.channel.name
    if channel_name is None:
        channel_name = "Undefined"

    if isinstance(log_channel, hikari.GuildTextChannel):
        embed = hikari.Embed(
            title="Delete guild channel",
            color=0x0000FF,
            timestamp=pendulum.now("Europe/Warsaw")
            )

        embed.add_field(name="Name", value=channel_name)

        await log_channel.send(embed=embed)

# <--------------------------------------------------### Role Events
@plugin.listen(hikari.RoleCreateEvent)
async def on_role_create(event: hikari.RoleCreateEvent) -> None:
    log_channel = get_log_channel()

    role_name = event.role.name
    if role_name is None:
        role_name = "Undefined"

    if isinstance(log_channel, hikari.GuildTextChannel):
        embed = hikari.Embed(
            title="Create role",
            color=0x0000FF,
            timestamp=pendulum.now("Europe/Warsaw")
            )

        embed.add_field(name="Name", value=role_name)

        await log_channel.send(embed=embed)

@plugin.listen(hikari.RoleDeleteEvent)
async def on_role_remove(event: hikari.RoleDeleteEvent) -> None:
    log_channel = get_log_channel()

    if event.old_role is None:
        return

    role_name = event.old_role.name
    if role_name is None:
        role_name = "Undefined"

    if isinstance(log_channel, hikari.GuildTextChannel):
        embed = hikari.Embed(
            title="Delete guild channel",
            color=0x0000FF,
            timestamp=pendulum.now("Europe/Warsaw")
            )

        embed.add_field(name="Name", value=role_name)

        await log_channel.send(embed=embed)


def get_log_channel() -> typing.Optional[hikari.PermissibleGuildChannel]:
    config_manager: ConfigManager = plugin.client.get_type_dependency(ConfigManager)
    log_channel_id = config_manager.get_config_value("LOG_CHANNEL_ID")
    if not log_channel_id:
        return None
    return plugin.client.cache.get_guild_channel(int(log_channel_id))


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
