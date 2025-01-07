import hikari
import lightbulb
import pendulum

from database.database_manager import DatabaseManager

database_manager = DatabaseManager()

plugin = lightbulb.Plugin("TopVoice")

voice_start_times = {}

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("топ-войса", "Топ пользователей по длительности нахождения в гс.", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def top_voice(ctx: lightbulb.Context) -> None:
    top_users_list = await database_manager.fetchall("SELECT id, voice_time FROM user_data ORDER BY voice_time DESC LIMIT 10")

    title = "**Топ 10 пользователей по длительности нахождения в голосовых каналах:**\n\n"

    guild = ctx.get_guild()
    if guild is None:
        return

    for index, user in enumerate(top_users_list, start=1):
        user_id, voice_time = user
        if voice_time == 0:
            continue

        voice_time = format_duration(voice_time)
        member = guild.get_member(user_id)
        if member is not None:
            user_ping = member.mention
        else:
            user_ping = f"<@{user_id}>"
        title += f"{index}. `{voice_time}` - {user_ping}\n"
    embed = hikari.Embed(description=title, color=0x2B2D31)
    await ctx.respond(embed=embed)


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    before = event.old_state
    after = event.state
    member = event.state.member

    if member is None:
        return

    if member.is_bot:
        return

    if before is None and after is not None:
        if member.id not in voice_start_times:
            voice_start_times[member.id] = pendulum.now("Europe/Warsaw")
    elif before is not None and after.channel_id is None:
        if member.id in voice_start_times:
            duration = (pendulum.now("Europe/Warsaw") - voice_start_times[member.id]).total_seconds()
            duration = round(duration)
            await update_voice_time(member.id, member.username, duration)
            del voice_start_times[member.id]


async def update_voice_time(user_id: int, username: str, duration: int) -> None:
    row = await database_manager.fetchone("SELECT voice_time FROM user_data WHERE id = ?", (user_id,))

    if row:
        user_voice_time = row[0] + duration
        await database_manager.execute("UPDATE user_data SET username = ?, voice_time = ? WHERE id = ?",(username, user_voice_time, user_id),)
    else:
        user_voice_time = duration
        await database_manager.execute("INSERT INTO user_data (id, username, voice_time) VALUES (?, ?, ?)",(user_id, username, user_voice_time),)


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
