import asyncio
import aiosqlite
import asyncpg
from datetime import datetime

SQLITE_DB = "database/database.sql"
POSTGRES_DSN = "postgresql://marmeladka_user:marmeladkabot@localhost/marmeladka_db"

def parse_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None

async def create_tables(pg_conn):
    create_user_data = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id BIGINT PRIMARY KEY,
        username VARCHAR(30),
        lang VARCHAR(7) DEFAULT 'en-EN',
        message_count INTEGER NOT NULL DEFAULT 0,
        invite_count INTEGER NOT NULL DEFAULT 0,
        voice_time INTEGER NOT NULL DEFAULT 0,
        bump_count INTEGER NOT NULL DEFAULT 0,
        tag VARCHAR(32),
        biography TEXT,
        birthday_date DATE
    );
    """

    create_nuclear_data = """
    CREATE TABLE IF NOT EXISTS nuclear_data (
        user_id BIGINT PRIMARY KEY,
        username VARCHAR(30),
        new_user BOOLEAN NOT NULL DEFAULT TRUE,
        nuclear_mode BOOLEAN NOT NULL DEFAULT FALSE,
        bomb_start_count INTEGER NOT NULL DEFAULT 0,
        mivina_start_count INTEGER NOT NULL DEFAULT 0,
        bomb_cd DATE,
        mivina_cd DATE
    );
    """

    create_nuclear_logs = """
    CREATE TABLE IF NOT EXISTS nuclear_logs (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        username VARCHAR(32),
        date DATE NOT NULL DEFAULT CURRENT_DATE,
        used BOOLEAN NOT NULL DEFAULT FALSE,
        log_type VARCHAR(10) NOT NULL
    );
    """

    create_guild_config = """
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id BIGINT PRIMARY KEY,
        guild_name VARCHAR(32),
        lang VARCHAR(5) DEFAULT 'en-EN',
        welcome_channel_id BIGINT,
        welcome_message TEXT,
        welcome_role_id BIGINT,
        private_category_id BIGINT,
        private_voice_id BIGINT
    );
    """

    create_embed_config = """
    CREATE TABLE IF NOT EXISTS embed_config (
        id SERIAL PRIMARY KEY,
        guild_id BIGINT NOT NULL,
        embed_key VARCHAR,
        title VARCHAR(256),
        description VARCHAR(4096),
        footer_text VARCHAR(2048),
        author_name VARCHAR(256),
        image_url VARCHAR(256),
        thumbnail_url VARCHAR(256),
        footer_icon_url VARCHAR(256),
        color VARCHAR(256),
        url VARCHAR(256),
        CONSTRAINT uix_guild_embed_key UNIQUE (guild_id, embed_key)
    );
    """

    await pg_conn.execute(create_user_data)
    await pg_conn.execute(create_nuclear_data)
    await pg_conn.execute(create_nuclear_logs)
    await pg_conn.execute(create_guild_config)
    await pg_conn.execute(create_embed_config)
    print("Все таблицы успешно созданы.")

async def migrate_user_data(sqlite_conn, pg_conn):
    query = """
        SELECT id, username, message_count, invite_count, voice_time, bump_count, tag, biography, birthday_date
        FROM user_data
    """
    async with sqlite_conn.execute(query) as cursor:
        rows = await cursor.fetchall()
        for row in rows:
            user_id, username, message_count, invite_count, voice_time, bump_count, tag, biography, birthday_date = row
            birthday = parse_date(birthday_date)
            lang = "en-EN"
            try:
                await pg_conn.execute(
                    """
                    INSERT INTO user_data
                    (user_id, username, lang, message_count, invite_count, voice_time, bump_count, tag, biography, birthday_date)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    """,
                    user_id, username, lang, message_count, invite_count, voice_time, bump_count, tag, biography, birthday
                )
            except Exception as e:
                print(f"Ошибка вставки для user_data user_id={user_id}: {e}")

async def migrate_nuclear_data(sqlite_conn, pg_conn):
    query = """
        SELECT user_id, username, new_user, nuclear_mode, bomb_start_count, mivina_start_count, bomb_cd, mivina_cd
        FROM nuclear_data
    """
    async with sqlite_conn.execute(query) as cursor:
        rows = await cursor.fetchall()
        for row in rows:
            user_id, username, new_user, nuclear_mode, bomb_start_count, mivina_start_count, bomb_cd, mivina_cd = row
            bomb_date = parse_date(bomb_cd)
            mivina_date = parse_date(mivina_cd)
            new_user_bool = bool(new_user) if new_user is not None else None
            nuclear_mode_bool = bool(nuclear_mode) if nuclear_mode is not None else None
            try:
                await pg_conn.execute(
                    """
                    INSERT INTO nuclear_data
                    (user_id, username, new_user, nuclear_mode, bomb_start_count, mivina_start_count, bomb_cd, mivina_cd)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    user_id, username, new_user_bool, nuclear_mode_bool, bomb_start_count, mivina_start_count, bomb_date, mivina_date
                )
            except Exception as e:
                print(f"Ошибка вставки для nuclear_data user_id={user_id}: {e}")

async def migrate_nuclear_logs(sqlite_conn, pg_conn):
    async def fetch_and_insert_logs(table_name: str, log_type_value: str):
        query = f"""
            SELECT user_id, username, date, used
            FROM {table_name}
        """
        async with sqlite_conn.execute(query) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                user_id, username, date_str, used = row
                log_date = parse_date(date_str)
                used_bool = bool(used) if used is not None else False
                try:
                    await pg_conn.execute(
                        """
                        INSERT INTO nuclear_logs
                        (user_id, username, date, used, log_type)
                        VALUES ($1, $2, $3, $4, $5)
                        """,
                        user_id, username, log_date, used_bool, log_type_value
                    )
                except Exception as e:
                    print(f"Ошибка вставки из {table_name} user_id={user_id}: {e}")

    print("Миграция bomb_logs...")
    await fetch_and_insert_logs("bomb_logs", "bomb")

    print("Миграция mivina_logs...")
    await fetch_and_insert_logs("mivina_logs", "mivina")

async def main():
    sqlite_conn = await aiosqlite.connect(SQLITE_DB)
    pg_conn = await asyncpg.connect(dsn=POSTGRES_DSN)

    try:
        await create_tables(pg_conn)

        print("Миграция user_data...")
        await migrate_user_data(sqlite_conn, pg_conn)

        print("Миграция nuclear_data...")
        await migrate_nuclear_data(sqlite_conn, pg_conn)

        print("Миграция nuclear_logs...")
        await migrate_nuclear_logs(sqlite_conn, pg_conn)

        print("Миграция завершена.")
    finally:
        await sqlite_conn.close()
        await pg_conn.close()
if __name__ == "__main__":
    asyncio.run(main())
