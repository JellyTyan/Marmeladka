import random

import hikari
import lightbulb

import yaml
from functions.anime_func import get_anime_image
from utils.create_embed import create_embed

plugin = lightbulb.Plugin("Emotions")

@plugin.command
@lightbulb.app_command_permissions(dm_enabled=False)
@lightbulb.command("эмоция", "Вырази свои чувства", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def emotion(ctx: lightbulb.Context) -> None:
    pass

@plugin.command
@lightbulb.option("user", "Кого обнять?", hikari.User, required=True)
@lightbulb.command("обнять", "Обнять кого-то", auto_defer=True)
@lightbulb.implements(lightbulb.UserCommand)
async def hug_command(ctx: lightbulb.UserContext) -> None:
    me = ctx.app.get_me()
    if me is None:
        return

    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}\nТебе не обязательно было меня обнимать. Обними своего друга...",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/4RK7EnRhtkat2/giphy.gif",
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}\nБедняжка. Обнимать себя, вместо кого-то, это грустно",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWZvdml1anZ1eHJ4MDRqYTR6cWo2dXJmeGw0eXczajdzNGdweWI4NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UOIq2y59BhuYy9YL7b/giphy.gif",
        )
        await ctx.respond(embed=embed)

    else:
        embed = hikari.Embed(
            description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}",
            color=0x2B2D31,
        )
        embed.set_image(await get_anime_image("hug"))
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого ударить?", hikari.User, required=True)
@lightbulb.command("ударить", "Ударь кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kick_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Попытался ударить** \n{user.mention}\nЧто? Думаешь ты можешь меня ударить? Я приду к тебе ночью и убью тебя.",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/wOly8pa4s4W88/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Ударил**\n{user.mention}\nБожечки, мне его жалко((",
            color=0x2B2D31,
            image_url="https://media1.tenor.com/m/mzlTqk44glQAAAAd/блять-я-сам-себя-захуярил.gif"
        )
        await ctx.respond(embed=embed)

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Ударил**\n{user.mention}",
            color=0x2B2D31,
            image_url=await get_anime_image("slap")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого приветствуешь?", hikari.User, required=True)
@lightbulb.command("привет", "Приветствуй кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hi_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}\nПриветики, привети!",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/bcKmIWkUMCjVm/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}\nСамого себя приветствовать... Он одинок?",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjI5Zno5YWNrcW9xY3ZkZGlha2o4em0xYjAzM2txNGRndmZ1Z2FzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/326aSJHSRzCQ3K2cEk/giphy.gif"
        )
        await ctx.respond(embed=embed)

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}",
            color=0x2B2D31,
            image_url=await get_anime_image("hi")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого поцеловать?", hikari.User, required=True)
@lightbulb.command("поцеловать", "Поцелуй своего любимого")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kiss_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Целует**\n{user.mention}\nЭто очень мило с твоей стороны. Спасибо! Но мне кажется лучше тебе поцеловать того, кого по настоящему любишь.",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/4orREzKni7BTi/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Целует**\n{user.mention}\nОн сам себя поцеловал. Как же это...",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDF3NTZoOTY5dTB2M3JvZTF5OGFvNWJ0bzFqcWRpYzIxYzJmM3RvdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pBj39cHnzprlS/giphy-downsized-large.gif"
        )

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Целует**\n{user.mention}",
            color=0x2B2D31,
            image_url=await get_anime_image("kiss")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого погладить?", hikari.User, required=True)
@lightbulb.command("погладить", "Погладь кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def pet_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}\nОууу... Ты меня приручил <3",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/X12bFJrWSGTqlhlztZ/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}\nГладить самого себя... Это нормально.\nСебя не полюбишь - никто не полюбит",
            color=0x2B2D31,
            image_url="https://media1.tenor.com/m/h2G84I4CL-8AAAAC/trickytank-head.gif"
        )
        await ctx.respond(embed=embed)

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}",
            color=0x2B2D31,
            image_url=await get_anime_image("pat")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.command("улыбнуться", "То и означает")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def smile_command(ctx: lightbulb.Context) -> None:
    embed = create_embed(
        description=f"{ctx.user.mention}\n**Улыбается**))",
        color=0x2B2D31,
        image_url=await get_anime_image("smile")
    )
    await ctx.respond(embed=embed)


@emotion.child
@lightbulb.command("плак-плак", "Или бигмаки?")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def cry_command(ctx: lightbulb.Context) -> None:
    embed = create_embed(
        description=f"{ctx.user.mention}\n**Плачет**(((",
        color=0x2B2D31,
        image_url=await get_anime_image("cry")
    )
    await ctx.respond(embed=embed)


@emotion.child
@lightbulb.option("user", "Перед кем напортачил?", hikari.User, required=True)
@lightbulb.command("извиниться", "Извинись перед кем напортачил!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def sorry_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}\nНу.. Я на тебя никогда не обижалась. Не стоит перед мной извинятся. Я не держу обид",
            color=0x2B2D31,
            image_url="https://media.giphy.com/media/ulWUgCk4F1GGA/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}\nЧто же ты натворил, что сам перед собой извиняешься...",
            color=0x2B2D31,
            image_url=get_random_gif("sorry")
        )
        await ctx.respond(embed=embed)

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}",
            color=0x2B2D31,
            image_url=get_random_gif("sorry")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого рукопожатишь?", hikari.User, required=True)
@lightbulb.command("рукопожатие", "Пожми руку кому-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def handshake_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}\nТы мне руку пожал)",
            image_url="https://media.giphy.com/media/CHmwA02GQ6aTS/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}",
            image_url="https://media1.tenor.com/m/LjDeSB3jOb0AAAAd/donfreez-handshake.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}",
            image_url=get_random_gif("handshake")
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого шекотать?", hikari.User, required=True)
@lightbulb.command("щекотать", "Щекотай кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def tike_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return
    user = ctx.options.user

    if user.id == me.id:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Щекотает**\n{user.mention}\nАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА",
            color=0x2B2D31,
            image_url="ttps://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTdvdWw0MTgxZXBsbzQxc2oyNnZycnAzZTJ4OHV6aWVxNHowNXVrZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7528JmqtT7cwzV1S/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    else:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Щекотает**\n{user.mention}",
            color=0x2B2D31,
            image_url=await get_anime_image("tickle")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


def get_random_gif(type: str) -> str:
    with open("src/yaml/gifs.yaml", "r") as file:
        gifs = yaml.safe_load(file)
        gif_list = gifs["gif_types"][type]
        return random.choice(gif_list)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
