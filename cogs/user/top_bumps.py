import hikari
from hikari.events import channel_events
import lightbulb

from database.database_manager import DatabaseManager

database_manager = DatabaseManager()


plugin = lightbulb.Plugin("TopBumps")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("топ-бампов", "Топ пользователей по бампам.", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def top_messages(ctx: lightbulb.Context) -> None:
    top_users_list = await database_manager.fetchall("SELECT id, bump_count FROM user_data ORDER BY bump_count DESC LIMIT 10")

    title = "Топ 10 пользователей по количеству бампов на сервере:\n\n"

    guild = ctx.get_guild()
    if guild is None:
        return

    for index, user in enumerate(top_users_list, start=1):
        user_id, bump_count = user
        if bump_count == 0:
            continue

        member = guild.get_member(user_id)
        if member is not None:
            user_ping = member.mention
        else:
            user_ping = f"<@{user_id}>"

        title += f"{index}. {user_ping} - {bump_count} бампов\n"
    embed = hikari.Embed(description=title, color=0x2B2D31)

    await ctx.respond(embed=embed)


@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    try:
        if event.author.is_bot:
            embed = event.embeds[0]

            if embed.description and "Время реакции" in embed.description:
                if embed.author is None:
                    return
                user_name = embed.author.name

                guild = event.get_guild()
                if guild is None:
                    return

                members = guild.get_members()

                for member in members:
                    member = guild.get_member(member)
                    if member is None:
                        continue
                    if member.username == user_name:
                        user = member
                        break

                await update_bump_count(user.id, user_name)

                bump_count = await database_manager.fetchone("SELECT bump_count FROM user_data WHERE id = ?",(user.id,),)

                embed_success = hikari.Embed(
                    description=f"Хэй, {user.mention}, спасибочки!\n Общее твоё количество бампов: `{bump_count[0]}`",
                    color=0x2B2D31,
                )
                channel = event.get_channel()
                if isinstance(channel, hikari.GuildTextChannel):
                    await channel.send(embed=embed_success)

    except Exception as e:
        print(e)
        pass


async def update_bump_count(user_id: int, username: str) -> None:
    row = await database_manager.fetchone("SELECT bump_count FROM user_data WHERE id = ?", (user_id,))

    if row:
        bump_count = row[0] + 1
        await database_manager.execute("UPDATE user_data SET username = ?, bump_count = ? WHERE id = ?",(username, bump_count, user_id),)
    else:
        bump_count = 1
        await database_manager.execute("INSERT INTO user_data (id, username, bump_count) VALUES (?, ?, ?)",(user_id, username, bump_count),)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
