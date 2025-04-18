import logging
import json

import hikari
import miru
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.database_manager import DatabaseManager
from database.models import UserData
from functions.user_profile_func import UserProfileFunc

logger = logging.getLogger(__name__)

class EditProfileButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Edit profile")
        self.value = True
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=False)

    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(modal=EditProfile())

class EditProfile(miru.Modal, title="Edit profile"):
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        self.session = async_sessionmaker(self.db_manager.engine, expire_on_commit=True)
    tag = miru.TextInput(
        label="tag",
        style=hikari.TextInputStyle.SHORT,
        placeholder="type your tag",
        custom_id="tag_input",
        required=False,
        max_length=20
    )

    bio = miru.TextInput(
        label="Biography",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Type your biography",
        custom_id="bio_input",
        required=False,
    )

    birth = miru.TextInput(
        label="Your Birthday, format mm-dd(07-31)",
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

        user_language = await UserProfileFunc().get_lang(user_id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

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


            await ctx.respond(language_json["edit_profile_callback"]["success"], flags=hikari.MessageFlag.EPHEMERAL)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await ctx.respond(language_json["edit_profile_callback"]["error"], flags=hikari.MessageFlag.EPHEMERAL)
