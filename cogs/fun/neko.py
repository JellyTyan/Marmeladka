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

# @commands.command()
# async def hentai(self, ctx, api_type=""):
#     if ctx.message.channel.nsfw:
#         api_types = ['femdom', 'classic', 'ngif', 'erofeet', 'erok', 'les',
#                      'hololewd', 'lewdk', 'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri',
#                      'tits', 'pussy_jpg', 'cum_jpg', 'pussy', 'lewdkemo', 'lewd', 'cum', 'spank',
#                      'smallboobs', 'Random_hentai_gif', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat',
#                      'feet', 'smug', 'kemonomimi', 'solog', 'holo', 'bj', 'woof', 'yuri', 'trap', 'anal',
#                      'blowjob', 'holoero', 'feed', 'gasm', 'hentai', 'futanari', 'ero', 'solo', 'pwankg', 'eron',
#                      'erokemo']
#         if api_type in api_types:
#             req = requests.get(f'https://nekos.life/api/v2/img/{api_type}')
#             try:
#                 if req.status_code != 200:
#                     print("Unable to obtain image")
#                 api_json = json.loads(req.text)
#                 url = api_json["url"]

#                 message = await ctx.send(embed=teapot.messages.downloading())
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get(url) as resp:
#                         if resp.status != 200:
#                             print(resp.status)
#                             print(await resp.read())
#                             return await ctx.send('Could not download file...')
#                         data = io.BytesIO(await resp.read())
#                         await ctx.send(
#                             file=discord.File(data, f'SPOILER_HENTAI.{url.split("/")[-1].split(".")[-1]}'))
#                         await message.delete()
#             except:
#                 await ctx.send(embed=teapot.messages.error(f"obtaining image ({req.status_code})"))
#         else:
#             await ctx.send(embed=teapot.messages.invalidargument(", ".join(api_types)))
#     else:
#         await ctx.send("This command only works in NSFW channels!")


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
