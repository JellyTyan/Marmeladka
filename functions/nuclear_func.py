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
        """Получение количества оружия у пользователя
        Args:
            user_id (int): ID пользователя.
            nuclear_type (str): Тип кулдауна ('mivina' или 'bomb').

        Returns:
            bool: True, если кулдаун прошёл, иначе False.
        """
        if nuclear_type not in ["mivina", "bomb"]:
            return None
        async with self.session() as session:
            async with session.begin():
                stmt = select(func.count()).select_from(NuclearLogs).where(NuclearLogs.user_id == user_id, NuclearLogs.used == 0, NuclearLogs.log_type == nuclear_type)
                weapon_count = await session.scalar(stmt)
                await session.aclose()

        return weapon_count if weapon_count else 0


    async def check_cooldown(self, user_id: int, cooldown_type: str) -> bool:
        """Проверка кулдауна для получения предмета (ядерки или мивины).

        Args:
            user_id (int): ID пользователя.
            cooldown_type (str): Тип кулдауна ('bomb_cd' или 'mivina_cd').

        Returns:
            bool: True, если кулдаун прошёл, иначе False.
        """
        async with self.session() as session:
            async with session.begin():
                stmt = select(getattr(NuclearData, cooldown_type)).where(NuclearData.user_id == user_id)
                last_time = await session.scalar(stmt)
                await session.aclose()

        if last_time:
            current_time = pendulum.now().to_date_string()
            return current_time > last_time

        return True


    async def update_cooldown(self, user_id: int, cooldown_type: str) -> None:
        """Обновляет кулдаун для указанного типа предмета (ядерки или мивины).

        Args:
            user_id (int): ID пользователя.
            cooldown_type (str): Тип кулдауна ('bomb_cd' или 'mivina_cd').
        """
        current_time = pendulum.now().to_date_string()

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData).where(NuclearData.user_id == user_id)
                user_data = await session.scalar(stmt)

                if user_data:
                    setattr(user_data, cooldown_type, current_time)
                    session.add(user_data)
                else:
                    new_user_data = NuclearData(user_id=user_id, **{cooldown_type: current_time})
                    session.add(new_user_data)

                await session.commit()
                await session.aclose()


    async def get_start_count(self, user_id: int, column: str) -> int:
        """Получение количества запусков (ядерки или мивинки).

        Args:
            user_id (int): айди пользователя
            column (str): название столбца (bomb_start_count или mivina_start_count)

        Returns:
            int: количество запусков
        """
        if column not in ["bomb_start_count", "mivina_start_count"]:
            raise ValueError("Некорректное имя столбца")

        async with self.session() as session:
            async with session.begin():
                stmt = select(getattr(NuclearData, column)).where(NuclearData.user_id == user_id)
                count = await session.scalar(stmt)
                await session.aclose()

        return count if count is not None else 0


    async def update_start_count(self, user_id: int, count: int, column: str) -> None:
        """Обновление количества запусков (ядерки или мивинки) у пользователя.

        Args:
            user_id (int): айди пользователя
            count (int): новое значение счётчика
            column (str): название столбца (bomb_start_count или mivina_start_count)
        """
        if column not in ["bomb_start_count", "mivina_start_count"]:
            raise ValueError("Некорректное имя столбца")

        async with self.session() as session:
            async with session.begin():
                stmt = select(NuclearData).where(NuclearData.user_id == user_id)
                user_data = await session.scalar(stmt)

                if user_data:
                    setattr(user_data, column, count)
                    session.add(user_data)
                else:
                    new_user_data = NuclearData(user_id=user_id, **{column: count})
                    session.add(new_user_data)

                await session.commit()
                await session.aclose()


    async def wrote_log(self, user_id: int, user_name: str, log_type: str) -> None:
        """Запись в базу данных о новой полученной мивинке или ядерке.

        Args:
            user_id (int): айди пользователя
            user_name (str): ник пользователя
            log_type (str): тип лога (bomb или mivina)
        """
        if log_type not in ["bomb", "mivina"]:
            raise ValueError("Некорректный тип лога")

        current_time = pendulum.now().to_date_string()

        async with self.session() as session:
            async with session.begin():
                new_log = NuclearLogs(
                    user_id=user_id,
                    username=user_name,
                    date=current_time,
                    used=False,
                    log_type=log_type
                )
                session.add(new_log)
                await session.commit()
                await session.aclose()


    async def get_oldest_weapon_id(self, user_id: int, weapon_type: str) -> int | None:
        """Получение самой старой записи (ядерки или мивинки) у пользователя.

        Args:
            user_id (int): айди пользователя
            weapon_type (str): тип оружия ("bomb" или "mivina")

        Returns:
            int | None: айди самой старой записи или None, если записи нет
        """
        if weapon_type not in ["bomb", "mivina"]:
            raise ValueError("Некорректный тип лога")

        async with self.session() as session:
            async with session.begin():
                stmt = (
                    select(NuclearLogs.id)
                    .where(NuclearLogs.user_id == user_id, NuclearLogs.used == 0, NuclearLogs.log_type == weapon_type)
                    .order_by(NuclearLogs.date.asc())
                    .limit(1)
                )
                oldest_log_id = await session.scalar(stmt)
                await session.aclose()

        return oldest_log_id


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
                last_time_str = await session.scalar(stmt)
                await session.aclose()

        if not last_time_str:
            return False

        last_time = pendulum.parse(last_time_str)
        days_since_received = (pendulum.now() - last_time).days

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

    async def update_log_used(self, weapon_id: int) -> None:
        """Обновляет запись в логе, помечая оружие как использованную.

        Args:
            log_id (int): айди записи в NuclearLogs
        """
        async with self.session() as session:
            async with session.begin():
                stmt = update(NuclearLogs).where(NuclearLogs.id == weapon_id).values(used=True)
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

        num_nuc_start = str(await self.get_start_count(user.id, "bomb_start_count"))
        num_miv_start = str(await self.get_start_count(user.id, "mivina_start_count"))
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
