from datetime import timedelta, timezone

import hikari
import arc
import logging
import pendulum
from database.models import UserData
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, extract

from database.database_manager import DatabaseManager
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)

plugin = arc.GatewayPlugin("BirthdayNotification")


@arc.utils.cron_loop("0 9 * * *", timezone=timezone(timedelta(hours=1)))
async def birth_check():
    try:
        today = pendulum.now()
        db = plugin.client.get_type_dependency(DatabaseManager)
        session = async_sessionmaker(db.engine, expire_on_commit=True)

        statement = select(UserData.user_id).where(
            (extract('month', UserData.birthday_date) == today.month) &
            (extract('day', UserData.birthday_date) == today.day)
        )

        async with session() as session:
            result = await session.execute(statement)
            user_ids = result.scalars().all()

        logger.info(f"Found {len(user_ids)} users with birthdays today")

        if not user_ids:
            return

        config = plugin.client.get_type_dependency(ConfigManager)

        try:
            birthday_channel_id = config.get_config_value("BIRTHDAY_CHANNEL_ID")
            channel_id_int = int(birthday_channel_id)
        except Exception as e:
            logger.error(f"Ошибка получения ID канала: {e}")
            return

        for user_id in user_ids:
            try:
                message = f"У <@{user_id}> сегодня день рождения! Поздравляем! https://cdn.discordapp.com/attachments/1108629194788847637/1265283297827881012/Happy_Birthday.mp4?ex=66a0f266&is=669fa0e6&hm=0b568445807e5efce7ff5e22b77fb58951f973c3dcff443012e89f7be3d0cac5&"
                await plugin.client.rest.create_message(channel_id_int, message, user_mentions=True)
                logger.info(f"Birthday message sent for user {user_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение для user_id {user_id}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error in birth_check: {e}", exc_info=True)

@plugin.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    birth_check.start()

@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
