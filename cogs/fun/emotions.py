import random

import hikari
import lightbulb

import yaml
from functions.anime_func import get_nekos_gif, get_waifu_gif
from utils.create_embed import create_embed

loader = lightbulb.Loader()

group = lightbulb.Group("эмоция", "Вырази свои чувства!", dm_enabled=False)


@group.register
class HugCommand(
    lightbulb.SlashCommand,
    name="обнять",
    description="Обнять кого-то"
):
    user = lightbulb.user("user", "Кого обнять?")

    @lightbulb.invoke
    async def hug_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Обнимает** \n{user.mention}\nТебе не обязательно было меня обнимать. Обними своего друга...",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/4RK7EnRhtkat2/giphy.gif",
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

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
            embed.set_image(await get_nekos_gif("hug"))
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class KickCommand(
    lightbulb.SlashCommand,
    name="ударить",
    description="Ударь кого-то"
):
    user = lightbulb.user("user", "Кого ударить?")

    @lightbulb.invoke
    async def kick_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        me = bot.get_me()
        if me is None:
            return
        user = self.user

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Попытался ударить** \n{user.mention}\nЧто? Думаешь ты можешь меня ударить? Я приду к тебе ночью и убью тебя.",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/wOly8pa4s4W88/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

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
                image_url=await get_nekos_gif("slap")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class HiCommand(
    lightbulb.SlashCommand,
    name="привет",
    description="Приветствуй кого-то"
):
    user = lightbulb.user("user", "Кого приветствуешь?")

    @lightbulb.invoke
    async def hi_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        me = bot.get_me()
        if me is None:
            return
        user = self.user

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Поприветствовал**\n{user.mention}\nПриветики, привети!",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/bcKmIWkUMCjVm/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

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
                image_url=await get_nekos_gif("wave/")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class KissCommand(
    lightbulb.SlashCommand,
    name="поцеловать",
    description="Поцелуй своего любимого"
):
    user = lightbulb.user("user", "Кого поцеловать?")

    @lightbulb.invoke
    async def kiss_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Целует**\n{user.mention}\nЭто очень мило с твоей стороны. Спасибо! Но мне кажется лучше тебе поцеловать того, кого по настоящему любишь.",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/4orREzKni7BTi/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Целует**\n{user.mention}\nОн сам себя поцеловал. Как же это...",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDF3NTZoOTY5dTB2M3JvZTF5OGFvNWJ0bzFqcWRpYzIxYzJmM3RvdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pBj39cHnzprlS/giphy-downsized-large.gif"
            )
            await ctx.respond(embed=embed)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Целует**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("kiss")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)

@group.register
class PetCommand(
    lightbulb.SlashCommand,
    name="погладить",
    description="Погладь кого-то"
):
    user = lightbulb.user("user", "Кого погладить?")

    @lightbulb.invoke
    async def pet_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Гладит**\n{user.mention}\nОууу... Ты меня приручил <3",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/X12bFJrWSGTqlhlztZ/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

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
                image_url=await get_nekos_gif("pat")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)

@group.register
class SmileCommand(
    lightbulb.SlashCommand,
    name="улыбнуться",
    description="То и означает"
):

    @lightbulb.invoke
    async def smile_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        image_url = await get_nekos_gif("smile")
        print(image_url)
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Улыбается**))",
            color=0x2B2D31,
            image_url=image_url
        )
        await ctx.respond(embed=embed)


@group.register
class CryCommand(
    lightbulb.SlashCommand,
    name="плак-плак",
    description="Или бигмаки?"
):

    @lightbulb.invoke
    async def cry_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Плачет**(((",
            color=0x2B2D31,
            image_url=await get_nekos_gif("cry")
        )
        await ctx.respond(embed=embed)


@group.register
class SorryCommand(
    lightbulb.SlashCommand,
    name="извиниться",
    description="Извинись перед кем напортачил!"
):
    user = lightbulb.user("user", "Перед кем напортачил?")

    @lightbulb.invoke
    async def sorry_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Извиняется перед**\n{user.mention}\nНу.. Я на тебя никогда не обижалась. Не стоит перед мной извиняться. Я не держу обид",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/ulWUgCk4F1GGA/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

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
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class HandshakeCommand(
    lightbulb.SlashCommand,
    name="рукопожатие",
    description="Пожми руку кому-то"
):
    user = lightbulb.user("user", "Кого рукопожатишь?")

    @lightbulb.invoke
    async def handshake_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}\nТы мне руку пожал)",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/CHmwA02GQ6aTS/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}",
                color=0x2B2D31,
                image_url="https://media1.tenor.com/m/LjDeSB3jOb0AAAAd/donfreez-handshake.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Жмёт руку**\n{user.mention}",
                color=0x2B2D31,
                image_url=get_random_gif("handshake")
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)


@group.register
class TickleCommand(
    lightbulb.SlashCommand,
    name="щекотать",
    description="Щекотай кого-то"
):
    user = lightbulb.user("user", "Кого шекотать?")

    @lightbulb.invoke
    async def tike_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Щекотает**\n{user.mention}\nАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА",
                color=0x2B2D31,
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTdvdWw0MTgxZXBsbzQxc2oyNnZycnAzZTJ4OHV6aWVxNHowNXVrZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7528JmqtT7cwzV1S/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Щекотает**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("tickle")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)

@group.register
class MidfingerCommand(
    lightbulb.SlashCommand,
    name="фак",
    description="Весёлый третий пальчик."
):
    @lightbulb.invoke
    async def midfinger_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Показывает фак**",
            color=0x2B2D31,
            image_url=await get_waifu_gif("midfing")
        )
        await ctx.respond(embed=embed)


def get_random_gif(type: str) -> str:
    with open("src/yaml/gifs.yaml", "r") as file:
        gifs = yaml.safe_load(file)
        gif_list = gifs["gif_types"][type]
        return random.choice(gif_list)


loader.command(group)
