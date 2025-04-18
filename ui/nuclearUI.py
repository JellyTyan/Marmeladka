import json
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher

import hikari
import miru

from functions.nuclear_func import NuclearFunc
from functions.user_profile_func import UserProfileFunc
from utils.create_embed import create_embed
from utils.get_random_gif import get_random_gif

nuclear_func = NuclearFunc()

cooldowns = {}


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class NuclearCase(miru.Modal, title="Enter the code phrase, and the arsenal will appear in the case"):
    codeword = miru.TextInput(
        label="What should be written here?",
        style=hikari.TextInputStyle.SHORT,
        placeholder="Enter the code word",
        custom_id="codeword",
        required=True,
        max_length=30,
    )

    async def callback(self, ctx: miru.ModalContext):
        codeword = str(self.codeword.value)
        user_id = ctx.author.id


        # Получения языка пользователя
        user_language = await UserProfileFunc().get_lang(user_id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        # Ключевая фраза
        target_phrase_bomb = language_json["nuclear_ui"]["nuclear_code_phrase"]
        target_phrase_mivina = language_json["nuclear_ui"]["mivina_code_phrase"]

        # Порог схожести, при котором считаем, что фразы идентичны
        similarity_threshold = 0.8

        # Сравниваем сообщение с ключевой фразой
        if similar(codeword.lower(), target_phrase_bomb.lower()) > similarity_threshold:
            nuclear_mode = await nuclear_func.get_nuclear_mode(user_id)
            if nuclear_mode == 0:
                embedDecline = create_embed(description=language_json["nuclear_ui"]["nuclear_mode_off"])
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return

            # Проверяем КД
            if await nuclear_func.check_cooldown(user_id, "bomb_cd"):
                # Увеличиваем количество пультов и обновляем количевство в БД
                await nuclear_func.update_cooldown(user_id, "bomb_cd")
                await nuclear_func.wrote_log(user_id, ctx.author.username, "bomb")

                # Уведомляем о успешном обновлении кол-во и чистим сообщения

                embedSuccesed = create_embed(description=language_json["nuclear_ui"]["bomb_success"])
                await ctx.respond(embed=embedSuccesed, flags=hikari.MessageFlag.EPHEMERAL)

                # self.bot.dispatch("bomb_given", inter.author)

                return
            else:
                # Уведомляем, что пользователь должен подождать и чистим сообщения
                embedDecline = create_embed(description=language_json["nuclear_ui"]["bomb_cooldown"])
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return

        # Пользователь хочет получить мивину
        elif (similar(codeword.lower(), target_phrase_mivina.lower()) > similarity_threshold):
            nuclear_mode = await nuclear_func.get_nuclear_mode(user_id)
            if nuclear_mode == 0:
                embedDecline = create_embed(description=language_json["nuclear_ui"]["nuclear_mode_off"])
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return

            # Проверяем КД
            if await nuclear_func.check_cooldown(user_id, "mivina_cd"):
                # Обновляем КД

                # Увеличиваем количество мивинок и обновляем БД
                await nuclear_func.update_cooldown(user_id, "mivina_cd")
                await nuclear_func.wrote_log(user_id, ctx.author.username, "mivina")

                # Уведомляем о успешком обновление кол-во и чистим сообщения
                embedSuccesed = create_embed(description=language_json["nuclear_ui"]["mivina_success"])
                await ctx.respond(embed=embedSuccesed, flags=hikari.MessageFlag.EPHEMERAL)

                # self.bot.dispatch("mivina_given", inter.author)
                return
            else:
                # Уведомляем, что пользователь должен подождать и чистим сообщения
                embedDecline = create_embed(description=language_json["nuclear_ui"]["mivina_cooldown"])
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return
        else:
            guild = ctx.get_guild()
            if guild is None:
                return
            await ctx.client.rest.edit_member(guild.id, ctx.author, communication_disabled_until=datetime.now(timezone.utc) + timedelta(seconds=15), reason="Loh")
            embedDecline = create_embed(description=language_json["nuclear_ui"]["wrong_codeword"])
            await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
            return


class TurnOnNuclear(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.SUCCESS,
            label="Turn ON",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.user.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)
        await nuclear_func.update_nuclear_mode(ctx.author.id, True)
        await ctx.respond(language_json["nuclear_ui"]["nuclear_mode_enabled"], flags=hikari.MessageFlag.EPHEMERAL)
        self.view.stop()


class TurnOffNuclear(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.DANGER,
            label="Turn OFF",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        user_id = ctx.user.id
        now = datetime.now()
        cooldown = 12 * 60 * 60

        user_language = await UserProfileFunc().get_lang(user_id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        last_used = cooldowns.get(user_id, 0)
        if now - last_used < cooldown:
            remaining = int(cooldown - (now - last_used))
            hours, minutes = divmod(remaining // 60, 60)
            await ctx.respond((language_json["nuclear_ui"]["nuclear_mode_disable_prompt"]).format(hours,minutes), flags=hikari.MessageFlag.EPHEMERAL)
            return

        cooldowns[user_id] = now

        view = miru.View()
        view.add_item(AcceptButton())

        embed = create_embed(
            title=language_json["nuclear_ui"]["nuclear_mode_disable_confirm"],
            description=language_json["nuclear_ui"]["nuclear_mode_disable_desc"]
        )

        await ctx.respond(embed=embed, components=view, flags=hikari.MessageFlag.EPHEMERAL)
        ctx.client.start_view(view)

class AcceptButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.SUCCESS,
            label="Confirm",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.user.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)
        await nuclear_func.update_nuclear_mode(ctx.author.id, False)
        await nuclear_func.reset_bombs(ctx.author.id)
        await ctx.respond(language_json["nuclear_ui"]["nuclear_mode_disabled"], flags=hikari.MessageFlag.EPHEMERAL)
        self.view.stop()


class SelfBombActivate(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.DANGER,
            label="Are you sure?",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.author.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)
        oldest_bomb_id = await nuclear_func.get_oldest_weapon_id(ctx.author.id, "bomb")
        if oldest_bomb_id is None:
            return
        guild = ctx.get_guild()
        if guild is None:
            return

        if await nuclear_func.is_weapon_activated(oldest_bomb_id):
            await ctx.client.rest.edit_member(guild, ctx.author, communication_disabled_until=datetime.now(timezone.utc) + timedelta(seconds=300), reason="bomb")
            embed = create_embed(
                description=(language_json["nuclear_ui"]["self_bomb_success"]).format(user_mention = ctx.author.mention),
                image_url=get_random_gif("bomb_self")
            )
            await nuclear_func.update_log_used(oldest_bomb_id)
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.NONE)
            return
        else:
            embed = create_embed(
                description=language_json["nuclear_ui"]["self_bomb_failed"],
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDFlNTZoYXNjM21ta2FrbTZoN3E3MjNkMnhraGxhazJtaW42NjJ0ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkf7qxSEUqNCataNjK/giphy.gif"
            )
            await nuclear_func.update_log_used(oldest_bomb_id)
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.NONE)
            return
        self.view.stop()
