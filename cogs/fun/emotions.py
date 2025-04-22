import random

import arc
import hikari

import yaml
from functions.anime_func import get_nekos_gif, get_waifu_gif
from utils.create_embed import create_embed

plugin = arc.GatewayPlugin("Emotions", invocation_contexts=(hikari.ApplicationContextType(0), ))

emotions = plugin.include_slash_group("emotions", "Express your feelings!", autodefer=arc.AutodeferMode.ON)


@emotions.include
@arc.slash_subcommand("hug", "Give someone a hug")
async def hug_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("The user to say hi to.", name="user")]
):
    me = ctx.client.cache.get_me()
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


@emotions.include
@arc.slash_subcommand("kick", "Kick someone.")
async def kick_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Kick who?", name="user")]
):
    me = ctx.client.cache.get_me()
    if me is None:
        return

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


@emotions.include
@arc.slash_subcommand("greet", "Greet someone.")
async def greet_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Who are you greeting?", name="user")]
):
    me = ctx.client.cache.get_me()
    if me is None:
        return

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


@emotions.include
@arc.slash_subcommand("kiss", "Kiss your lover!")
async def kiss_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Who to kiss?", name="user")]
):
    me = ctx.client.cache.get_me()
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


@emotions.include
@arc.slash_subcommand("pet", "Pet someone!")
async def pet_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Who to pet?", name="user")]
):
    me = ctx.client.cache.get_me()
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


@emotions.include
@arc.slash_subcommand("smile", "That's what it means.")
async def smile_command(ctx: arc.GatewayContext):
    image_url = await get_nekos_gif("smile")
    embed = create_embed(
        description=f"{ctx.user.mention}\n**Smiles**))",
        color=0x2B2D31,
        image_url=image_url
    )
    await ctx.respond(embed=embed)


@emotions.include
@arc.slash_subcommand("cry", "Cry about it?")
async def cry_command(ctx: arc.GatewayContext):
    embed = create_embed(
        description=f"{ctx.user.mention}\n**Crying**(((",
        color=0x2B2D31,
        image_url=await get_nekos_gif("cry")
    )
    await ctx.respond(embed=embed)


@emotions.include
@arc.slash_subcommand("sorry", "Sorry to whoever you screwed up!")
async def sorry_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Screwed up in front of who?", name="user")]
):
    me = ctx.client.cache.get_me()
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


@emotions.include
@arc.slash_subcommand("handshake", "Shake hands with someone.")
async def handshake_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Who are you shaking hands with?", name="user")]
):
    me = ctx.client.cache.get_me()
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


@emotions.include
@arc.slash_subcommand("tickle", "Tickle someone.")
async def tickle_command(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Who to tickle?", name="user")]
):
    me = ctx.client.cache.get_me()
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

@emotions.include
@arc.slash_subcommand("midfinger", "Fun third finger.")
async def midfinger_command(ctx: arc.GatewayContext):
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


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
