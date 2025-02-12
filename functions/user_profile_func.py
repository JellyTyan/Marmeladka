from database.database_manager import DatabaseManager, UserData
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

class UserProfileFunc():
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=False)

    async def get_bump_count(self, id: int) -> int:
        """Get user bump count"""
        async with self.session() as session:
            async with session.begin():
                stmt = select(UserData.bump_count).where(UserData.user_id == id)
                bump_count = await session.scalar(stmt)
                await session.aclose()

        return 0 if bump_count is None else bump_count

    async def get_voice_time(self, id: int) -> str:
        """Get user voice time"""
        async with self.session() as session:
            async with session.begin():
                stmt = select(UserData.voice_time).where(UserData.user_id == id)
                voice_time = await session.scalar(stmt)
                await session.aclose()

        if voice_time is None:
            return "00:00:00"
        else:
            days = voice_time // 86400
            hours = (voice_time % 86400) // 3600
            minutes = (voice_time % 3600) // 60
            seconds = voice_time % 60
            return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"

    async def get_message_count(self, id: int) -> int:
        """Get user message count"""
        async with self.session() as session:
            async with session.begin():
                stmt = select(UserData.message_count).where(UserData.user_id == id)
                message_count = await session.scalar(stmt)
                await session.aclose()

        return 0 if message_count is None else message_count

    async def get_invite_count(self, id: int) -> int:
        """Get user invite count"""
        async with self.session() as session:
            async with session.begin():
                stmt = select(UserData.invite_count).where(UserData.user_id == id)
                invite_count = await session.scalar(stmt)
                await session.aclose()

        return 0 if invite_count is None else invite_count

    async def get_biograpgy(self, id: int) -> str:
        """Get user biography"""
        async with self.session() as session:
            async with session.begin():
                stmt = select(UserData.biography).where(UserData.user_id == id)
                biography = await session.scalar(stmt)
                await session.aclose()

        return "No Bio" if biography is None else biography

    async def get_tag(self, id: int) -> str:
        """Get user tag"""
        async with self.session() as session:
            async with session.begin():
                stmt = select(UserData.tag).where(UserData.user_id == id)
                tag = await session.scalar(stmt)
                await session.aclose()

        return "No tag" if tag is None else tag
