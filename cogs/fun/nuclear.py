import os
import pendulum

import lightbulb
import hikari
import miru
from miru.ext import nav

import functions.nuclear_func as nuclearFunc
from config.config_manager import ConfigManager
from ui.nuclearUI import NuclearCase, TurnOnNuclear, TurnOffNuclear, SelfBombActivate
from database.database_manager import DatabaseManager
from utils.create_embed import create_embed
from utils.get_random_gif import get_random_gif

last_switch_call = {}

plugin = lightbulb.Plugin("PluginName")

database_manager = DatabaseManager()
config_manager = ConfigManager()


@plugin.listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    # При присоединении пользователя создавать запись в БД
    await database_manager.execute("INSERT INTO nuclear_data (user_id, username, new_user) VALUES (?, ?, ?)",(event.user_id, event.user.username, True),)

@plugin.listener(hikari.MemberDeleteEvent)
async def on_member_remove(event: hikari.MemberDeleteEvent):
    # Если новый пользователь вышел с сервера, то удалять запись с ним в БД
    check_new = await nuclearFunc.get_new_user(event.user_id)
    if check_new is True:
        await database_manager.execute("DELETE FROM nuclear_data WHERE user_id = ?", (event.user_id, ))

# @commands.Cog.listener()
# async def on_member_update(self, before: disnake.Member, after: disnake.Member):
#     try:
#         if after.current_timeout is None:
#             nuclear_role = after.guild.get_role(NUCLEAR_ROLE)
#             await after.remove_roles(nuclear_role)
#     except Exception:
#         return


@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("суицид", "Press F.", app_command_dm_enabled=False, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def suicide(ctx: lightbulb.SlashContext):
    try:
        guild = ctx.get_guild()
        if guild is None:
            return
        await ctx.app.rest.edit_member(guild, ctx.author, communication_disabled_until=pendulum.now("UTC").add(minutes=1), reason="Suicide")

        embed = create_embed(
            description=f"{ctx.author.mention} суициднулся. Press F",
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTZuaTZmczRuZ2ltM2tiemZibTZlamo0ODdqMTRjejUyNzAzZnpxeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eHR8NnClhVMwgRIAwb/giphy-downsized.gif",
            color=0x313338
        )
        await ctx.respond(embed=embed)
    except Exception as e:
        await ctx.respond("Простите, вы не смогли самоубиться...")
        print(e)


@plugin.command
@lightbulb.add_cooldown(1, 5, lightbulb.UserBucket)
@lightbulb.command("арсенал", "Ядерки, Мивинки - тебе это нужно?", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def arsenal(ctx: lightbulb.SlashContext):
    user = ctx.author
    miru_client: miru.Client = ctx.bot.d.miru

    # Если пользователь новый, то отправляем вспомонательный эмбед
    check_result = await nuclearFunc.get_new_user(user.id)
    if check_result is True:
        embedNewUser_1 = create_embed(
            title="Приветствуем новичка в системе Ядерок!",
            description="Ядерка - это уникальная разработка в Discord. Ядерка - это не будущее, это настоящее. Ваш разговор зашёл в тупик? Запусти ядерку! Он не сможет ничего делать в течении 5-и минут! Только готовься в сию же секунду получить ответку. \n ДА НАЧНЁТСЯ ЖЕ ЯДЕРНАЯ ВОЙНА!",
            image_url="https://cdn.discordapp.com/attachments/1149398121110057088/1197523129187188816/nuclear-weapons-earth-0308221.png?ex=65bb9352&is=65a91e52&hm=b44b59d17423f2a75659eb7746f9f8663fc489e3c0e8f60f8b90828385d390bf&",
            color=0x313338
        )

        embedNewUser_2 = create_embed(
            title="Приветствуем новичка в системе Ядерок!",
            description="А теперь я расскажу как ей пользоваться. \n Тебе нужно запомнить 2 фразы ```Дайте мне пульт от ядерки``` и ```Дайте мне мивинку```\n С ними я понимаю, что тебе требуется арсенал. \n Получать арсенал ты можешь один раз в день. \nЧтобы попросить арсенал воспользуйся командой ```/кейс```\n\n Теперь ты получил ядерку или мивинку. В твоём распоряжении кнопка запуска и аптечка. \n По нажатию **кнопки запуска** (команда)```/ядерка *пользователь*``` ты отправляешь ядерку на свою цель. \n **Мивинка** тебе нужна, чтобы подлечится, если вдруг на тебя попала ядерка. Для этого тебе нужно попросить меня тебя подлечить (В ЛС со мной)```/мивинка```\n Ядерку ты не сможешь запустить на Сладостей и остальных ботов. \nНу же! Получи свою первую Ядерку прямо сейчас!\n\n Инструктаж закончен! Удачи, Генерал!",
            color=0x313338
        )

        embeds = [embedNewUser_1, embedNewUser_2]

        items: list[nav.NavItem] = [
            nav.PrevButton(),
            nav.NextButton(),
        ]

        navigator = nav.NavigatorView(pages=embeds, items=items)

        builder = await navigator.build_response_async(miru_client)
        await builder.create_initial_response(ctx.interaction)

        miru_client.start_view(navigator)

        await nuclearFunc.set_new_user(user.id, False)
        await nuclearFunc.update_nuclear_mode(user.id, 1)
        return

    # Если ядерный режим отключён, то предлагаем включить
    nuclear_mode = await nuclearFunc.get_nuclear_mode(user.id)
    if nuclear_mode is False:
        view = miru.View().add_item(TurnOnNuclear())
        await ctx.respond("Ядерный режим отключён. Желаете включить?", flags=hikari.MessageFlag.EPHEMERAL, components=view)
        miru_client.start_view(view)
        return

    image_profile = await nuclearFunc.generate_arsenal(user=user)
    embedProfile = create_embed(image_url=image_profile)

    nuclear_off_view = miru.View().add_item(TurnOffNuclear())

    await ctx.respond(embed=embedProfile, components=nuclear_off_view, flags=hikari.MessageFlag.EPHEMERAL)

    miru_client.start_view(nuclear_off_view)

    os.remove("profileTemp.png")


@plugin.command
@lightbulb.add_cooldown(1, 5, lightbulb.UserBucket)
@lightbulb.option("user", "В кого запустить?", hikari.User, required=True)
@lightbulb.option("name", "Название пускаемого бое-заряда.", str, required=False)
@lightbulb.command("ядерка", "Запусти ядерку на человека.", app_command_dm_enabled=False, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def start_bomb(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx.options.user
    nuclear_name = ctx.options.name
    if nuclear_name is None:
        nuclear_name = " "
    else:
        nuclear_name = '"' + ctx.options.name + '" '
    user_id = ctx.author.id
    guild = ctx.get_guild()
    if guild is None:
        return

    # Проверка на ядерный режим автора
    self_nuclear_mode = await nuclearFunc.get_nuclear_mode(user_id)
    if self_nuclear_mode == 0:
        await ctx.respond("У вас отключён ядерный режим!", flags=hikari.MessageFlag.EPHEMERAL)
        return
    # Проверка на наличие ядерок
    bombs_count = await nuclearFunc.get_bomb_count(user_id)
    if bombs_count <= 0:
        await ctx.respond("Ваш ядерный арсенал пуст, Генерал!", flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Проверка на ядерный режим цели
    target_nuclear_mode = await nuclearFunc.get_nuclear_mode(member.id)
    if target_nuclear_mode == 0:
        await ctx.respond("У вашей цели отключён ядерный режим!", flags=hikari.MessageFlag.EPHEMERAL)
        return

    if member.communication_disabled_until() is not None:
        await ctx.respond("Ваша цель и так страдает!", flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Проверка на цель - бот
    if member.is_bot:
        embed = create_embed(
            description="Простите, я не могу допустить такого.",
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWsxY3FtYzJrcGIzZzk2MWw4MXB5b3dtbGhxazgwczhzZmttbm5xdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUA7bbaSmCUfNYjhks/giphy.gif"
        )
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    oldest_bomb_id = await nuclearFunc.get_oldest_bomb_id(user_id)

    # Интеракция при отправке на самого себя
    if member.id == user_id:
        view = miru.View(timeout=60).add_item(SelfBombActivate())

        embed = create_embed(
            description="Вы уверены, что желаете запустить в себя ядерку?"
        )
        await ctx.respond(embed=embed, components=view, flags=hikari.MessageFlag.EPHEMERAL)
        return

    try:
        if await nuclearFunc.is_bomb_activated(oldest_bomb_id):
            if await nuclearFunc.is_bomb_make_hirohito(oldest_bomb_id):
                embed = create_embed(
                    title="О, нет!",
                    description=f"{ctx.user.mention} {member.mention}, ядерка сделала Хирохито и взорвала вас обоих",
                    image_url=get_random_gif("broken_bomb")
                )
                await ctx.respond(f"||{ctx.author.mention} {member.mention}||", embed=embed, user_mentions=True)
                await ctx.app.rest.edit_member(guild, ctx.author, communication_disabled_until=pendulum.now("UTC").add(minutes=5), reason="bomb")
            else:
                embed = create_embed(
                    description=f"{member.mention}\n**Внимание! У тебя прилёт ядерного заряда {nuclear_name}от**\n{ctx.user.mention}",
                    image_url=get_random_gif("bomb_to")
                )
                await ctx.respond(f"||{member.mention}||", embed=embed)

            await ctx.app.rest.edit_member(guild, member, communication_disabled_until=pendulum.now("UTC").add(minutes=5), reason="bomb")

            await nuclearFunc.update_bomb_log(oldest_bomb_id)

            start_bomb = await nuclearFunc.get_bomb_start_count(user_id)
            await nuclearFunc.update_bomb_start_count(user_id, start_bomb + 1)

            # self.bot.dispatch("bomb_start", inter.author, member)
        else:
            embed = create_embed(
                description="Упс. Ядерка не сработала. Кажется она слишком старая.",
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDFlNTZoYXNjM21ta2FrbTZoN3E3MjNkMnhraGxhazJtaW42NjJ0ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkf7qxSEUqNCataNjK/giphy.gif"
            )
            await nuclearFunc.update_bomb_log(oldest_bomb_id)
            # self.bot.dispatch("bomb_start", ctx.author, member)
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            return
    except Exception as e:
        print(e)

    # Попытка отправке жертве успешную отправку ядерки
    try:
        DMmessage = f"ГЕНЕРАЛ! НЕ ВРЕМЯ ДРЕМАТЬ!\n\n{ctx.author.mention} запустил в нас своим вооружением {nuclear_name}и мы страдаем от этого!\n Захавай мивинку и вперёд в бой!\n`/мивинка`"
        await member.send(DMmessage, user_mentions=True)

    # Если произошла ошибка отправить в чат
    except hikari.ForbiddenError:
        embed = create_embed(
            description="Привет! В тебя запустили ядерку.\nЧтобы вылечиться используй в ЛС со мной команду `/мивинка`. \n\nЯ тебе не смогла отправить в ЛС это сообщение! При возникновении проблем с использованием команды `/мивинка` попробуй поменять настройки конфендициальности Discord."
        )

        mivina_channel_id = config_manager.get_config_value("MIVINA_CHANNEL_ID")
        marmelad_channel = await ctx.app.rest.fetch_channel(int(mivina_channel_id))
        if isinstance(marmelad_channel, hikari.TextableGuildChannel):
            await marmelad_channel.send(f"{member.mention}", embed=embed, user_mentions=True)
    except Exception as e:
        print(e)

# Мивинка
@plugin.command
@lightbulb.command("мивинка", "Использовать мивинку для лечения.", app_command_dm_enabled=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def start_mivina(ctx: lightbulb.SlashContext):
    guild_id = config_manager.get_config_value("GUILD_ID")
    guild = await ctx.app.rest.fetch_guild(int(guild_id))
    if guild is None:
        return
    user_id = ctx.user.id
    member = await ctx.app.rest.fetch_member(guild, ctx.author)

    if member is None:
        await ctx.respond("Пользователь не найден.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Проверка на наличие мивинок у пользователя
    mivina_count = await nuclearFunc.get_mivina_count(user_id)
    if mivina_count <= 0:
        await ctx.respond("Мивинки закончились, Генерал! К сожалению, ничем помочь не могу!", flags=hikari.MessageFlag.EPHEMERAL)
        return

    oldest_mivina_id = await nuclearFunc.get_oldest_mivina_id(user_id)

    mivina_channel_id = config_manager.get_config_value("MIVINA_CHANNEL_ID")
    marmelad_channel = await ctx.app.rest.fetch_channel(int(mivina_channel_id))
    if not isinstance(marmelad_channel, hikari.TextableGuildChannel):
        return
    # Убираем тайм-аут
    try:
        if await nuclearFunc.is_mivina_activated(oldest_mivina_id):
            await ctx.app.rest.edit_member(guild, member, communication_disabled_until=None, reason="mivina")

            # Отправляем в канал Мармеладка информацию о использовании мивины
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Вкусил вкусняшечки**",
                image_url=get_random_gif("mivina")
            )
            await marmelad_channel.send(embed=embed)

            await ctx.respond("Так точно, Генерал, надеюсь снова такое не произойдёт!")

            await nuclearFunc.update_mivina_log(oldest_mivina_id)

            start_mivina = await nuclearFunc.get_mivina_start_count(user_id)
            await nuclearFunc.update_mivina_start_count(user_id, start_mivina + 1)
            # self.bot.dispatch("mivina_start", inter.author)
        else:
            await ctx.respond("Возьмите салфеточку, Генерал...")
            embed = create_embed(
                description=f"{ctx.user.mention}\nЗапарил мивинку и добавил Beanz от Вафельки, которые шли в комплекте. {ctx.user.mention} стошнило. Кажется Beanz были просрочены. Почему?",
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWVpODRkMjk1am91amhuaDdiczRtYm50M2Npd3Y5aWl5eWF0Y3R3YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nfecRCYP9PjO/giphy.gif"
                )

            await marmelad_channel.send(embed=embed)
            await nuclearFunc.update_mivina_log(oldest_mivina_id)
            # self.bot.dispatch("mivina_start", inter.author)
    except Exception as e:
        await ctx.respond("Простите, произошла неизвестная ошибка")
        print(e)


@plugin.command
@lightbulb.command("кейс", "Выдача ядерки и мивинки.", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def nuclear_case(ctx: lightbulb.SlashContext):
    # Если пользователь новый - отправляем сообщение
    check_new_user = await nuclearFunc.get_new_user(ctx.author.id)
    if check_new_user is True:
        await ctx.respond("Приветствую нового генерала в системе Ядерка! Пропишите `/арсенал` для деталей", flags=hikari.MessageFlag.EPHEMERAL)
        return
    # Если старый - отправляем модальное окно с выбором ядерки или мивинки
    else:
        modal = NuclearCase()
        builder = modal.build_response(ctx.bot.d.miru)

        await builder.create_modal_response(ctx.interaction)

        ctx.bot.d.miru.start_modal(modal)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
