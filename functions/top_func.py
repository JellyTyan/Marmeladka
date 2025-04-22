from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.database_manager import DatabaseManager
from database.models import UserData

database_manager = DatabaseManager()

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


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
