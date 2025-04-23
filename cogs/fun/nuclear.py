import json
import logging
import os

import arc
import hikari
import miru
import pendulum
from miru.ext import nav
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config_manager import ConfigManager
from database.init import db
from database.models import NuclearData
from functions.nuclear_func import NuclearFunc
from functions.user_profile_func import UserProfileFunc
from ui.nuclearUI import NuclearCase, SelfBombActivate, TurnOffNuclear, TurnOnNuclear
from utils.create_embed import create_embed
from utils.get_random_gif import get_random_gif

last_switch_call = {}

plugin = arc.GatewayPlugin("Nuclear")

logger = logging.getLogger(__name__)

config_manager = ConfigManager()
nuclear_func = NuclearFunc()


@plugin.listen(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    session = async_sessionmaker(db.engine, expire_on_commit=True)
    async with session() as session:
        user = NuclearData(
            user_id=event.user.id,
            username=event,
        )
        session.add(user)
        await session.commit()

@plugin.listen(hikari.MemberDeleteEvent)
async def on_member_remove(event: hikari.MemberDeleteEvent):
    session = async_sessionmaker(db.engine, expire_on_commit=True)
    async with session() as session:
        user = select(NuclearData).where(NuclearData.user_id == event.user_id)
        await session.delete(user)
        await session.commit()


@plugin.include
@arc.slash_command(
    "suicide", "Press F.",
    invocation_contexts=[hikari.ApplicationContextType.GUILD]
    )
async def suicide_command(ctx: arc.GatewayContext) -> None:
    try:
        guild = ctx.get_guild()
        if guild is None:
            return

        await ctx.client.rest.edit_member(guild, ctx.user, communication_disabled_until=pendulum.now("UTC").add(minutes=1), reason="Suicide")

        embed = create_embed(
            description=f"{ctx.user.mention} made suicide. Press F",
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTZuaTZmczRuZ2ltM2tiemZibTZlamo0ODdqMTRjejUyNzAzZnpxeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eHR8NnClhVMwgRIAwb/giphy-downsized.gif",
            color=0x313338
        )
        await ctx.respond(embed=embed)
    except Exception:
        with open ("localization/ru-Ru.json", "r") as f:
            data = json.load(f)

        await ctx.respond(data.get("suicide").get("fail"))


@plugin.include
@arc.with_hook(arc.channel_limiter(5.0, 1))
@arc.slash_command(
    "arsenal", "Nukes, Mivinki - do you need it?",
    invocation_contexts=[hikari.ApplicationContextType.GUILD],
    )
async def arsenal_command(ctx: arc.GatewayContext, cx: miru.Client = arc.inject()) -> None:
    user = ctx.user

    # Если пользователь новый, то отправляем вспомонательный эмбед
    if await nuclear_func.get_new_user(user.id):
        user_language = await UserProfileFunc().get_lang(user.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)
        embedNewUser_1 = create_embed(
            title=language_json["arsenal"]["new_user"][0]["title"],
            description=language_json["arsenal"]["new_user"][0]["description"],
            image_url="https://cdn.discordapp.com/attachments/1149398121110057088/1197523129187188816/nuclear-weapons-earth-0308221.png?ex=65bb9352&is=65a91e52&hm=b44b59d17423f2a75659eb7746f9f8663fc489e3c0e8f60f8b90828385d390bf&",
            color=0x313338
        )

        embedNewUser_2 = create_embed(
            title=language_json["arsenal"]["new_user"][1]["title"],
            description=language_json["arsenal"]["new_user"][1]["description"],
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
        await nuclear_func.update_nuclear_mode(user.id, True)
        return

    # Если ядерный режим отключён, то предлагаем включить
    if await nuclear_func.get_nuclear_mode(user.id) is False:
        user_language = await UserProfileFunc().get_lang(user.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        view = miru.View().add_item(TurnOnNuclear())
        await ctx.respond(language_json["arsenal"]["nuclear_off"], flags=hikari.MessageFlag.EPHEMERAL, components=view)
        cx.start_view(view)
        return

    image_profile = await nuclear_func.generate_arsenal(user=user)
    embedProfile = create_embed(image_url=image_profile)

    nuclear_off_view = miru.View().add_item(TurnOffNuclear())

    await ctx.respond(embed=embedProfile, components=nuclear_off_view, flags=hikari.MessageFlag.EPHEMERAL)

    cx.start_view(nuclear_off_view)

    os.remove(image_profile)


@plugin.include
@arc.with_hook(arc.channel_limiter(5.0, 1))
@arc.slash_command(
    "nuclear", "Nuke a man.",
    invocation_contexts=[hikari.ApplicationContextType.GUILD],
    )
async def startbomb_command(
    ctx: arc.GatewayContext,
    target_user: arc.Option[hikari.User, arc.UserParams("Launch at who?", name="user")],
    nuclear_name: arc.Option[str | None, arc.StrParams("What is the name of the nuclear bomb?", name="name")] = None
    ) -> None:
    nuclear_name = f'"{nuclear_name}" ' if nuclear_name else " "

    guild = ctx.get_guild()
    if not guild:
        return

    author = guild.get_member(ctx.user.id)
    target_member = guild.get_member(target_user.id) if target_user else None

    if not author or not target_member:
        return

    # Получения языка пользователя
    user_language = await UserProfileFunc().get_lang(author.id)
    with open (f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)

    # Проверка на ядерный режим автора
    author_nuclear_mode = await nuclear_func.get_nuclear_mode(author.id)
    if author_nuclear_mode is False:
        await ctx.respond(language_json["start_bomb"]["nuclear_off"], flags=hikari.MessageFlag.EPHEMERAL)
        return
    # Проверка на наличие ядерок
    bombs_count = await nuclear_func.get_weapon_count(author.id, nuclear_type="bomb")
    oldest_bomb_id = await nuclear_func.get_oldest_weapon_id(author.id, weapon_type="bomb")
    if bombs_count and bombs_count <= 0 or oldest_bomb_id is None:
        await ctx.respond(language_json["start_bomb"]["arsenal_empty"], flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Проверка на ядерный режим цели
    target_nuclear_mode = await nuclear_func.get_nuclear_mode(target_member.id)
    if target_nuclear_mode is False:
        await ctx.respond(language_json["start_bomb"]["target_nuclear_off"], flags=hikari.MessageFlag.EPHEMERAL)
        return

    if target_member.communication_disabled_until() is not None:
        await ctx.respond(language_json["start_bomb"]["target_suffering"], flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Проверка на цель - бот
    if target_member.is_bot:
        embed = create_embed(
            description=language_json["start_bomb"]["bot_protection"],
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWsxY3FtYzJrcGIzZzk2MWw4MXB5b3dtbGhxazgwczhzZmttbm5xdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUA7bbaSmCUfNYjhks/giphy.gif"
        )
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        return


    # Интеракция при отправке на самого себя
    if target_member.id == author.id:
        view = miru.View(timeout=60).add_item(SelfBombActivate())

        embed = create_embed(description=language_json["start_bomb"]["self_bomb"])
        await ctx.respond(embed=embed, components=view, flags=hikari.MessageFlag.EPHEMERAL)
        return

    try:
        if await nuclear_func.is_weapon_activated(oldest_bomb_id):
            if await nuclear_func.is_bomb_make_hirohito(oldest_bomb_id):
                embed = create_embed(
                    title="Oh, no!",
                    description=f"{author.mention} {target_member.mention}, nuclear did a Hirohito and blew you both up.",
                    image_url=get_random_gif("broken_bomb")
                )
                await ctx.respond(
                    f"||{author.mention} {target_member.mention}||",
                    embed=embed, user_mentions=True,
                    flags=hikari.MessageFlag.EPHEMERAL
                    )
                await ctx.client.rest.edit_member(guild, ctx.user, communication_disabled_until=pendulum.now("UTC").add(minutes=5), reason="bomb")
            else:
                embed = create_embed(
                    description=f"{target_member.mention}\n**WARNING! You’re getting hit by a nuclear payload {nuclear_name}from**\n{ctx.user.mention}",
                    image_url=get_random_gif("bomb_to")
                )
                await ctx.respond(
                    f"||{target_member.mention}||",
                    embed=embed,
                    user_mentions=True,
                    flags=hikari.MessageFlag.EPHEMERAL
                    )

            await ctx.client.rest.edit_member(
                guild,
                target_member,
                communication_disabled_until=pendulum.now("UTC").add(minutes=5),
                reason="bomb"
                )

            await nuclear_func.update_log_used(oldest_bomb_id)

            start_bomb = await nuclear_func.get_start_count(author.id, "bomb_start_count")
            await nuclear_func.update_start_count(author.id, start_bomb + 1, "bomb_start_count")

            # self.bot.dispatch("bomb_start", inter.author, member)
        else:
            embed = create_embed(
                description="Oops. The nuke didn’t go off. Seems like it’s too old.",
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDFlNTZoYXNjM21ta2FrbTZoN3E3MjNkMnhraGxhazJtaW42NjJ0ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkf7qxSEUqNCataNjK/giphy.gif"
            )
            await nuclear_func.update_log_used(oldest_bomb_id)
            # self.bot.dispatch("bomb_start", ctx.author, member)
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            return
    except Exception as e:
        logger.error(e)

    # Попытка отправке жертве успешную отправку ядерки
    try:
        DMmessage = (language_json["start_bomb"]["dm_alert"]).format(author.mention, nuclear_name)
        await target_member.send(DMmessage, user_mentions=True)

    # Если произошла ошибка отправить в чат
    except hikari.ForbiddenError:
        embed = create_embed(description=language_json["start_bomb"]["mivina_help"])

        mivina_channel_id = config_manager.get_config_value("MIVINA_CHANNEL_ID")
        marmelad_channel = await ctx.client.rest.fetch_channel(int(mivina_channel_id))
        if isinstance(marmelad_channel, hikari.TextableGuildChannel):
            await marmelad_channel.send(f"{target_member.mention}", embed=embed, user_mentions=True)
    except Exception as e:
        logger.error(e)

@startbomb_command.set_error_handler
async def startbomb_error_handler(
    ctx: arc.GatewayContext, error: Exception
) -> None:
    if isinstance(error, arc.UnderCooldownError):
        await ctx.respond(
            "Command is on cooldown!"
            f"\nTry again in `{error.retry_after}` seconds."
        )
    else:
        raise error


@plugin.include
@arc.with_hook(arc.channel_limiter(5.0, 1))
@arc.slash_command(
    "mivina", "Use mivinka for treatment.",
    invocation_contexts=[hikari.ApplicationContextType.BOT_DM],
    )
async def mivina_command(ctx: arc.GatewayContext) -> None:
    guild_id = config_manager.get_config_value("GUILD_ID")
    if not guild_id:
        return

    guild =ctx.client.cache.get_guild(int(guild_id))
    if not guild:
        return

    # Получения языка пользователя
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open (f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)

    member = guild.get_member(ctx.user.id)
    if not member:
        await ctx.respond(language_json["mivina"]["no_member"], flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Проверка на наличие мивинок у пользователя
    mivina_count = await nuclear_func.get_weapon_count(member.id, nuclear_type="mivina")
    oldest_mivina_id = await nuclear_func.get_oldest_weapon_id(member.id, weapon_type="mivina")
    if mivina_count is None or mivina_count <= 0 or oldest_mivina_id is None:
        await ctx.respond(language_json["mivina"]["no_mivina"], flags=hikari.MessageFlag.NONE)
        return

    if member.communication_disabled_until() is None:
        await ctx.respond(language_json["mivina"]["healthy"], flags=hikari.MessageFlag.NONE)
        return

    mivina_channel_id = config_manager.get_config_value("MIVINA_CHANNEL_ID")
    marmelad_channel = ctx.client.cache.get_guild_channel(int(mivina_channel_id))
    if not isinstance(marmelad_channel, hikari.TextableGuildChannel):
        return
    # Убираем тайм-аут
    try:
        if await nuclear_func.is_weapon_activated(oldest_mivina_id):
            await ctx.client.rest.edit_member(guild, member, communication_disabled_until=None, reason="mivina")

            # Отправляем в канал Мармеладка информацию о использовании мивины
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Tasted the deliciousness!**",
                image_url=get_random_gif("mivina")
            )
            await marmelad_channel.send(embed=embed)

            await ctx.respond(language_json["mivina"]["success_dm"], flags=hikari.MessageFlag.NONE)

            await nuclear_func.update_log_used(oldest_mivina_id)

            start_mivina = await nuclear_func.get_start_count(member.id, "mivina_start_count")
            await nuclear_func.update_start_count(member.id, start_mivina + 1, "mivina_start_count")
            # self.bot.dispatch("mivina_start", inter.author)
        else:
            await ctx.respond(language_json["mivina"]["not_success"])
            embed = create_embed(
                description=(language_json["mivina"]["bad_mivina"]).format(user=ctx.user.mention),
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWVpODRkMjk1am91amhuaDdiczRtYm50M2Npd3Y5aWl5eWF0Y3R3YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nfecRCYP9PjO/giphy.gif"
                )

            await marmelad_channel.send(embed=embed)
            await nuclear_func.update_log_used(oldest_mivina_id)
            # self.bot.dispatch("mivina_start", inter.author)
    except Exception as e:
        await ctx.respond(language_json["mivina"]["error"])
        logger.error(e)

@mivina_command.set_error_handler
async def mivina_error_handler(
    ctx: arc.GatewayContext, error: Exception
) -> None:
    if isinstance(error, arc.UnderCooldownError):
        await ctx.respond(
            "Command is on cooldown!"
            f"\nTry again in `{error.retry_after}` seconds."
        )
    else:
        raise error


@plugin.include
@arc.with_hook(arc.channel_limiter(5.0, 1))
@arc.slash_command(
    "case", "Issuing nukes and mivinas.",
    invocation_contexts=[hikari.ApplicationContextType.GUILD],
    )
async def nuclear_case(ctx: arc.GatewayContext, cx: miru.Client = arc.inject()) -> None:
    check_new_user = await nuclear_func.get_new_user(ctx.user.id)
    if check_new_user is True:
        user_language = await UserProfileFunc().get_lang(ctx.user.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)
        await ctx.respond(language_json["nuclear_case"]["new_user"], flags=hikari.MessageFlag.EPHEMERAL)
        return
    else:
        modal = NuclearCase()
        builder = modal.build_response(cx)

        await builder.create_modal_response(ctx.interaction)

        cx.start_modal(modal)

@nuclear_case.set_error_handler
async def case_error_handler(
    ctx: arc.GatewayContext, error: Exception
) -> None:
    if isinstance(error, arc.UnderCooldownError):
        await ctx.respond(
            "Command is on cooldown!"
            f"\nTry again in `{error.retry_after}` seconds."
        )
    else:
        await ctx.respond("❌ Something went wrong. Please contact the bot developer.", flags=hikari.MessageFlag.EPHEMERAL)


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
