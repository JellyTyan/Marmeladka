import random
from io import BytesIO

import hikari
import pendulum
from PIL import Image, ImageDraw, ImageFont

from database.database_manager import DatabaseManager, NuclearLogs, NuclearData
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, func, update, insert

class NuclearFunc():
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=False)


    async def get_weapon_count(self, user_id: int, nuclear_type: str) -> int | None:
        """Получение количества оружия у пользователя"""
        if nuclear_type not in ["mivina", "nuclear"]:
            return None
        async with self.session() as session:
            async with session.begin():
                stmt = select(func.count()).select_from(NuclearLogs).where(NuclearLogs.user_id == user_id, NuclearLogs.used == 0, NuclearLogs.log_type == nuclear_type)
                weapon_count = await session.scalar(stmt)
                await session.aclose()

        return weapon_count if weapon_count else 0


    async def check_bomb_cooldown(self, user_id: int) -> bool:
        """Проверка кулдауна для получения ядерки (кулдаун 1 день)."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.bomb_cd).where(NuclearData.user_id == user_id)
                bomb_cd = await session.scalar(stmt)
                await session.aclose()

        if bomb_cd is not None:
            current_time = pendulum.now().to_date_string()  # Формат YYYY-MM-DD
            return current_time > bomb_cd

        return True


    async def update_bomb_cooldown(self, user_id: int) -> None:
        """Обновляет кулдаун ядерки у пользователя."""

        current_time = pendulum.now().to_date_string()

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData).where(NuclearData.user_id == user_id)
                user_data = await session.scalar(stmt)

                if user_data:
                    user_data.bomb_cd = current_time
                    session.add(user_data)
                else:
                    new_user_data = NuclearData(user_id=user_id, bomb_cd=current_time)
                    session.add(new_user_data)

                await session.commit()
                await session.aclose()


    async def get_bomb_start_count(self, user_id: int) -> int:
        """Получение количества запусков ядерок."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.bomb_start_count).where(NuclearData.user_id == user_id)
                bomb_start_count = await session.scalar(stmt)
                await session.aclose()

        return bomb_start_count if bomb_start_count is not None else 0


    async def update_bomb_start_count(self, user_id: int, count: int) -> None:
        """Обновление количества запусков ядерок у пользователя."""

        async with self.session() as session:
            async with session.begin():
                # Проверяем существование записи
                stmt = select(NuclearData).where(NuclearData.user_id == user_id)
                user_data = await session.scalar(stmt)

                if user_data:
                    # Обновляем значение, если запись существует
                    user_data.bomb_start_count = count
                    session.add(user_data)
                else:
                    # Создаем новую запись, если её нет
                    new_user_data = NuclearData(user_id=user_id, bomb_start_count=count)
                    session.add(new_user_data)

                await session.commit()
                await session.aclose()


    async def wrote_bomb_log(self, user_id: int, user_name: str) -> None:
        """Запись в базу данных о новой полученной ядерке."""

        current_time = pendulum.now().to_date_string()  # Формат YYYY-MM-DD

        async with self.session() as session:
            async with session.begin():
                new_bomb_log = NuclearLogs(user_id=user_id, username=user_name, date=current_time, used=False, log_type="bomb")
                session.add(new_bomb_log)

                await session.commit()
                await session.aclose()


    async def get_oldest_bomb_id(self, user_id: int) -> int:
        """Получение самой старой ядерки у пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.id).where(NuclearLogs.user_id == user_id, NuclearLogs.used == 0, NuclearLogs.log_type == "bomb").order_by(NuclearLogs.date.asc()).limit(1)
                oldest_bomb_id = await session.scalar(stmt)
                await session.aclose()

        return oldest_bomb_id if oldest_bomb_id is not None else 0


    async def is_bomb_activated(self, bomb_id: int) -> bool:
        """Проверка запустится ли ядерка."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.date).where(NuclearLogs.id == bomb_id)
                last_time_str = await session.scalar(stmt)
                await session.aclose()

        if not last_time_str:
            return False

        last_time = pendulum.parse(last_time_str)
        current_time = pendulum.now()
        days_since_received = (current_time - last_time).days

        return should_activate_nuke(days_since_received)


    async def is_bomb_make_hirohito(self, bomb_id: int) -> bool:
        """Проверка взорвёт ли ядерка отправителя и получателя одновременно."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.date).where(NuclearLogs.id == bomb_id)
                last_time_str = await session.scalar(stmt)
                await session.aclose()

        if not last_time_str:
            return False

        last_time = pendulum.parse(last_time_str)
        current_time = pendulum.now()
        days_since_received = (current_time - last_time).days

        return should_nuke_make_hirohito(days_since_received)

    async def update_bomb_log(self, bomb_id: int) -> None:
        """Обновляет запись о конкретной ядерке, делая её использованной."""

        async with self.session() as session:
            async with session.begin():
                stmt = update(NuclearLogs).where(NuclearLogs.id == bomb_id).values(used=1)
                await session.execute(stmt)
                await session.commit()
                await session.aclose()


    async def reset_bombs(self, user_id: int) -> None:
        """Сброс ядерок у пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = update(NuclearLogs).where(NuclearLogs.user_id == user_id).values(used=1)
                await session.execute(stmt)
                await session.commit()
                await session.aclose()
# ---------------------------------------------------------------------------------------------------------------------Mivina>
    async def check_mivina_cooldown(self, user_id: int) -> bool:
        """Проверка кулдауна для получения мивинок. Кулдаун в 1 день."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.mivina_cd).where(NuclearData.user_id == user_id)
                result = await session.execute(stmt)
                row = result.scalar()

                await session.aclose()

        if row:
            last_time = row
            current_time = pendulum.now().strftime("%Y-%m-%d")
            return current_time > last_time

        return True


    async def update_mivina_cooldown(self, user_id: int) -> None:
        """Обновление кулдауна мивинки у пользователя"""

        current_time = pendulum.now().strftime("%Y-%m-%d")

        async with self.session() as session:
            async with session.begin():
                # Проверка, существует ли запись
                stmt = select(NuclearData.mivina_cd).where(NuclearData.user_id == user_id)
                result = await session.execute(stmt)
                row = result.scalar()

                if row:
                    # Если запись существует - обновляем значение
                    await session.execute(
                        update(NuclearData).where(NuclearData.user_id == user_id).values(mivina_cd=current_time)
                    )
                else:
                    # Если записи нет - создаём новую
                    await session.execute(
                        insert(NuclearData).values(user_id=user_id, mivina_cd=current_time)
                    )

                await session.commit()
                await session.aclose()


    async def get_mivina_start_count(self, user_id: int) -> int:
        """Получение количества использований мивинки"""
        async with self.session() as session:
            stmt = select(NuclearData.mivina_start_count).where(NuclearData.user_id == user_id)
            result = await session.execute(stmt)
            row = result.scalar()
        return row if row else 0


    async def update_mivina_start_count(self, user_id: int, count: int) -> None:
        """Обновление количества использования мивинок у пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.mivina_start_count).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)

                if row is not None:
                    update_stmt = (
                        update(NuclearData)
                        .where(NuclearData.user_id == user_id)
                        .values(mivina_start_count=count)
                    )
                    await session.execute(update_stmt)
                else:
                    insert_stmt = NuclearData(user_id=user_id, mivina_start_count=count)
                    session.add(insert_stmt)

                await session.commit()
                await session.aclose()


    async def wrote_mivina_log(self, user_id: int, user_name: str) -> None:
        """Запись в базу данных о новой полученной мивинке."""

        async with self.session() as session:
            async with session.begin():
                new_log = NuclearLogs(
                    user_id=user_id,
                    username=user_name,
                    date=pendulum.now().to_date_string(),
                    used=False,
                    log_type="mivina"
                )
                session.add(new_log)
                await session.commit()
                await session.aclose()


    async def get_oldest_mivina_id(self, user_id: int) -> int | None:
        """Получение самой старой мивинки у пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.id).where(NuclearLogs.user_id == user_id, NuclearLogs.used == 0, NuclearLogs.log_type == "mivina").order_by(NuclearLogs.date.asc()).limit(1)
                get_oldest_mivina_id = await session.scalar(stmt)
                await session.aclose()

        return get_oldest_mivina_id if get_oldest_mivina_id is not None else None


    async def is_mivina_activated(self, mivina_id: int) -> bool:
        """Проверка, активируется ли мивинка."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.date).where(NuclearLogs.id == mivina_id)
                row = await session.scalar(stmt)
                await session.aclose()

        if row:
            last_time = pendulum.parse(row)
            days_since_received = (pendulum.now() - last_time).days
            return should_activate_nuke(days_since_received)

        return False


    async def update_mivina_log(self, mivina_id: int) -> None:
        """Обновляет запись о конкретной мивинке, помечая её как использованную."""

        async with self.session() as session:
            async with session.begin():
                stmt = (
                    update(NuclearLogs)
                    .where(NuclearLogs.id == mivina_id)
                    .values(used=True)
                )
                await session.execute(stmt)
                await session.commit()
                await session.aclose()
# --------------------------------------------------------------------------------------------------------------------- User>
    async def get_nuclear_mode(self, user_id: int) -> bool:
        """Получение ядерного режима пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.nuclear_mode).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)
                await session.aclose()

        return row == 1 if row is not None else False


    async def update_nuclear_mode(self, user_id: int, mode: int) -> None:
        """Обновляет ядерный режим пользователя."""

        async with self.session() as session:
            async with session.begin():
                # Проверяем, существует ли запись
                stmt = select(NuclearData.nuclear_mode).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)

                if row is not None:
                    # Обновляем существующую запись
                    update_stmt = (
                        update(NuclearData)
                        .where(NuclearData.user_id == user_id)
                        .values(nuclear_mode=mode)
                    )
                    await session.execute(update_stmt)
                else:
                    # Создаем новую запись
                    insert_stmt = insert(NuclearData).values(user_id=user_id, nuclear_mode=mode)
                    await session.execute(insert_stmt)

                await session.commit()
                await session.aclose()


    async def get_new_user(self, user_id: int) -> bool:
        """Получение значения new_user. Если отсутствует запись, то возвращает True."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.new_user).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)
                await session.aclose()

        return row == 1 if row is not None else True


    async def set_new_user(self, user_id: int, mode: bool) -> None:
        """Устанавливает значение new_user.

        Args:
            user_id (int): айди пользователя
            mode (bool): режим, где True = 1 и False = 0
        """
        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)

                if row:
                    # Если запись существует - обновляем значение
                    row.new_user = mode
                else:
                    # Если записи нет - создаём новую
                    session.add(NuclearData(user_id=user_id, new_user=mode))

                await session.commit()
                await session.aclose()

# ------------------------------------------------------> Help

    async def generate_arsenal(self, user: hikari.User) -> str:
        """Генерирует арсенал для пользователя

        Args:
            user_id (int): айди пользователя
        """
        wallpaper = Image.open("src/img/garageArmy.png")
        avatar = user.display_avatar_url
        avt = BytesIO(await avatar.read())
        img = Image.open(avt)
        img = img.resize((160, 160))
        wallpaper.paste(img, (620, 130))

        idraw = ImageDraw.Draw(wallpaper)
        nickname_font = ImageFont.truetype("src/fonts/nuclear.ttf", size=50)
        num_font = ImageFont.truetype("src/fontspip install sqlalchemy[asyncio]/nuclear.ttf", size=50)

        text = user.username
        text_width = idraw.textlength(text, font=nickname_font)
        x = (wallpaper.width - text_width) // 2
        y = 310
        idraw.text((x, y), text, font=nickname_font, align="left", fill=(0, 0, 0))

        num_nuc = str(await self.get_weapon_count(user.id, nuclear_type="bomb"))
        num_miv = str(await self.get_weapon_count(user.id, nuclear_type="mivina"))
        idraw.text((293, 150), num_nuc, font=num_font, fill=(0, 0, 0))
        idraw.text((1285, 150), num_miv, font=num_font, fill=(0, 0, 0))

        num_nuc_start = str(await self.get_bomb_start_count(user.id))
        num_miv_start = str(await self.get_mivina_start_count(user.id))
        idraw.text((319, 290), num_nuc_start, font=num_font, fill=(0, 0, 0))
        idraw.text((1293, 290), num_miv_start, font=num_font, fill=(0, 0, 0))
        wallpaper.save("profileTemp.png")

        return "profileTemp.png"

def get_activation_chance(days_since_received: int):
    if days_since_received >= 30:
        return 10.0

    initial_chance = 100.0
    final_chance = 10.0
    days_to_min_chance = 30
    decrease_per_day = (initial_chance - final_chance) / days_to_min_chance

    chance = initial_chance - days_since_received * decrease_per_day
    return max(chance, final_chance)

def should_activate_nuke(days_since_received: int):
    chance = get_activation_chance(days_since_received)
    random_value = random.uniform(0, 100)
    return random_value <= chance


def get_hirohito_chance(days_since_received: int):
    if days_since_received <= 7:
        return 0.0
    if days_since_received >= 30:
        return 10.0

    initial_chance = 100.0
    final_chance = 10.0
    days_to_min_chance = 30
    decrease_per_day = (initial_chance - final_chance) / days_to_min_chance

    chance = initial_chance - days_since_received * decrease_per_day
    return max(chance, final_chance)

def should_nuke_make_hirohito(days_since_received: int):
    chance = get_activation_chance(days_since_received)
    random_value = random.uniform(0, 100)
    return random_value >= chance
