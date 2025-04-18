import hikari
import lightbulb

from database.database_manager import DatabaseManager
from database.models import UserData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

database_manager = DatabaseManager()

loader = lightbulb.Loader()


@loader.command
class TopMessagesCommand(
    lightbulb.SlashCommand,
    name="commands.topmessages.name",
    description="commands.topmessages.description",
    contexts=(hikari.ApplicationContextType(0),),
    localize=True
):

    @lightbulb.invoke
    async def top_messages(self, ctx: lightbulb.Context) -> None:
        session = async_sessionmaker(database_manager.engine, expire_on_commit=False)
        async with session() as session:
            stmt = select(UserData).order_by(UserData.message_count.desc()).limit(10)
            top_users_list = await session.scalars(stmt)
            await session.aclose()

        title = "**Top 10 users by number of messages on the server:**\n\n"

        guild_id = ctx.guild_id
        if guild_id is None:
            return

        guild = await ctx.client.rest.fetch_guild(guild_id)
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
            title += f"{index}. `{user.message_count} сообщений` - {user_ping}\n"
        embed = hikari.Embed(description=title, color=0x2b2d31)

        await ctx.respond(embed=embed)


@loader.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    if not event.message.attachments:
        if not event.author.is_bot:
            channel = await event.app.rest.fetch_channel(event.channel_id)
            if channel is None:
                return
            if not isinstance(channel, hikari.GuildTextChannel):
                return

            await update_message_count(event.author.id, event.author.username)


async def update_message_count(user_id: int, username: str) -> None:
    """Обновляет количество сообщений пользователя.

    Args:
        user_id (int): ID пользователя
        username (str): Имя пользователя
    """
    session = async_sessionmaker(database_manager.engine, expire_on_commit=True)
    async with session() as session:
        async with session.begin():
            stmt = select(UserData).where(UserData.user_id == user_id)
            row = await session.scalar(stmt)

            if row:
                row.username = username
                row.message_count += 1
            else:
                session.add(UserData(id=user_id, username=username, message_count=1))

            await session.commit()
            await session.aclose()
