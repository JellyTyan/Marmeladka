import nekos
import lightbulb
import hikari

import functions.cutie_func as cutieFunc
from functions.anime_func import get_anime_image


plugin = lightbulb.Plugin("Cutie")


@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("cutie", "Милота")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def cute(ctx: lightbulb.Context):
    pass


@cute.child
@lightbulb.command("ква", "Ква-ква-ква")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def rand_frog_image(ctx: lightbulb.Context):
    frog_image_url = await cutieFunc.get_random_image(query='frog')

    embed = hikari.Embed(description="Ква-ква-ква", color=0x53377A)
    embed.set_image(frog_image_url)
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


@cute.child
@lightbulb.command("мяу", "Мяяяяяяя")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def rand_cat_image(ctx: lightbulb.Context):
    embed = hikari.Embed(description="Мяу-мя", color=0x53377A)
    embed.set_image(nekos.cat())
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed)


@cute.child
@lightbulb.command("фыр", "Фыр-фыр-фыр")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def rand_fox_image(ctx: lightbulb.Context):
    fox_image_url = await cutieFunc.get_random_fox_image()

    embed = hikari.Embed(description="Фряя", color=0x53377A)
    embed.set_image(fox_image_url)
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


@cute.child
@lightbulb.command("га", "Га-га-га-га")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def rand_goose_image(ctx: lightbulb.Context):
    embed = hikari.Embed(description="ГАААА", color=0x53377A)
    embed.set_image(await get_anime_image("goose"))
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
