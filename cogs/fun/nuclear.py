import os

import hikari
import lightbulb
import miru
import pendulum
from lightbulb.prefab import fixed_window
from miru.ext import nav
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager, NuclearData
from functions.nuclear_func import NuclearFunc
from ui.nuclearUI import NuclearCase, SelfBombActivate, TurnOffNuclear, TurnOnNuclear
from utils.create_embed import create_embed
from utils.get_random_gif import get_random_gif

last_switch_call = {}

loader = lightbulb.Loader()

database_manager = DatabaseManager()
config_manager = ConfigManager()
nuclear_func = NuclearFunc()


@loader.listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    session = async_sessionmaker(database_manager.engine, expire_on_commit=True)
    async with session() as session:
        user = NuclearData(
            user_id=event.user.id,
            username=event,
        )
        session.add(user)
        await session.commit()

@loader.listener(hikari.MemberDeleteEvent)
async def on_member_remove(event: hikari.MemberDeleteEvent):
    session = async_sessionmaker(database_manager.engine, expire_on_commit=True)
    async with session() as session:
        user = select(NuclearData).where(NuclearData.user_id == event.user_id)
        await session.delete(user)
        await session.commit()

# @commands.Cog.listener()
# async def on_member_update(self, before: disnake.Member, after: disnake.Member):
#     try:
#         if after.current_timeout is None:
#             nuclear_role = after.guild.get_role(NUCLEAR_ROLE)
#             await after.remove_roles(nuclear_role)
#     except Exception:
#         return


@loader.command
class SuicideCommand(
    lightbulb.SlashCommand,
    name="суицид",
    description="Press F.",
    dm_enabled=False
):
    @lightbulb.invoke
    async def help_command(self, ctx: lightbulb.Context) -> None:
        await ctx.defer(ephemeral=False)
        try:
            guild_id = ctx.guild_id
            if guild_id is None:
                return
            guild = await ctx.client.rest.fetch_guild(guild_id)
            if guild is None:
                return

            await ctx.client.rest.edit_member(guild, ctx.user, communication_disabled_until=pendulum.now("UTC").add(minutes=1), reason="Suicide")

            embed = create_embed(
                description=f"{ctx.user.mention} суициднулся. Press F",
                image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTZuaTZmczRuZ2ltM2tiemZibTZlamo0ODdqMTRjejUyNzAzZnpxeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eHR8NnClhVMwgRIAwb/giphy-downsized.gif",
                color=0x313338
            )
            await ctx.respond(embed=embed)
        except Exception:
            await ctx.respond("Простите, вы не смогли самоубиться...")


@loader.command
class ArsenalCommand(
    lightbulb.SlashCommand,
    name="арсенал",
    description="Ядерки, Мивинки - тебе это нужно?",
    dm_enabled=False,
    hooks=[fixed_window(5.0, 1, "user")]
):
    @lightbulb.invoke
    async def arsenal(self, ctx: lightbulb.Context, cx: miru.Client) -> None:
        await ctx.defer(ephemeral=True)
        user = ctx.user

        # Если пользователь новый, то отправляем вспомонательный эмбед
        if await nuclear_func.get_new_user(user.id):
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

            builder = await navigator.build_response_async(cx, ephemeral=True)
            await builder.create_initial_response(ctx.interaction)

            cx.start_view(navigator)

            await nuclear_func.set_new_user(user.id, False)
            await nuclear_func.update_nuclear_mode(user.id, 1)
            return

        # Если ядерный режим отключён, то предлагаем включить
        if await nuclear_func.get_nuclear_mode(user.id) is False:
            view = miru.View().add_item(TurnOnNuclear())
            await ctx.respond("Ядерный режим отключён. Желаете включить?", flags=hikari.MessageFlag.EPHEMERAL, components=view)
            cx.start_view(view)
            return

        image_profile = await nuclear_func.generate_arsenal(user=user)
        embedProfile = create_embed(image_url=image_profile)

        nuclear_off_view = miru.View().add_item(TurnOffNuclear())

        await ctx.respond(embed=embedProfile, components=nuclear_off_view, flags=hikari.MessageFlag.EPHEMERAL)

        cx.start_view(nuclear_off_view)

        os.remove("profileTemp.png")


@loader.command
class StartBombCommand(
    lightbulb.SlashCommand,
    name="ядерка",
    description="Запусти ядерку на человека.",
    dm_enabled=False,
    hooks=[fixed_window(5.0, 1, "user")]
):
    user = lightbulb.user("user", "В кого запустить?")
    name = lightbulb.string("name", "Название пускаемого бое-заряда.", default=None)

    @lightbulb.invoke
    async def start_bomb(self, ctx: lightbulb.Context) -> None:
        target_user = self.user
        nuclear_name = self.name

        target_user = self.user
        nuclear_name = f'"{self.name}" ' if self.name else " "

        if not ctx.guild_id:
            return

        guild = ctx.interaction.get_guild()
        if not guild:
            return

        author = guild.get_member(ctx.user.id)
        target_member = guild.get_member(target_user.id) if target_user else None

        if not author or not target_member:
            return

        # Проверка на ядерный режим автора
        author_nuclear_mode = await nuclear_func.get_nuclear_mode(author.id)
        if author_nuclear_mode == 0:
            await ctx.respond("У вас отключён ядерный режим!", ephemeral=True)
            return
        # Проверка на наличие ядерок
        bombs_count = await nuclear_func.get_weapon_count(author.id, nuclear_type="bomb")
        oldest_bomb_id = await nuclear_func.get_oldest_weapon_id(author.id, weapon_type="bomb")
        if bombs_count and bombs_count <= 0 or oldest_bomb_id is None:
            await ctx.respond("Ваш ядерный арсенал пуст, Генерал!", ephemeral=True)
            return

        # Проверка на ядерный режим цели
        target_nuclear_mode = await nuclear_func.get_nuclear_mode(target_member.id)
        if target_nuclear_mode == 0:
            await ctx.respond("У вашей цели отключён ядерный режим!", ephemeral=True)
            return

        if target_member.communication_disabled_until() is not None:
            await ctx.respond("Ваша цель и так страдает!", ephemeral=True)
            return

        # Проверка на цель - бот
        if target_member.is_bot:
            embed = create_embed(
                description="Простите, я не могу допустить такого.",
                image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWsxY3FtYzJrcGIzZzk2MWw4MXB5b3dtbGhxazgwczhzZmttbm5xdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUA7bbaSmCUfNYjhks/giphy.gif"
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return


        # Интеракция при отправке на самого себя
        if target_member.id == author.id:
            view = miru.View(timeout=60).add_item(SelfBombActivate())

            embed = create_embed(
                description="Вы уверены, что желаете запустить в себя ядерку?"
            )
            await ctx.respond(embed=embed, components=view, ephemeral=True)
            return

        try:
            if await nuclear_func.is_weapon_activated(oldest_bomb_id):
                if await nuclear_func.is_bomb_make_hirohito(oldest_bomb_id):
                    embed = create_embed(
                        title="О, нет!",
                        description=f"{author.mention} {target_member.mention}, ядерка сделала Хирохито и взорвала вас обоих",
                        image_url=get_random_gif("broken_bomb")
                    )
                    await ctx.respond(f"||{author.mention} {target_member.mention}||", embed=embed, user_mentions=True, ephemeral=False)
                    await ctx.client.rest.edit_member(guild, ctx.user, communication_disabled_until=pendulum.now("UTC").add(minutes=5), reason="bomb")
                else:
                    embed = create_embed(
                        description=f"{target_member.mention}\n**Внимание! У тебя прилёт ядерного заряда {nuclear_name}от**\n{ctx.user.mention}",
                        image_url=get_random_gif("bomb_to")
                    )
                    await ctx.respond(f"||{target_member.mention}||", embed=embed, user_mentions=True, ephemeral=False)

                await ctx.client.rest.edit_member(guild, target_member, communication_disabled_until=pendulum.now("UTC").add(minutes=5), reason="bomb")

                await nuclear_func.update_log_used(oldest_bomb_id)

                start_bomb = await nuclear_func.get_start_count(author.id, "bomb_start_count")
                await nuclear_func.update_start_count(author.id, start_bomb + 1, "bomb_start_count")

                # self.bot.dispatch("bomb_start", inter.author, member)
            else:
                embed = create_embed(
                    description="Упс. Ядерка не сработала. Кажется она слишком старая.",
                    image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDFlNTZoYXNjM21ta2FrbTZoN3E3MjNkMnhraGxhazJtaW42NjJ0ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkf7qxSEUqNCataNjK/giphy.gif"
                )
                await nuclear_func.update_log_used(oldest_bomb_id)
                # self.bot.dispatch("bomb_start", ctx.author, member)
                await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
                return
        except Exception as e:
            print(e)

        # Попытка отправке жертве успешную отправку ядерки
        try:
            DMmessage = f"ГЕНЕРАЛ! НЕ ВРЕМЯ ДРЕМАТЬ!\n\n{author.mention} запустил в нас своим вооружением {nuclear_name}и мы страдаем от этого!\n Захавай мивинку и вперёд в бой!\n`/мивинка`"
            await target_member.send(DMmessage, user_mentions=True)

        # Если произошла ошибка отправить в чат
        except hikari.ForbiddenError:
            embed = create_embed(
                description="Привет! В тебя запустили ядерку.\nЧтобы вылечиться используй в ЛС со мной команду `/мивинка`. \n\nЯ тебе не смогла отправить в ЛС это сообщение! При возникновении проблем с использованием команды `/мивинка` попробуй поменять настройки конфендициальности Discord."
            )

            mivina_channel_id = config_manager.get_config_value("MIVINA_CHANNEL_ID")
            marmelad_channel = await ctx.client.rest.fetch_channel(int(mivina_channel_id))
            if isinstance(marmelad_channel, hikari.TextableGuildChannel):
                await marmelad_channel.send(f"{target_member.mention}", embed=embed, user_mentions=True)
        except Exception as e:
            print(e)


@loader.command
class StartMivinaCommand(
    lightbulb.SlashCommand,
    name="мивинка",
    description="Использовать мивинку для лечения.",
    hooks=[fixed_window(5.0, 1, "user")]
):
    @lightbulb.invoke
    async def mivina_bomb(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()

        guild_id = config_manager.get_config_value("GUILD_ID")
        if not guild_id:
            return

        guild = await ctx.client.rest.fetch_guild(int(guild_id))
        if not guild:
            return

        member = guild.get_member(ctx.user.id)
        if not member:
            await ctx.respond("Пользователь не найден.", flags=hikari.MessageFlag.EPHEMERAL)
            return

        # Проверка на наличие мивинок у пользователя
        mivina_count = await nuclear_func.get_weapon_count(member.id, nuclear_type="mivina")
        oldest_mivina_id = await nuclear_func.get_oldest_weapon_id(member.id, weapon_type="mivina")
        if mivina_count is None or mivina_count <= 0 or oldest_mivina_id is None:
            await ctx.respond("Мивинки закончились, Генерал! К сожалению, ничем помочь не могу!", flags=hikari.MessageFlag.NONE)
            return

        mivina_channel_id = config_manager.get_config_value("MIVINA_CHANNEL_ID")
        marmelad_channel = await ctx.client.rest.fetch_channel(int(mivina_channel_id))
        if not isinstance(marmelad_channel, hikari.TextableGuildChannel):
            return
        # Убираем тайм-аут
        try:
            if await nuclear_func.is_weapon_activated(oldest_mivina_id):
                await ctx.client.rest.edit_member(guild, member, communication_disabled_until=None, reason="mivina")

                # Отправляем в канал Мармеладка информацию о использовании мивины
                embed = create_embed(
                    description=f"{ctx.user.mention}\n**Вкусил вкусняшечки**",
                    image_url=get_random_gif("mivina")
                )
                await marmelad_channel.send(embed=embed)

                await ctx.respond("Так точно, Генерал, надеюсь снова такое не произойдёт!", flags=hikari.MessageFlag.NONE)

                await nuclear_func.update_log_used(oldest_mivina_id)

                start_mivina = await nuclear_func.get_start_count(member.id, "mivina_start_count")
                await nuclear_func.update_start_count(member.id, start_mivina + 1, "mivina_start_count")
                # self.bot.dispatch("mivina_start", inter.author)
            else:
                await ctx.respond("Возьмите салфеточку, Генерал...")
                embed = create_embed(
                    description=f"{ctx.user.mention}\nЗапарил мивинку и добавил Beanz от Вафельки, которые шли в комплекте. {ctx.user.mention} стошнило. Кажется Beanz были просрочены. Почему?",
                    image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWVpODRkMjk1am91amhuaDdiczRtYm50M2Npd3Y5aWl5eWF0Y3R3YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nfecRCYP9PjO/giphy.gif"
                    )

                await marmelad_channel.send(embed=embed)
                await nuclear_func.update_log_used(oldest_mivina_id)
                # self.bot.dispatch("mivina_start", inter.author)
        except Exception as e:
            await ctx.respond("Простите, произошла неизвестная ошибка")
            print(e)


@loader.command
class NuclearCaseCommand(
    lightbulb.SlashCommand,
    name="кейс",
    description="Выдача ядерки и мивинки.",
    dm_enabled=False,
):
    @lightbulb.invoke
    async def nuclear_case(self, ctx: lightbulb.Context, cx: miru.Client) -> None:
        check_new_user = await nuclear_func.get_new_user(ctx.user.id)
        if check_new_user is True:
            await ctx.respond("Приветствую нового генерала в системе Ядерка! Пропишите `/арсенал` для деталей", flags=hikari.MessageFlag.EPHEMERAL)
            return
        else:
            modal = NuclearCase()
            builder = modal.build_response(cx)

            await builder.create_modal_response(ctx.interaction)

            cx.start_modal(modal)
