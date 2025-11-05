""" Module for generating random neko pictures"""
import arc
import hikari

from functions.anime_func import get_nekos_gif

plugin = arc.GatewayPlugin("NekoPy", invocation_contexts=(hikari.ApplicationContextType(0), ))

neko = plugin.include_slash_group("anime", "Anime images.", autodefer=arc.AutodeferMode.ON)


@neko.include
@arc.slash_subcommand("neko", "Cat-girls")
async def neko_girl(ctx: arc.GatewayContext) -> None:
    await ctx.respond(embed=await build_embed("neko"), delete_after=300)

@neko.include
@arc.slash_subcommand("kitsune", "Foxy girls, huh?")
async def kitsune_girl(ctx: arc.GatewayContext) -> None:
        await ctx.respond(embed=await build_embed("kitsune"), delete_after=300)


@neko.include
@arc.slash_subcommand("waifu", "Yours and not just wafu!")
async def waifu(ctx: arc.GatewayContext) -> None:
    await ctx.respond(embed=await build_embed("waifu"), delete_after=300)


@neko.include
@arc.slash_subcommand("husbando", "Yours and not just men!")
async def husbando(ctx: arc.GatewayContext) -> None:
    await ctx.respond(embed=await build_embed("husbando"), delete_after=300)


async def build_embed(x: str):
    embed = hikari.Embed(color=0x53377A)
    embed.set_image(await get_nekos_gif(x))
    embed.set_footer(text="The message will be deleted in 5 minutes.", icon="https://i.gifer.com/ZKZg.gif")
    return embed


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
