import random
from io import BytesIO

import hikari
import pendulum
from PIL import Image, ImageDraw, ImageFont

from database.database_manager import DatabaseManager

database_manager = DatabaseManager()

# -----------------------------------------------------------------------------------------------------------Bombs>
async def get_bomb_count(user_id: int) -> int:
    """Получение количество ядерки и пользователя

    Args:
        user_id (int): айди пользователя

    Returns:
        int: количество ядерок
    """
        # Попытка получить текущее значение bomb_count
    result = await database_manager.fetchone("SELECT COUNT(*) FROM bomb_logs WHERE user_id = ? AND used = 0", (user_id,))

    # Возвращаем количество записей
    return result[0] if result else 0


async def check_bomb_cooldown(user_id: int) -> bool:
    """Проверка кулдауна для получения ядерки. Кулдаун в 1 день

    Args:
        user_id (int): айди пользователя

    Returns:
        bool: True
    """
    row = await database_manager.fetchone("SELECT bomb_cd FROM nuclear_data WHERE user_id = ?", (user_id,))

    # Если существует запись - проверяем КД
    if row is not None:
        current_time = pendulum.now().strftime("%Y-%m-%d")

        if current_time > row[0]:
            return True
        else:
            return False
    # Если запись отсутствует - возвращаем True
    else:
        return True


async def update_bomb_cooldown(user_id: int) -> None:
    """Обновляет кулдаун ядерки у пользователя

    Args:
        user_id (int): айди пользователя
    """
    current_time = pendulum.now().strftime("%Y-%m-%d")

    # Проверяем, существует ли запись
    row = await database_manager.fetchone(
        "SELECT bomb_cd FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        # Обновляем значение, если запись существует
        await database_manager.execute(
            "UPDATE nuclear_data SET bomb_cd = ? WHERE user_id = ?",
            (current_time, user_id)
        )
    else:
        # Создаем новую запись, если её нет
        await database_manager.execute(
            "INSERT INTO nuclear_data (user_id, bomb_cd) VALUES (?, ?)",
            (user_id, current_time)
        )


async def get_bomb_start_count(user_id: int) -> int:
    """Получение количества запусков ядерок

    Args:
        user_id (int): айди пользователя

    Returns:
        int: количество запусков
    """
    row = await database_manager.fetchone(
        "SELECT bomb_start_count FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    # Если запись существует - возвращаем значение
    return row[0] if row else 0


async def update_bomb_start_count(user_id: int, count: int) -> None:
    """Обновление количества запусков ядерок у пользователя

    Args:
        user_id (int): айди пользователя
        count (int): количество запусков ядерок
    """
    row = await database_manager.fetchone(
        "SELECT bomb_start_count FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        # Если запись существует - обновляем значение
        await database_manager.execute(
            "UPDATE nuclear_data SET bomb_start_count = ? WHERE user_id = ?",
            (count, user_id)
        )
    else:
        # Если не существует запись - создаём новую запись
        await database_manager.execute(
            "INSERT INTO nuclear_data (user_id, bomb_start_count) VALUES (?, ?)",
            (user_id, count)
        )


async def wrote_bomb_log(user_id: int, user_name: str) -> None:
    """Запись в базу данных о новой полученной ядерке

    Args:
        user_id (int): айди пользователя
        user_name (str): ник пользователя
    """
    current_time = pendulum.now().strftime("%Y-%m-%d")
    await database_manager.execute(
        "INSERT INTO bomb_logs (user_id, username, date, used) VALUES (?, ?, ?, ?)",
        (user_id, user_name, current_time, 0)
    )


async def get_oldest_bomb_id(user_id: int) -> int:
    """Получение самой старой ядерки у пользователя

    Args:
        user_id (int): айди пользователя

    Returns:
        int: айди ядерки
    """
    row = await database_manager.fetchone(
        "SELECT id FROM bomb_logs WHERE user_id = ? AND used = 0 ORDER BY date ASC LIMIT 1",
        (user_id,)
    )
    return row[0] if row else 0


async def is_bomb_activated(bomb_id: int) -> bool:
    """Проверка запуститься ли ядерка

    Args:
        bomb_id (int): айди ядерки

    Returns:
        bool: True, если ядерка должна запуститься, иначе False
    """
    row = await database_manager.fetchone(
        "SELECT date FROM bomb_logs WHERE id = ?", (bomb_id,)
    )

    if not row:
        return False

    last_time_str = row[0]
    current_time = pendulum.now()
    last_time = pendulum.parse(last_time_str)

    days_since_received = (current_time - last_time).days
    return should_activate_nuke(days_since_received)


async def is_bomb_make_hirohito(bomb_id: int) -> bool:
    """Проверка взорвёт ли ядерка отправителя и получателя одновременно

    Args:
        bomb_id (int): айди ядерки

    Returns:
        bool: True, если взрыв возможен, иначе False
    """
    row = await database_manager.fetchone(
        "SELECT date FROM bomb_logs WHERE id = ?", (bomb_id,)
    )

    if not row:
        return False

    last_time_str = row[0]
    current_time = pendulum.now()
    last_time = pendulum.parse(last_time_str)

    days_since_received = (current_time - last_time).days
    return should_nuke_make_hirohito(days_since_received)


async def update_bomb_log(bomb_id: int) -> None:
    """Обновляет запись о конкретной ядерке, делая её использованной

    Args:
        bomb_id (int): айди ядерки
    """
    await database_manager.execute(
        "UPDATE bomb_logs SET used = 1 WHERE id = ?", (bomb_id,)
    )


async def reset_bombs(user_id: int) -> None:
    """Сброс ядерок у пользователя

    Args:
        user_id (int): айди пользователя
    """
    await database_manager.execute(
        "UPDATE bomb_logs SET used = 1 WHERE user_id = ?", (user_id,)
    )

# ---------------------------------------------------------------------------------------------------------------------Mivina>
async def get_mivina_count(user_id: int) -> int:
    """Получение количество мивинок у пользователя

    Args:
        user_id (int): айди пользователя

    Returns:
        int: количество мивинок
    """
    row = await database_manager.fetchone(
        "SELECT COUNT(*) FROM mivina_logs WHERE user_id = ? AND used = 0", (user_id,)
    )
    return row[0] if row else 0


async def check_mivina_cooldown(user_id: int) -> bool:
    """Проверка кулдауна для получения мивинок. Кулдаун в 1 день

    Args:
        user_id (int): айди пользователя

    Returns:
        bool: True, если кулдаун прошел, иначе False
    """
    row = await database_manager.fetchone(
        "SELECT mivina_cd FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        last_time = row[0]
        current_time = pendulum.now().strftime("%Y-%m-%d")
        return current_time > last_time

    # Если запись отсутствует - возвращаем True (кулдаун прошел)
    return True


async def update_mivina_cooldown(user_id: int) -> None:
    """Обновление кулдауна мивинки у пользователя

    Args:
        user_id (int): айди пользователя
    """
    current_time = pendulum.now().strftime("%Y-%m-%d")

    row = await database_manager.fetchone(
        "SELECT mivina_cd FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        await database_manager.execute(
            "UPDATE nuclear_data SET mivina_cd = ? WHERE user_id = ?", (current_time, user_id)
        )
    else:
        await database_manager.execute(
            "INSERT INTO nuclear_data (user_id, mivina_cd) VALUES (?, ?)", (user_id, current_time)
        )


async def get_mivina_start_count(user_id: int) -> int:
    """Получение количества использований мивинки

    Args:
        user_id (int): айди пользователя

    Returns:
        int: количество использований
    """
    row = await database_manager.fetchone(
        "SELECT mivina_start_count FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    return row[0] if row else 0


async def update_mivina_start_count(user_id: int, count: int) -> None:
    """Обновление количества использования мивинок у пользователя

    Args:
        user_id (int): айди пользователя
        count (int): количество использований мивинок
    """
    row = await database_manager.fetchone(
        "SELECT mivina_start_count FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        await database_manager.execute(
            "UPDATE nuclear_data SET mivina_start_count = ? WHERE user_id = ?", (count, user_id)
        )
    else:
        await database_manager.execute(
            "INSERT INTO nuclear_data (user_id, mivina_start_count) VALUES (?, ?)", (user_id, count)
        )


async def wrote_mivina_log(user_id: int, user_name: str) -> None:
    """Запись в базу данных о новой полученной мивинке

    Args:
        user_id (int): айди пользователя
        user_name (str): ник пользователя
    """
    current_time = pendulum.now().strftime("%Y-%m-%d")
    await database_manager.execute(
        "INSERT INTO mivina_Logs (user_id, username, date, used) VALUES (?, ?, ?, ?)",
        (user_id, user_name, current_time, 0)
    )


async def get_oldest_mivina_id(user_id: int) -> int:
    """Получение самой старой мивинки у пользователя

    Args:
        user_id (int): айди пользователя

    Returns:
        int: айди мивинки
    """
    rows = await database_manager.fetchall(
        "SELECT id FROM mivina_Logs WHERE user_id = ? AND used = 0",
        (user_id,)
    )
    return rows[0][0] if rows else None


async def is_mivina_activated(mivina_id: int) -> bool:
    """Проверка запуститься ли мивинка

    Args:
        bomb_id (int): айди ядерки

    Returns:
        bool: True
    """
    query = "SELECT date FROM mivina_Logs WHERE id = ?"
    row = await database_manager.fetchone(query, (mivina_id,))

    if row:
        last_time_str = row[0]
        current_time = pendulum.now()
        last_time = pendulum.parse(last_time_str)

        days_since_received = (current_time - last_time).days

        if should_activate_nuke(days_since_received):
            return True
    return False


async def update_mivina_log(mivina_id: int) -> None:
    """Обновляет запись о конкретной мивинки, делая её использованной

    Args:
        bomb_id (int): айди мивинки
    """
    query = "UPDATE mivina_Logs SET used = 1 WHERE id = ?"
    await database_manager.execute(query, (mivina_id,))
# --------------------------------------------------------------------------------------------------------------------- User>
async def get_nuclear_mode(user_id: int) -> bool:
    """Получение ядерного режима пользователя

    Args:
        user_id (int): айди пользователя

    Returns:
        bool: True
    """
    row = await database_manager.fetchone("SELECT nuclear_mode FROM nuclear_data WHERE user_id = ?", (user_id,))

    if row is not None:
        return row[0] == 1
    return False


async def update_nuclear_mode(user_id: int, mode: int) -> None:
    """Обновляет ядерный режим пользователя

    Args:
        user_id (int): айди пользователя
        mode (int): режим, где 1 = True и 0 = False
    """
    # Попытка получить текущее значение nuclear_mode
    row = await database_manager.fetchone(
        "SELECT nuclear_mode FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        # Если запись существует - обновляем значение
        await database_manager.execute(
            "UPDATE nuclear_data SET nuclear_mode = ? WHERE user_id = ?",
            (mode, user_id)
        )
    else:
        # Если не существует запись - создаём новую запись
        await database_manager.execute(
            "INSERT INTO nuclear_data (user_id, nuclear_mode) VALUES (?, ?)",
            (user_id, mode)
        )


async def get_new_user(user_id: int) -> bool:
    """Получение значения new_user. Если отсутствует запись, то возвращает True

    Args:
        user_id (int): айди пользователя

    Returns:
        bool: True
    """
    # Попытка получить текущее значение new_user
    row = await database_manager.fetchone(
        "SELECT new_user FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row is not None:
        # Если запись существует - возвращаем значение
        return row[0] == 1
    else:
        # Если не существует запись - возвращаем значение по умолчанию
        return True


async def set_new_user(user_id: int, mode: bool) -> None:
    """Устанавливает значение new_user

    Args:
        user_id (int): айди пользователя
        mode (bool): режим, где True = 1 и False = 0
    """
    # Попытка получить текущее значение new_user
    row = await database_manager.fetchone(
        "SELECT new_user FROM nuclear_data WHERE user_id = ?", (user_id,)
    )

    if row:
        # Если запись существует - обновляем значение
        await database_manager.execute(
            "UPDATE nuclear_data SET new_user = ? WHERE user_id = ?",
            (mode, user_id)
        )
    else:
        # Если не существует запись - создаём новую запись
        await database_manager.execute(
            "INSERT INTO nuclear_data (user_id, new_user) VALUES (?, ?)",
            (user_id, mode)
        )

# ------------------------------------------------------> Help

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


async def generate_arsenal(user: hikari.User) -> str:
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

    num_nuc = str(await get_bomb_count(user.id))
    num_miv = str(await get_mivina_count(user.id))
    idraw.text((293, 150), num_nuc, font=num_font, fill=(0, 0, 0))
    idraw.text((1285, 150), num_miv, font=num_font, fill=(0, 0, 0))

    num_nuc_start = str(await get_bomb_start_count(user.id))
    num_miv_start = str(await get_mivina_start_count(user.id))
    idraw.text((319, 290), num_nuc_start, font=num_font, fill=(0, 0, 0))
    idraw.text((1293, 290), num_miv_start, font=num_font, fill=(0, 0, 0))
    wallpaper.save("profileTemp.png")

    return "profileTemp.png"
