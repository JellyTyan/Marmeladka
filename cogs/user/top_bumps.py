import hikari
import lightbulb
import logging

from database.database_manager import DatabaseManager
from database.models import UserData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

database_manager = DatabaseManager()

loader = lightbulb.Loader()

logger = logging.getLogger(__name__)

@loader.command
class TopBumpsCommand(
    lightbulb.SlashCommand,
    name="commands.topbumps.name",
    description="commands.topbumps.description",
    contexts=(hikari.ApplicationContextType(0),),
    localize=True
):

    @lightbulb.invoke
    async def top_messages(self, ctx: lightbulb.Context) -> None:
        session = async_sessionmaker(database_manager.engine, expire_on_commit=False)
        async with session() as session:
            stmt = select(UserData).order_by(UserData.bump_count.desc()).limit(10)
            top_users_list = await session.scalars(stmt)
            await session.aclose()

        title = "**Top 10 users by number of bumps on the server:**\n\n"

        guild_id = ctx.guild_id
        if guild_id is None:
            return

        guild = await ctx.client.rest.fetch_guild(guild_id)
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


@loader.listener(hikari.GuildMessageCreateEvent)
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


async def update_bump_count(user_id: int, username: str) -> None:
    """Обновляет количество бамповых операций пользователя.

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
                row.bump_count += 1
            else:
                session.add(UserData(id=user_id, username=username, bump_count=1))

            await session.commit()
            await session.aclose()
