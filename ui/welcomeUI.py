import hikari
import miru

from utils.create_embed import create_embed
from ui.profileUI import EditProfileButton
from typing import Optional


role_color_mapping = {
    "Красный": 1106244113587785829,
    "Оранжевый": 1106244211138887780,
    "Жёлтый": 1106244235411345408,
    "Зелёный": 1106244181602603038,
    "Синий": 1106244160958255225,
    "Голубой": 1124257706321125439,
    "Розовый": 1121558196046270466,
    "Фиолетовый": 1106250927805042708,
    "Серый": 1135230107095662602,
    "Белый": 1135231008413855795,
}

class MainView(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(timeout=None, *args, **kwargs)

    @miru.text_select(
        placeholder="📚 ┋ Правила участника сервера",
        options=[
            miru.SelectOption(label="Общие положения", emoji="📱"),
            miru.SelectOption(label="Размещение ссылок", emoji="🖥️"),
            miru.SelectOption(label="Голосовой чат", emoji="🎤"),
            miru.SelectOption(label="Ники", emoji="🏷️"),
            miru.SelectOption(label="Приватные каналы", emoji="⛔"),
        ], min_values=1, max_values=1, custom_id="rules_select_menu")
    async def rules_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        selected_option = select.values[0]
        embedRules = hikari.Embed()

        if selected_option == "Общие положения":
            embedRules = create_embed(
                title="🎉__Общие положения сообщества__",
                description="\
╔════════════════ ❀•°❀°•❀ ════════════════╗\n\n\
1️⃣ **Уважайте других пользователей.**\n\
2️⃣ **Запрещён любой NSFW контент.**\n\
3️⃣ **Запрещено злоупотребление Caps Lock** (кроме аббревиатур).\n\
4️⃣ **Запрещён любой тип флуда вне канала** #флудилка.\n\
5️⃣ **Дискуссии на политические, религиозные и подобные темы** \
проводите в ЛС.\n\
6️⃣ **Запрещена пропаганда алкоголя / наркотиков / курения.**\n\
7️⃣ **Запрещены террористическая символика, призывы к насилию \
и экстремизму.**\n\n\
╚════════════════ ❀•°❀°•❀ ════════════════╝",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png",
                )
            embedRules.set_footer("Пожалуйста, ознакомьтесь и соблюдайте данные правила для комфортного общения!")

        elif selected_option == "Размещение ссылок":
            embedRules = create_embed(
                title="📢__ **Ограничения на ссылки и рекламу:**__",
                description="\
╔════════════════ ❀•°❀°•❀ ════════════════╗\n\n\
1️⃣ **Запрещается реклама** без согласования с Jelly.\n\
2️⃣ **Запрещается публикация или распространение вирусных ссылок** и ссылок на торренты.\n\
3️⃣ **Запрещается публикация или распространение ссылок** на:\n\
- Площадки приема платежей\n\
- Сервисы для пожертвований\n\
- Спонсорскую помощь и прочее.\n\n\
╚════════════════ ❀•°❀°•❀ ════════════════╝",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )
            embedRules.set_footer("Пожалуйста, ознакомьтесь и соблюдайте данные правила для комфортного общения!")

        elif selected_option == "Голосовой чат":
            embedRules = create_embed(
                title="__Правила голосового чата__",
                description="\
╔════════════════ ❀•°❀°•❀ ════════════════╗\n\n\
1️⃣ **Избегайте громких звуков**: не издавайте резкие шумы в микрофон и не злоупотребляйте звуковой панелью.\n\
2️⃣ **Используйте Push-To-Talk**, если в вашем окружении много шума.\n\n\
🔊 Уважайте других участников, чтобы создать комфортную атмосферу для общения!\n\n\
╚════════════════ ❀•°❀°•❀ ════════════════╝",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )
            embedRules.set_footer("Пожалуйста, ознакомьтесь и соблюдайте данные правила для комфортного общения!")

        elif selected_option == "Ники":
            embedRules = create_embed(
                title="__Правила использования ников__",
                description="\
╔════════════════ ❀•°❀°•❀ ════════════════╗\n\n\
1️⃣ Если ваш ник невозможно отметить, он будет изменён администрацией.\n\
2️⃣ **На ники распространяются** Общие положения Правил сервера.\n\n\
💡 **Совет:** Убедитесь, что ваш ник легко читается и не нарушает общие правила!\n\n\
╚════════════════ ❀•°❀°•❀ ════════════════╝",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )
            embedRules.set_footer("Пожалуйста, ознакомьтесь и соблюдайте данные правила для комфортного общения!")

        elif selected_option == "Приватные каналы":
            embedRules = create_embed(
                title="__Правила приватных каналов__",
                description="\
╔════════════════ ❀•°❀°•❀ ════════════════╗\n\n\
1️⃣ Названия приватных каналов **не должны включать**:\n\
- Ссылки\n\
- Оскорбления\n\
- Рекламу\n\
- Пропаганду алкоголя, наркотиков или курения.\n\n\
⚠️ **Важно:** Содержание приватных каналов **не модерируется**, и жалобы на сообщения из них будут отклонены.\n\n\
╚════════════════ ❀•°❀°•❀ ════════════════╝",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )
            embedRules.set_footer("Пожалуйста, ознакомьтесь и соблюдайте данные правила для комфортного общения!")

        await ctx.respond(embed=embedRules, flags=hikari.MessageFlag.EPHEMERAL)

    @miru.text_select(
        placeholder="🛠️ ┋ Функционал сервера",
        options=[
            miru.SelectOption(label="Сладости", emoji="🥞"),
            miru.SelectOption(label="Кастомизация", emoji="🎨"),
        ], min_values=1, max_values=1, custom_id="functions_select_menu"
    )
    async def functions_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        selected_option = select.values[0]

        if selected_option == "Сладости":
            embedFunc = create_embed(
                color=0x313338,
                title="__Сладости__",
                description="На сервере есть 4 помощницы:\n\n🧡 **Мармеладка** 🧡\n\n🤍 **Зефирка** 🤍\n\n🤎 **Шокомелька** 🤎💜**Милка**💜\n\n__Узнай про каждую кнопками ниже!__",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

            sweet_view = SelectMainBots()

            await ctx.respond(embed=embedFunc, components=sweet_view, flags=hikari.MessageFlag.EPHEMERAL)

            ctx.client.start_view(sweet_view)

        elif selected_option == "Кастомизация":
            embedFunc = create_embed(
                color=0x313338,
                title="__Кастомизация__",
                description="Эта ветка посвящена всеееееей кастомизации!",
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

            color_view = SelectColor().add_item(EditProfileButton())

            await ctx.respond(embed=embedFunc, components=color_view, flags=hikari.MessageFlag.EPHEMERAL)

            ctx.client.start_view(color_view)


class SelectMainBots(miru.View):
    @miru.text_select(
        placeholder="🧁 ┋ Кого сейчас?",
        options=[
            miru.SelectOption(label="Мармеладка", emoji="🧡"),
            miru.SelectOption(label="Зефирка", emoji="🤍"),
            miru.SelectOption(label="Шокомелька", emoji="🤎"),
            miru.SelectOption(label="Милка", emoji="💜"),
            miru.SelectOption(label="Криска", emoji="🐀"),
        ], min_values=1, max_values=1, custom_id="bots_select_menu"
    )
    async def callback(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        selected_option = select.values[0]

        embedFunc = hikari.Embed()

        # Мармеладка
        if selected_option == "Мармеладка":
            embedFunc = create_embed(
                color=0xFFA500,
                title="__Мармеладка__",
                description="Самая главная Лисичка на этом сервере. Выполняет все главные функции сервера, даже тебе эту информацию предоставляет. Все о её командах можешь узнать через `/помощь`",
                image_url="https://c4.wallpaperflare.com/wallpaper/138/566/373/anime-girls-sewayaki-kitsune-no-senko-san-fox-girl-yellow-eyes-portrait-display-hd-wallpaper-preview.jpg"
            )

        # Зефирка
        elif selected_option == "Зефирка":
            embedFunc = create_embed(
                color=0xFFFFFF,
                title="__Зефирка__",
                description="По сюжету, шизофрения Мармеладки. Самый главный DJ сервера. Проиграет для тебя любую мелодию с популярных стриминговых площадок: Youtube Music, SoundCloud, Spotify, Apple Music.",
                image_url="https://preview.redd.it/shiro-san-rtx-on-v0-u7i864vg31sb1.png?auto=webp&s=6e07bf650a35f79eb4ea69d58af218c02c98cfb9"
            )

        # Шокомелька
        elif selected_option == "Шокомелька":
            embedFunc = create_embed(
                color=0x964B00,
                title="__Шокомелька__",
                description="Подружка Мармеладки и Зефирки(она тануки, то есть енот). По настроению сидит на своей требуне и проигрывает Lo-Fi музыку. Хочет принести гармонию в этот мир.",
                image_url="https://cdn.discordapp.com/attachments/1109526498299359303/1322581174727479327/EdL9VcH.png?ex=67716534&is=677013b4&hm=34ab50dd67868bac2be59eb4577392b178e03c3cd7921c8a5494a4f8ca434531&"
            )

        # Милка
        elif selected_option == "Милка":
            embedFunc = create_embed(
                color=0xA020F0,
                title="__Милка__",
                description="Если так посудить она самая главная Кицуне, но для неё осталась не такая главная задача. Она на пару с главным DJ - Зефирка, зажигает на сервере!",
                image_url="https://i.redd.it/what-are-your-thoughts-on-yozora-v0-62t00vvtr3nd1.jpg?width=1170&format=pjpg&auto=webp&s=43b4c815d4c9f24a03616c8146763f31c5eea752"
            )

        # Криска
        elif selected_option == "Криска":
            embedFunc = create_embed(
                color=0x808080,
                title="__Криска__",
                description="Это Криска, она тут недавно, но уже успела понравиться всем. Она умеет многое, но главное - она умеет быть с тобой в любой момент. Играет любую абсолютно музыку.",
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzQ2MWljY2VseW1ibTdkeHQwdGo1YTNqMG15cGNkaGpmZ25yMjYyYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eK12uCsrAh4wmTXejp/giphy.gif"
            )

        await ctx.respond(embed=embedFunc, flags=hikari.MessageFlag.EPHEMERAL)

class SelectColor(miru.View):
    def __init__(self):
        super().__init__(timeout=None)

    @miru.text_select(
        placeholder="🌈 ┋Выбирайте цвет",
        options=[
            miru.SelectOption(label="Красный", emoji="❤️"),
            miru.SelectOption(label="Оранжевый", emoji="🧡"),
            miru.SelectOption(label="Жёлтый", emoji="💛"),
            miru.SelectOption(label="Зелёный", emoji="💚"),
            miru.SelectOption(label="Синий", emoji="💙"),
            miru.SelectOption(label="Голубой", emoji="💙"),
            miru.SelectOption(label="Розовый", emoji="💗"),
            miru.SelectOption(label="Фиолетовый", emoji="💜"),
            miru.SelectOption(label="Серый", emoji="🖤"),
            miru.SelectOption(label="Белый", emoji="🤍"),
            miru.SelectOption(label="Убрать", emoji="💟"),
        ], min_values=1, max_values=1, custom_id="color_select_menu")

    async def basic_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        selected_option = select.values[0]

        member_id = ctx.author.id
        guild = ctx.get_guild()
        if guild is None:
            return
        member = guild.get_member(member_id)
        if member is None:
            return

        if selected_option == "Убрать":
            await update_member_role(member, role_color_mapping, None)
            await ctx.respond("Вы убрали у себя цвет", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            role_id = role_color_mapping.get(selected_option)
            if role_id:
                await update_member_role(member, role_color_mapping, role_id)
                await ctx.respond(f"Вы поменяли цвет своего ника на {selected_option}", flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond("Неверная опция", flags=hikari.MessageFlag.EPHEMERAL)
            return

    async def on_error(
        self,
        error: Exception,
        item: miru.abc.ViewItem | None = None,
        ctx: miru.ViewContext | None = None
    ) -> None:
        if ctx is not None:
            await ctx.respond(f"Oh no! This error occured: {error}", flags=hikari.MessageFlag.EPHEMERAL)


async def update_member_role(member: hikari.Member, role_ids, new_role_id: Optional[int] = None) -> None:
    """Update users color roles

    Args:
        member (disnake.Member): Member object to change
        new_role_id (disnake.Role): Role color object, which need to add
        role_ids (List): Member roles ids
    """
    member_roles = member.get_roles()
    current_role_ids = [role.id for role in member_roles if role.id in role_ids.values()]

    if current_role_ids:
        await member.remove_role(*[role for role in member_roles if role.id in current_role_ids])

    if new_role_id:
        guild = member.get_guild()
        if guild is None:
            return
        new_role = guild.get_role(new_role_id)
        if new_role is None:
            return

        await member.add_role(new_role)
