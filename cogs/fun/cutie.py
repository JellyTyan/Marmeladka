import nekos
import lightbulb
import hikari
import asyncio

import functions.cutie_func as cutieFunc

loader = lightbulb.Loader()

group = lightbulb.Group("commands.cutie.name", "commands.cutie.description", dm_enabled=False, localize=True)

@group.register
class FrogImage(
    lightbulb.SlashCommand,
    name="commands.frogimage.name",
    description="commands.frogimage.description",
    localize=True
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        frog_image_url = await cutieFunc.get_random_image(query='frog')

        embed = hikari.Embed(description="Ква-ква-ква", color=0x53377A)
        embed.set_image(frog_image_url)
        embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
        response = await ctx.respond(embed=embed)
        await asyncio.sleep(300)
        await ctx.delete_response(response)


@group.register
class CatImage(
    lightbulb.SlashCommand,
    name="commands.catimage.name",
    description="commands.catimage.description",
    localize=True
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        embed = hikari.Embed(description="Мяу-мя", color=0x53377A)
        embed.set_image(nekos.cat())
        embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
        response = await ctx.respond(embed=embed)
        await asyncio.sleep(300)
        await ctx.delete_response(response)


@group.register
class FoxImage(
    lightbulb.SlashCommand,
    name="commands.foximage.name",
    description="commands.foximage.description",
    localize=True
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        fox_image_url = await cutieFunc.get_random_fox_image()

        embed = hikari.Embed(description="Фряя", color=0x53377A)
        embed.set_image(fox_image_url)
        embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
        response = await ctx.respond(embed=embed)
        await asyncio.sleep(300)
        await ctx.delete_response(response)


@group.register
class GooseImage(
    lightbulb.SlashCommand,
    name="commands.gooseimage.name",
    description="commands.gooseimage.description",
    localize=True
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        embed = hikari.Embed(description="ГАААА", color=0x53377A)
        embed.set_image(await cutieFunc.get_goose_image("goose"))
        embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
        response = await ctx.respond(embed=embed)
        await asyncio.sleep(300)
        await ctx.delete_response(response)


loader.command(group)
