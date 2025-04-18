import hikari
import lightbulb
import pendulum

from database.database_manager import DatabaseManager
from database.models import UserData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

database_manager = DatabaseManager()

loader = lightbulb.Loader()

voice_start_times = {}

@loader.command
class TopVoiceCommand(
    lightbulb.SlashCommand,
    name="commands.topvoice.name",
    description="commands.topvoice.description",
    contexts=(hikari.ApplicationContextType(0),),
    localize=True
):

    @lightbulb.invoke
    async def top_voice(self, ctx: lightbulb.Context) -> None:
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


@loader.listener(hikari.VoiceStateUpdateEvent)
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
    """Обновляет время голосового общения пользователя.

    Args:
        user_id (int): ID пользователя
        username (str): Имя пользователя
        duration (int): Длительность в секундах
    """
    session = async_sessionmaker(database_manager.engine, expire_on_commit=True)
    async with session() as session:
        async with session.begin():
            stmt = select(UserData).where(UserData.user_id == user_id)
            row = await session.scalar(stmt)

            if row:
                row.username = username
                row.voice_time += duration
            else:
                session.add(UserData(id=user_id, username=username, voice_time=duration))

            await session.commit()
            await session.aclose()


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
