import logging

from sqlalchemy.ext.asyncio import create_async_engine

from .models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_url: str = "postgresql+asyncpg://marmeladka_user:marmeladkabot@localhost/marmeladka_db", echo: bool = False):
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
