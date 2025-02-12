from difflib import SequenceMatcher

import miru
import hikari

from datetime import datetime, timedelta, timezone

from functions.nuclear_func import NuclearFunc
from utils.create_embed import create_embed
from utils.get_random_gif import get_random_gif

nuclear_func = NuclearFunc()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class NuclearCase(miru.Modal, title="Впиши код-фразу и в кейсе появится арсенал"):
    codeword = miru.TextInput(
        label="Что же сюда написать?",
        style=hikari.TextInputStyle.SHORT,
        placeholder="Введите кодовое слово",
        custom_id="codeword",
        required=True,
        max_length=30,
    )

    async def callback(self, ctx: miru.ModalContext):
        codeword = str(self.codeword.value)
        user_id = ctx.author.id

        # Ключевая фраза
        target_phrase_bomb = "дайте мне пульт от ядерки"
        target_phrase_mivina = "дайте мне мивинку"

        # Порог схожести, при котором считаем, что фразы идентичны
        similarity_threshold = 0.8

        # Сравниваем сообщение с ключевой фразой
        if similar(codeword.lower(), target_phrase_bomb.lower()) > similarity_threshold:
            nuclear_mode = await nuclear_func.get_nuclear_mode(user_id)
            if nuclear_mode == 0:
                embedDecline = create_embed(
                    description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы ввели кодовое слово, но кейс превратился в слово 'Отклонено'. Кажется стоит включить ядерный режим..."
                )
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return

            # Проверяем КД
            if await nuclear_func.check_bomb_cooldown(user_id):
                # Увеличиваем количество пультов и обновляем количевство в БД
                await nuclear_func.update_bomb_cooldown(user_id)
                await nuclear_func.wrote_bomb_log(user_id, ctx.author.username)

                # Уведомляем о успешном обновлении кол-во и чистим сообщения

                embedSuccesed = create_embed(
                    description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы вписали кодовое слово и кейс открылся. Внутри вы увидели ядерку. Вы забираете её себе.\n\n `+1 ядерка в арсенал`"
                )
                await ctx.respond(embed=embedSuccesed, flags=hikari.MessageFlag.EPHEMERAL)

                # self.bot.dispatch("bomb_given", inter.author)

                return
            else:
                # Уведомляем, что пользователь должен подождать и чистим сообщения
                embedDecline = create_embed(
                    description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы ввели кодовое слово и кейс открылся. Внутри было пусто. Кажется стоит прийти завтра за новым вооружением..."
                )
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return

        # Пользователь хочет получить мивину
        elif (similar(codeword.lower(), target_phrase_mivina.lower()) > similarity_threshold):
            nuclear_mode = await nuclear_func.get_nuclear_mode(user_id)
            if nuclear_mode == 0:
                embedDecline = create_embed(
                    description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы ввели кодовое слово, но кейс превратился в слово 'Отклонено'. Кажется стоит включить ядерный режим..."
                )
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return

            # Проверяем КД
            if await nuclear_func.check_mivina_cooldown(user_id):
                # Обновляем КД

                # Увеличиваем количество мивинок и обновляем БД
                await nuclear_func.update_mivina_cooldown(user_id)
                await nuclear_func.wrote_mivina_log(user_id, ctx.author.username)

                # Уведомляем о успешком обновление кол-во и чистим сообщения
                embedSuccesed = create_embed(
                    description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы вписали кодовое слово и кейс открылся. Внутри вы увидели мивинку. Вы забираете её себе.\n\n `+1 мивинка в арсенал`"
                )
                await ctx.respond(embed=embedSuccesed, flags=hikari.MessageFlag.EPHEMERAL)

                # self.bot.dispatch("mivina_given", inter.author)
                return
            else:
                # Уведомляем, что пользователь должен подождать и чистим сообщения
                embedDecline = create_embed(
                    description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы ввели кодовое слово и кейс открылся. Внутри было пусто. Кажется стоит прийти завтра за новым вооружением..."
                )
                await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
                return
        else:
            guild = ctx.get_guild()
            if guild is None:
                return
            await ctx.client.rest.edit_member(guild.id, ctx.author, communication_disabled_until=datetime.now(timezone.utc) + timedelta(seconds=15), reason="Loh")
            embedDecline = create_embed(
                description="Вы увидели перед собой кейс. На нём было написано: 'Впиши код-фразу и в кейсе появится арсенал'.\n\nВы ввели неверное слово. Кейс закрылся и вы отклонились."
            )
            await ctx.respond(embed=embedDecline, flags=hikari.MessageFlag.EPHEMERAL)
            return


class TurnOnNuclear(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.SUCCESS,
            label="Включить",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        await nuclear_func.update_nuclear_mode(ctx.author.id, 1)
        await ctx.respond("Ядерный режим включён!", flags=hikari.MessageFlag.EPHEMERAL)
        self.view.stop()


class TurnOffNuclear(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.DANGER,
            label="Выключить",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        view = miru.View()
        view.add_item(AcceptButton())

        embed = create_embed(
            title="Отключение Ядерного Режима",
            description='Вы уверены, что хотите отключить ядерный режим? В таком случае вы объявляете разоружение и больше не вправе иметь доступ к системе Ядерка! Вы "аптека!"'
        )

        await ctx.respond(embed=embed, components=view, flags=hikari.MessageFlag.EPHEMERAL)

        ctx.client.start_view(view)

class AcceptButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.SUCCESS,
            label="Согласен",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        await nuclear_func.update_nuclear_mode(ctx.author.id, 0)
        await nuclear_func.reset_bombs(ctx.author.id)
        await ctx.respond("Спасибо за пользование системой Ядерка. Мы ждём вашего возвращения, Генерал!", flags=hikari.MessageFlag.EPHEMERAL)
        self.view.stop()


class SelfBombActivate(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.DANGER,
            label="Вы уверены?",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        oldest_bomb_id = await nuclear_func.get_oldest_bomb_id(ctx.author.id)
        guild = ctx.get_guild()
        if guild is None:
            return

        if await nuclear_func.is_bomb_activated(oldest_bomb_id):
            await ctx.client.rest.edit_member(guild, ctx.author, communication_disabled_until=datetime.now(timezone.utc) + timedelta(seconds=300), reason="bomb")
            embed = create_embed(
                description=f"Ладно...\n{ctx.author.mention}\n**У тебя прилёт от**\n{ctx.author.mention}",
                image_url=get_random_gif("bomb_self")
            )
            await nuclear_func.update_bomb_log(oldest_bomb_id)
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.NONE)
            return
        else:
            embed = create_embed(
                description="Упс. Ядерка не сработала. Кажется она слишком старая.",
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDFlNTZoYXNjM21ta2FrbTZoN3E3MjNkMnhraGxhazJtaW42NjJ0ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkf7qxSEUqNCataNjK/giphy.gif"
            )
            await nuclear_func.update_bomb_log(oldest_bomb_id)
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.NONE)
            return
        self.view.stop()
