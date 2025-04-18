import random

import hikari
import lightbulb

import yaml
from functions.anime_func import get_nekos_gif, get_waifu_gif
from utils.create_embed import create_embed

loader = lightbulb.Loader()

group = lightbulb.Group("commands.emotions.name", "commands.emotions.description", contexts=(hikari.ApplicationContextType(0), ), localize=True)


@group.register
class HugCommand(
    lightbulb.SlashCommand,
    name="commands.hug.name",
    description="commands.hug.description",
    localize=True
):
    user = lightbulb.user("commands.hug.options.user.name", "commands.hug.options.user.description", localize=True)

    @lightbulb.invoke
    async def hug_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Hugs** \n{user.mention}\nYou didn't have to hug me. Hug your friend...",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/4RK7EnRhtkat2/giphy.gif",
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Hugs** \n{user.mention}\nPoor thing. Hugging yourself instead of someone else is sad.",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWZvdml1anZ1eHJ4MDRqYTR6cWo2dXJmeGw0eXczajdzNGdweWI4NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UOIq2y59BhuYy9YL7b/giphy.gif",
            )
            await ctx.respond(embed=embed)

        else:
            embed = hikari.Embed(
                description=f"{ctx.user.mention}\n**Hugs** \n{user.mention}",
                color=0x2B2D31,
            )
            embed.set_image(await get_nekos_gif("hug"))
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class KickCommand(
    lightbulb.SlashCommand,
    name="commands.kick.name",
    description="commands.kick.description",
    localize=True
):
    user = lightbulb.user("commands.kick.options.user.name", "commands.kick.options.user.description", localize=True)

    @lightbulb.invoke
    async def kick_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        me = bot.get_me()
        if me is None:
            return
        user = self.user

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Tried to kick** \n{user.mention}\nWhat? You think you can hit me? I'll come to you at night and kill you.",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/wOly8pa4s4W88/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Kicks**\n{user.mention}\nOh, my God, I feel sorry for him((",
                color=0x2B2D31,
                image_url="https://media1.tenor.com/m/mzlTqk44glQAAAAd/блять-я-сам-себя-захуярил.gif"
            )
            await ctx.respond(embed=embed)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Kicks**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("slap")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class HiCommand(
    lightbulb.SlashCommand,
    name="commands.hi.name",
    description="commands.hi.description",
    localize=True
):
    user = lightbulb.user("commands.hi.options.user.name", "commands.hi.options.user.description", localize=True)

    @lightbulb.invoke
    async def hi_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        me = bot.get_me()
        if me is None:
            return
        user = self.user

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Greets**\n{user.mention}\nHenlo, Henlo!",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/bcKmIWkUMCjVm/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Greets**\n{user.mention}\nGreeting himself... Is he lonely?",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjI5Zno5YWNrcW9xY3ZkZGlha2o4em0xYjAzM2txNGRndmZ1Z2FzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/326aSJHSRzCQ3K2cEk/giphy.gif"
            )
            await ctx.respond(embed=embed)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Greets**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("wave/")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class KissCommand(
    lightbulb.SlashCommand,
    name="commands.kiss.name",
    description="commands.kiss.description",
    localize=True
):
    user = lightbulb.user("commands.kiss.options.user.name", "commands.kiss.options.user.description", localize=True)

    @lightbulb.invoke
    async def kiss_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Kisses**\n{user.mention}\nThat's very nice of you. Thank you! But I think you should kiss someone you really love.",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/4orREzKni7BTi/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Kisses**\n{user.mention}\nHe kissed himself. How did that...",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDF3NTZoOTY5dTB2M3JvZTF5OGFvNWJ0bzFqcWRpYzIxYzJmM3RvdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pBj39cHnzprlS/giphy-downsized-large.gif"
            )
            await ctx.respond(embed=embed)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Kisses**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("kiss")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)

@group.register
class PetCommand(
    lightbulb.SlashCommand,
    name="commands.pet.name",
    description="commands.pet.description",
    localize=True
):
    user = lightbulb.user("commands.pet.options.user.name", "commands.pet.options.user.description", localize=True)

    @lightbulb.invoke
    async def pet_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Pets**\n{user.mention}\nAwww... You tamed me <3",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/X12bFJrWSGTqlhlztZ/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Pets**\n{user.mention}Pets yourself... It's normal.\nIf you don't love yourself, no one will.",
                color=0x2B2D31,
                image_url="https://media1.tenor.com/m/h2G84I4CL-8AAAAC/trickytank-head.gif"
            )
            await ctx.respond(embed=embed)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Pets**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("pat")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)

@group.register
class SmileCommand(
    lightbulb.SlashCommand,
    name="commands.smile.name",
    description="commands.smile.description",
    localize=True
):

    @lightbulb.invoke
    async def smile_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        image_url = await get_nekos_gif("smile")
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Smiles**))",
            color=0x2B2D31,
            image_url=image_url
        )
        await ctx.respond(embed=embed)


@group.register
class CryCommand(
    lightbulb.SlashCommand,
    name="commands.cry.name",
    description="commands.cry.description",
    localize=True
):

    @lightbulb.invoke
    async def cry_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Crying**(((",
            color=0x2B2D31,
            image_url=await get_nekos_gif("cry")
        )
        await ctx.respond(embed=embed)


@group.register
class SorryCommand(
    lightbulb.SlashCommand,
    name="commands.sorry.name",
    description="commands.sorry.description",
    localize=True
):
    user = lightbulb.user("commands.sorry.options.user.name", "commands.sorry.options.user.description", localize=True)

    @lightbulb.invoke
    async def sorry_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Apologizes to**\n{user.mention}\nWell, I've never held a grudge against you. You don't have to apologize to me. I don't hold grudges.",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/ulWUgCk4F1GGA/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Apologizes to**\n{user.mention}\nWhat have you done that you're apologizing to yourself.....",
                color=0x2B2D31,
                image_url=get_random_gif("sorry")
            )
            await ctx.respond(embed=embed)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Apologizes to**\n{user.mention}",
                color=0x2B2D31,
                image_url=get_random_gif("sorry")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)


@group.register
class HandshakeCommand(
    lightbulb.SlashCommand,
    name="commands.handshake.name",
    description="commands.handshake.description",
    localize=True
):
    user = lightbulb.user("commands.handshake.options.user.name", "commands.handshake.options.user.description", localize=True)

    @lightbulb.invoke
    async def handshake_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Shaking hands**\n{user.mention}\nYou shook my hand)",
                color=0x2B2D31,
                image_url="https://media.giphy.com/media/CHmwA02GQ6aTS/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        elif ctx.user.id == user.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Shaking hands**\n{user.mention}",
                color=0x2B2D31,
                image_url="https://media1.tenor.com/m/LjDeSB3jOb0AAAAd/donfreez-handshake.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Shaking hands**\n{user.mention}",
                color=0x2B2D31,
                image_url=get_random_gif("handshake")
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)


@group.register
class TickleCommand(
    lightbulb.SlashCommand,
    name="commands.tickle.name",
    description="commands.tickle.description",
    localize=True
):
    user = lightbulb.user("commands.tickle.options.user.name", "commands.tickle.options.user.description", localize=True)

    @lightbulb.invoke
    async def tike_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        user = self.user

        me = bot.get_me()
        if me is None:
            return

        if user.id == me.id:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Tickles**\n{user.mention}\nАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА",
                color=0x2B2D31,
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTdvdWw0MTgxZXBsbzQxc2oyNnZycnAzZTJ4OHV6aWVxNHowNXVrZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7528JmqtT7cwzV1S/giphy.gif"
            )
            await ctx.respond(f"||{ctx.user.mention}||", embed=embed, user_mentions=True)

        else:
            embed = create_embed(
                description=f"{ctx.user.mention}\n**Tickles**\n{user.mention}",
                color=0x2B2D31,
                image_url=await get_nekos_gif("tickle")
            )
            await ctx.respond(f"||{user.mention}||", embed=embed, user_mentions=True)

@group.register
class MidfingerCommand(
    lightbulb.SlashCommand,
    name="commands.midfinger.name",
    description="commands.midfinger.description",
    localize=True
):
    @lightbulb.invoke
    async def midfinger_command(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        embed = create_embed(
            description=f"{ctx.user.mention}\n**Flips the bird**",
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
