import miru
import hikari

from database.database_manager import DatabaseManager, UserData
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

class EditProfileButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Редактировать профиль")
        self.value = True
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=False)

    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(modal=EditProfile())

class EditProfile(miru.Modal, title="Редактировать профиль"):
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=True)
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

        try:
            async with self.session() as session:
                user = select(UserData).where(UserData.user_id == user_id)
                user = await session.scalars(user)
                user = user.first()

                if user is None:
                    return

                user.tag = tag or user.tag
                user.biography = bio or user.biography
                user.birthday_date = birth or user.birthday_date

                await session.commit()

            await ctx.respond("Профиль успешно отредактирован!", flags=hikari.MessageFlag.EPHEMERAL)
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.respond("Произошла ошибка при редактировании профиля!", flags=hikari.MessageFlag.EPHEMERAL)
