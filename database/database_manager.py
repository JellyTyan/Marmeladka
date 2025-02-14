import logging

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class UserData(Base):
    __tablename__ = "user_data"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=True)
    message_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    invite_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    voice_time: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bump_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tag: Mapped[str] = mapped_column(String(50), nullable=True)
    biography: Mapped[str] = mapped_column(String(50), nullable=True)
    birthday_date: Mapped[str] = mapped_column(String(50), nullable=True)

class NuclearData(Base):
    __tablename__ = "nuclear_data"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=True)
    new_user: Mapped[int] = mapped_column(Boolean, nullable=False, default=True)
    nuclear_mode: Mapped[int] = mapped_column(Boolean, nullable=False, default=False)
    bomb_start_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mivina_start_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bomb_cd: Mapped[str] = mapped_column(String(50), nullable=True, default="")
    mivina_cd: Mapped[str] = mapped_column(String(50), nullable=True, default="")

class NuclearLogs(Base):
    __tablename__ = "nuclear_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(20), nullable=True)
    date: Mapped[str] = mapped_column(String(50), nullable=True)
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    log_type: Mapped[str] = mapped_column(String(10), nullable=False)


class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_url: str = "sqlite+aiosqlite:///database/database.sql", echo: bool = False):
        if self._initialized:
            return

        self.db_url = db_url
        self.echo = echo
        self.engine = create_async_engine(self.db_url, echo=self.echo)
        logger.info("Подключение к базе данных успешно")
        self._initialized = True

    async def init_db(self):
        """Creates tables if they do not exist"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База данных инициализирована")

    async def close(self):
        """Closes the database connection"""
        await self.engine.dispose()
        logger.info("Подключение к базе данных закрыто")
