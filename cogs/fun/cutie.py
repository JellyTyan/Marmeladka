import arc
import hikari
import nekos

import functions.cutie_func as cutieFunc

plugin = arc.GatewayPlugin("Cutie", invocation_contexts=[hikari.ApplicationContextType.GUILD])

cutie = plugin.include_slash_group("cutie", "So cuute!", autodefer=arc.AutodeferMode.ON)

@cutie.include
@arc.slash_subcommand("ribbit", "Ribbit-ribbit-ribbit")
async def frog_image(ctx: arc.GatewayContext) -> None:
    frog_image_url = await cutieFunc.get_random_image(query='frog')

    embed = hikari.Embed(description="Ribiir-ribbit-ribibit", color=0x53377A)
    embed.set_image(frog_image_url)
    embed.set_footer(text="The message will be deleted in 5 minutes.", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


@cutie.include
@arc.slash_subcommand("meow", "Meow-meow-meow")
async def cat_image(ctx: arc.GatewayContext) -> None:
    embed = hikari.Embed(description="Meeew :3", color=0x53377A)
    embed.set_image(nekos.cat())
    embed.set_footer(text="The message will be deleted in 5 minutes.", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


@cutie.include
@arc.slash_subcommand("bark", "Bark-bark-bark")
async def fox_image(ctx: arc.GatewayContext) -> None:
    fox_image_url = await cutieFunc.get_random_fox_image()

    embed = hikari.Embed(description="Frrr", color=0x53377A)
    embed.set_image(fox_image_url)
    embed.set_footer(text="The message will be deleted in 5 minutes.", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


@cutie.include
@arc.slash_subcommand("honk", "Hooooonk")
async def goose_image(ctx: arc.GatewayContext) -> None:
    embed = hikari.Embed(description="HOOOOONK", color=0x53377A)
    embed.set_image(await cutieFunc.get_goose_image("goose"))
    embed.set_footer(text="The message will be deleted in 5 minutes.", icon="https://i.gifer.com/ZKZg.gif")
    await ctx.respond(embed=embed, delete_after=300)


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
