import random
import asyncio

import hikari
from hikari.api import *
import lightbulb

import yaml
from functions.anime_func import get_anime_image

plugin = lightbulb.Plugin("Emotions")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("эмоция", "Вырази свои чувства")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def emotion(ctx: lightbulb.Context) -> None:
    pass

@emotion.child
@lightbulb.option("user", "Кого обнять?", hikari.User, required=True)
@lightbulb.command("обнять", "Обнять кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hug_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    if me is None:
        return

    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}\nТебе не обязательно было меня обнимать. Обними своего друга...",
            color=0x2B2D31,
            image="https://media.giphy.com/media/4RK7EnRhtkat2/giphy.gif",
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}\nБедняжка. Обнимать себя, вместо кого-то, это грустно",
            color=0x2B2D31,
            image="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWZvdml1anZ1eHJ4MDRqYTR6cWo2dXJmeGw0eXczajdzNGdweWI4NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UOIq2y59BhuYy9YL7b/giphy.gif",
        )
        await ctx.respond(embed=embed)

    else:
        embed = hikari.Embed(
            description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}",
            color=0x2B2D31,
        )
        embed.set_image(await get_anime_image("cuddle"))
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого ударить?", hikari.User, required=True)
@lightbulb.command("ударить", "Ударь кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kick_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Попытался ударить** \n{user.mention}\nЧто? Думаешь ты можешь меня ударить? Я приду к тебе ночью и убью тебя.",
            color=0x2B2D31,
            image="https://media.giphy.com/media/wOly8pa4s4W88/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Ударил**\n{user.mention}\nБожечки, мне его жалко((",
            color=0x2B2D31,
            image="https://media1.tenor.com/m/mzlTqk44glQAAAAd/блять-я-сам-себя-захуярил.gif"
        )
        await ctx.respond(embed=embed)

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Ударил**\n{user.mention}",
            color=0x2B2D31,
            image=await get_anime_image("slap")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого приветствуешь?", hikari.User, required=True)
@lightbulb.command("привет", "Приветствуй кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hi_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}\nПриветики, привети!",
            color=0x2B2D31,
            image="https://media.giphy.com/media/bcKmIWkUMCjVm/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}\nСамого себя приветствовать... Он одинок?",
            color=0x2B2D31,
            image="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjI5Zno5YWNrcW9xY3ZkZGlha2o4em0xYjAzM2txNGRndmZ1Z2FzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/326aSJHSRzCQ3K2cEk/giphy.gif"
        )
        await ctx.respond(embed=embed)

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}",
            color=0x2B2D31,
            image=await get_anime_image("wave")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого поцеловать?", hikari.User, required=True)
@lightbulb.command("поцеловать", "Поцелуй своего любимого")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kiss_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Целует**\n{user.mention}\nЭто очень мило с твоей стороны. Спасибо! Но мне кажется лучше тебе поцеловать того, кого по настоящему любишь.",
            color=0x2B2D31,
            image="https://media.giphy.com/media/4orREzKni7BTi/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Целует**\n{user.mention}\nОн сам себя поцеловал. Как же это...",
            color=0x2B2D31,
            image="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDF3NTZoOTY5dTB2M3JvZTF5OGFvNWJ0bzFqcWRpYzIxYzJmM3RvdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pBj39cHnzprlS/giphy-downsized-large.gif"
        )

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Целует**\n{user.mention}",
            color=0x2B2D31,
            image=await get_anime_image("kiss")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого погладить?", hikari.User, required=True)
@lightbulb.command("погладить", "Погладь кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def pet_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}\nОууу... Ты меня приручил <3",
            color=0x2B2D31,
            image="https://media.giphy.com/media/X12bFJrWSGTqlhlztZ/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}\nГладить самого себя... Это нормально.\nСебя не полюбишь - никто не полюбит",
            color=0x2B2D31,
            image="https://media1.tenor.com/m/h2G84I4CL-8AAAAC/trickytank-head.gif"
        )
        await ctx.respond(embed=embed)

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}",
            color=0x2B2D31,
            image=await get_anime_image("pet")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.command("улыбнуться", "То и означает")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def smile_command(ctx: lightbulb.Context) -> None:
    embed = generate_embed(
        description=f"{ctx.user.mention}\n**Улыбается**))",
        color=0x2B2D31,
        image=await get_anime_image("smile")
    )
    await ctx.respond(embed=embed)


@emotion.child
@lightbulb.option("user", "Перед кем напортачил?", hikari.User, required=True)
@lightbulb.command("извиниться", "Извинись перед кем напортачил!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def sorry_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}\nНу.. Я на тебя никогда не обижалась. Не стоит перед мной извинятся. Я не держу обид",
            color=0x2B2D31,
            image="https://media.giphy.com/media/ulWUgCk4F1GGA/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}\nЧто же ты натворил, что сам перед собой извиняешься...",
            color=0x2B2D31,
            image=get_random_gif("sorry")
        )
        await ctx.respond(embed=embed)

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}",
            color=0x2B2D31,
            image=get_random_gif("sorry")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого рукопожатишь?", hikari.User, required=True)
@lightbulb.command("рукопожатие", "Пожми руку кому-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def handshake_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}\nТы мне руку пожал)"
        )
        embed.set_image(url="https://media.giphy.com/media/CHmwA02GQ6aTS/giphy.gif")
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    elif ctx.user.id == user.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}",
            image="https://media1.tenor.com/m/LjDeSB3jOb0AAAAd/donfreez-handshake.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}",
            image=get_random_gif("handshake")
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)


@emotion.child
@lightbulb.option("user", "Кого шекотать?", hikari.User, required=True)
@lightbulb.command("щекотать", "Щекотай кого-то")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def tike_command(ctx: lightbulb.Context) -> None:
    me = ctx.app.get_me()
    user = ctx.options.user

    if user.id == me.id:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Щекотает**\n{user.mention}\nАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА",
            color=0x2B2D31,
            image="ttps://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTdvdWw0MTgxZXBsbzQxc2oyNnZycnAzZTJ4OHV6aWVxNHowNXVrZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7528JmqtT7cwzV1S/giphy.gif"
        )
        await ctx.respond(f"||{ctx.user.mention}||", embed=embed)

    else:
        embed = generate_embed(
            description=f"{ctx.user.mention}\n**Щекотает**\n{user.mention}",
            color=0x2B2D31,
            image=await get_anime_image("tickle")
        )
        await ctx.respond(f"||{user.mention}||", embed=embed)


@plugin.command
@lightbulb.command("свидание", "Поиграть в свидание")
@lightbulb.implements(lightbulb.SlashCommand)
async def dateCMD(ctx: lightbulb.Context):
    me = ctx.app.get_me()


    voice_channel = voice_state.channel
    await ctx.bot.join_voice_channel(voice_channel)

    # if not me.voice_clients:
    #     vc = await channelTest.connect()
    # else:
    #     vc = me.voice_clients[0]
    # if vc and vc.is_playing():
    #     await asyncio.sleep(1)
    #     return
    await ctx.respond("Идём❤️", ephemeral=True)


def get_random_gif(type: str) -> str:
    with open("src/yaml/gifs.yaml", "r") as file:
        gifs = yaml.safe_load(file)
        gif_list = gifs["gif_types"][type]
        return random.choice(gif_list)

def generate_embed(description: str, color: int, image: str) -> hikari.Embed:
    embed = hikari.Embed(
        description=description,
        color=color,
    )
    embed.set_image(image)
    return embed


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
