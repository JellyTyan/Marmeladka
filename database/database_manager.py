import aiosqlite
from typing import Any, List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "./database/database.sql"):
        self.db_path = db_path

    async def execute(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        """Выполняет запрос без возврата данных (например, INSERT, UPDATE, DELETE)."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(query, params or ())
            await db.commit()

    async def fetchone(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple[Any, ...]]:
        """Выполняет запрос и возвращает одну запись в виде кортежа."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row  # Устанавливаем row_factory для управления форматом
            cursor = await db.execute(query, params or ())
            row = await cursor.fetchone()
            await cursor.close()
            return tuple(row) if row else None  # Преобразуем Row в кортеж

    async def fetchall(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple[Any, ...]]:
        """Выполняет запрос и возвращает все записи."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(query, params or ())
            rows = await cursor.fetchall()
            results = [tuple(row) for row in rows]
            await cursor.close()
            return results

    async def create_table(self, table_name: str, schema: str) -> None:
        """
        Создает таблицу, если она не существует.
        :param table_name: Имя таблицы.
        :param schema: Схема таблицы (например, 'id INTEGER PRIMARY KEY, name TEXT').
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        await self.execute(query)
