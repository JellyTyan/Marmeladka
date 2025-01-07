import hikari
import lightbulb

from database.database_manager import DatabaseManager

database_manager = DatabaseManager()

plugin = lightbulb.Plugin("TopMessages")


@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("топ-сообщений", "Топ пользователей по сообщениям.", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def top_messages(ctx: lightbulb.Context) -> None:
    top_users_list = await database_manager.fetchall("SELECT id, message_count FROM user_data ORDER BY message_count DESC LIMIT 10")

    title = "**Топ 10 пользователей по количеству сообщений на сервере:**\n\n"

    guild = ctx.get_guild()
    if guild is None:
        return

    for index, user in enumerate(top_users_list, start=1):
        user_id, message_count = user
        if message_count == 0:
            continue

        member = guild.get_member(user_id)
        if member is not None:
            user_ping = member.mention
        else:
            user_ping = f"<@{user_id}>"
        title += f"{index}. `{message_count} сообщений` - {user_ping}\n"
    embed = hikari.Embed(description=title, color=0x2b2d31)

    await ctx.respond(embed=embed)


@plugin.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    if not event.message.attachments:
        if not event.author.is_bot:
            channel = await event.app.rest.fetch_channel(event.channel_id)
            if channel is None:
                return
            if not isinstance(channel, hikari.GuildTextChannel):
                return

            await update_message_count(event.author.id, event.author.username)


async def update_message_count(user_id: int, username: str):
    row = await database_manager.fetchone("SELECT message_count FROM user_data WHERE id = ?", (user_id,))

    if row:
        message_count = row[0] + 1
        await database_manager.execute("UPDATE user_data SET username = ?, message_count = ? WHERE id = ?",(username, message_count, user_id))
    else:
        message_count = 1
        await database_manager.execute("INSERT INTO user_data (id, username, message_count) VALUES (?, ?, ?)",(user_id, username, message_count))


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
