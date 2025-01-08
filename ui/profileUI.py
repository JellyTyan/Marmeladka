import miru
import hikari

from database.database_manager import DatabaseManager

database_manager = DatabaseManager()

class EditProfileButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Редактировать профиль")
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(modal=EditProfile())

class EditProfile(miru.Modal, title="Редактировать профиль"):
    tag = miru.TextInput(
        label="Тэг",
        style=hikari.TextInputStyle.SHORT,
        placeholder="Введите желаемый тэг",
        custom_id="tag_input",
        required=False,
        max_length=20
    )

    bio = miru.TextInput(
        label="Биография",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Введите биографию",
        custom_id="bio_input",
        required=False,
    )

    birth = miru.TextInput(
        label="Дата рождения, формат mm-dd(07-31)",
        style=hikari.TextInputStyle.SHORT,
        placeholder="07-31",
        custom_id="birth_input",
        required=False,
        max_length=5,
        min_length=5,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        user_id = ctx.author.id
        tag = self.tag.value
        bio = self.bio.value
        birth = self.birth.value

        print(f"User ID: {user_id}, Tag: {tag}, Bio: {bio}, Birth: {birth}")

        try:
            result = await database_manager.fetchone(
                "SELECT tag, biography, birthday_date FROM user_data WHERE id = ?", (user_id,)
            )

            current_tag, current_bio, current_birth = result if result else (None, None, None)

            new_tag = tag if tag else current_tag
            new_bio = bio if bio else current_bio
            new_birth = birth if birth else current_birth

            if result:
                await database_manager.execute(
                    """
                    UPDATE user_data
                    SET tag = ?, biography = ?, birthday_date = ?
                    WHERE id = ?
                    """,
                    (new_tag, new_bio, new_birth, user_id),
                )
            else:
                await database_manager.execute(
                    """
                    INSERT INTO user_data (id, tag, biography, birthday_date)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, new_tag, new_bio, new_birth),
                )

            await ctx.respond("Профиль успешно отредактирован!", flags=hikari.MessageFlag.EPHEMERAL)
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.respond("Произошла ошибка при редактировании профиля!", flags=hikari.MessageFlag.EPHEMERAL)
