import os
import random
from io import BytesIO

import hikari
import pendulum
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import and_, func, insert, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.database_manager import DatabaseManager
from database.models import NuclearData, NuclearLogs


class NuclearFunc():
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=False)


    async def get_weapon_count(self, user_id: int, nuclear_type: str) -> int:
        """Получение количества оружия у пользователя.

        Args:
            user_id (int): ID пользователя.
            nuclear_type (str): Тип оружия ('mivina' или 'bomb').

        Returns:
            int: Количество доступного оружия.
        """
        if nuclear_type not in {"mivina", "bomb"}:
            return 0

        async with self.session() as session:
            stmt = (
                select(func.count())
                .select_from(NuclearLogs)
                .where(
                    and_(
                        NuclearLogs.user_id == user_id,
                        NuclearLogs.used.is_(False),
                        NuclearLogs.log_type == nuclear_type,
                    )
                )
            )
            weapon_count = await session.scalar(stmt)

        return weapon_count or 0


    async def check_cooldown(self, user_id: int, cooldown_type: str) -> bool:
        """Проверка кулдауна для получения предмета (ядерки или мивины).

        Args:
            user_id (int): ID пользователя.
            cooldown_type (str): Тип кулдауна ('bomb_cd' или 'mivina_cd').

        Returns:
            bool: True, если кулдаун прошёл, иначе False.
        """
        if cooldown_type not in {"bomb_cd", "mivina_cd"}:
            return True

        async with self.session() as session:
            stmt = select(getattr(NuclearData, cooldown_type)).where(NuclearData.user_id == user_id)
            last_time = await session.scalar(stmt)

        if last_time is None:
            return True

        current_date = pendulum.now().date()
        return current_date > last_time


    async def update_cooldown(self, user_id: int, cooldown_type: str) -> None:
        """Обновляет кулдаун для указанного типа предмета (ядерки или мивины).

        Args:
            user_id (int): ID пользователя.
            cooldown_type (str): Тип кулдауна ('bomb_cd' или 'mivina_cd').
        """
        if cooldown_type not in {"bomb_cd", "mivina_cd"}:
            return

        current_time = pendulum.now().date()

        async with self.session() as session:
            async with session.begin():
                stmt = (
                    update(NuclearData)
                    .where(NuclearData.user_id == user_id)
                    .values({cooldown_type: current_time})
                )
                result = await session.execute(stmt)

                if result.rowcount == 0:
                    session.add(NuclearData(user_id=user_id, **{cooldown_type: current_time}))

            await session.commit()


    async def get_start_count(self, user_id: int, column: str) -> int:
        """Получение количества запусков (ядерки или мивины).

        Args:
            user_id (int): ID пользователя.
            column (str): Название столбца ('bomb_start_count' или 'mivina_start_count').

        Returns:
            int: Количество запусков.
        """
        valid_columns = {"bomb_start_count", "mivina_start_count"}
        if column not in valid_columns:
            raise ValueError(f"Некорректное имя столбца: {column}")

        async with self.session() as session:
            async with session.begin():
                stmt = select(getattr(NuclearData, column)).where(NuclearData.user_id == user_id)
                count = await session.scalar(stmt)

        return count or 0


    async def update_start_count(self, user_id: int, count: int, column: str) -> None:
        """Обновление количества запусков (ядерки или мивины) у пользователя.

        Args:
            user_id (int): ID пользователя.
            count (int): Новое значение счётчика.
            column (str): Название столбца ('bomb_start_count' или 'mivina_start_count').
        """
        valid_columns = {"bomb_start_count", "mivina_start_count"}
        if column not in valid_columns:
            raise ValueError(f"Некорректное имя столбца: {column}")

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData).where(NuclearData.user_id == user_id)
                user_data = await session.scalar(stmt)

                if user_data:
                    setattr(user_data, column, count)
                else:
                    user_data = NuclearData(user_id=user_id, **{column: count})
                    session.add(user_data)

                session.add(user_data)


    async def wrote_log(self, user_id: int, user_name: str, log_type: str) -> None:
        """Запись в базу данных о новой полученной мивинке или ядерке.

        Args:
            user_id (int): ID пользователя.
            user_name (str): Ник пользователя.
            log_type (str): Тип лога ('bomb' или 'mivina').
        """
        valid_types = {"bomb", "mivina"}
        if log_type not in valid_types:
            raise ValueError(f"Некорректный тип лога: {log_type}")

        async with self.session() as session:
            async with session.begin():
                session.add(NuclearLogs(
                    user_id=user_id,
                    username=user_name,
                    date=pendulum.now().date(),
                    used=False,
                    log_type=log_type
                ))


    async def get_oldest_weapon_id(self, user_id: int, weapon_type: str) -> int | None:
        """Получение самой старой записи (ядерки или мивинки) у пользователя.

        Args:
            user_id (int): айди пользователя
            weapon_type (str): тип оружия ("bomb" или "mivina")

        Returns:
            int | None: айди самой старой записи или None, если записи нет
        """
        valid_types = {"bomb", "mivina"}
        if weapon_type not in valid_types:
            raise ValueError(f"Некорректный тип оружия: {weapon_type}")

        async with self.session() as session:
            async with session.begin():
                stmt = (
                    select(NuclearLogs.id)
                    .where(
                        NuclearLogs.user_id == user_id,
                        NuclearLogs.used.is_(False),
                        NuclearLogs.log_type == weapon_type
                    )
                    .order_by(NuclearLogs.date.asc())
                    .limit(1)
                )
                return await session.scalar(stmt)


    async def is_weapon_activated(self, weapon_id: int) -> bool:
        """Проверка, активируется ли оружие (ядерка или мивинка).

        Args:
            weapon_id (int): айди записи в NuclearLogs

        Returns:
            bool: True, если запись активируется, иначе False
        """
        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.date).where(NuclearLogs.id == weapon_id)
                last_time = await session.scalar(stmt)

        if not last_time:
            return False

        last_time = pendulum.instance(last_time)

        current_time = pendulum.today().date()

        days_since_received = (current_time - last_time).days

        return should_activate_nuke(days_since_received)


    async def is_bomb_make_hirohito(self, bomb_id: int) -> bool:
        """Проверка взорвёт ли ядерка отправителя и получателя одновременно."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearLogs.date).where(NuclearLogs.id == bomb_id)
                last_time = await session.scalar(stmt)

        if not last_time:
            return False

        last_time = pendulum.instance(last_time)

        current_time = pendulum.today().date()

        days_since_received = (current_time - last_time).days

        return should_nuke_make_hirohito(days_since_received)


    async def update_log_used(self, weapon_id: int) -> None:
        """Обновляет запись в логе, помечая оружие как использованную.

        Args:
            weapon_id (int): айди записи в NuclearLogs
        """
        async with self.session() as session:
            async with session.begin():
                stmt = update(NuclearLogs).where(NuclearLogs.id == weapon_id).values(used=True)
                await session.execute(stmt)
                await session.commit()


    async def reset_bombs(self, user_id: int) -> None:
        """Сброс ядерок у пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = update(NuclearLogs).where(NuclearLogs.user_id == user_id).values(used=1)
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

        return row if row is not None else False


    async def update_nuclear_mode(self, user_id: int, mode: bool) -> None:
        """Обновляет ядерный режим пользователя."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.nuclear_mode).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)

                if row is not None:
                    update_stmt = (
                        update(NuclearData)
                        .where(NuclearData.user_id == user_id)
                        .values(nuclear_mode=mode)
                    )
                    await session.execute(update_stmt)
                else:
                    insert_stmt = insert(NuclearData).values(user_id=user_id, nuclear_mode=mode)
                    await session.execute(insert_stmt)


    async def get_new_user(self, user_id: int) -> bool:
        """Получение значения new_user. Если отсутствует запись, то возвращает True."""

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData.new_user).where(NuclearData.user_id == user_id)
                row = await session.scalar(stmt)

        return row if row is not None else True


    async def set_new_user(self, user_id: int, mode: bool) -> None:
        """Устанавливает значение new_user.

        Args:
            user_id (int): айди пользователя
            mode (bool): режим
        """
        async with self.session() as session:
            async with session.begin():
                row = await session.execute(select(NuclearData).where(NuclearData.user_id == user_id))
                row = row.scalars().first()

                if row:
                    row.new_user = mode
                else:
                    session.add(NuclearData(user_id=user_id, new_user=mode))

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
        num_font = ImageFont.truetype("src/fonts/nuclear.ttf", size=50)

        text = user.username
        text_width = idraw.textlength(text, font=nickname_font)
        x = (wallpaper.width - text_width) // 2
        y = 310
        idraw.text((x, y), text, font=nickname_font, align="left", fill=(0, 0, 0))

        num_nuc = str(await self.get_weapon_count(user.id, nuclear_type="bomb"))
        num_miv = str(await self.get_weapon_count(user.id, nuclear_type="mivina"))
        idraw.text((293, 150), num_nuc, font=num_font, fill=(0, 0, 0))
        idraw.text((1285, 150), num_miv, font=num_font, fill=(0, 0, 0))

        num_nuc_start = str(await self.get_start_count(user.id, "bomb_start_count"))
        num_miv_start = str(await self.get_start_count(user.id, "mivina_start_count"))
        idraw.text((319, 290), num_nuc_start, font=num_font, fill=(0, 0, 0))
        idraw.text((1293, 290), num_miv_start, font=num_font, fill=(0, 0, 0))

        os.makedirs("temp", exist_ok=True)

        image_path = f"temp/{user.id}.png"

        wallpaper.save(image_path)

        return image_path

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
