""" Module for generating random neko pictures"""
import hikari
import lightbulb

from functions.anime_func import get_anime_image, get_waifu_image

plugin = lightbulb.Plugin("Nekos")


@plugin.command
@lightbulb.command("аниме", "Анимешные картинки.", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def anime(ctx: lightbulb.Context) -> None:
    pass


@anime.child
@lightbulb.command("неко", "Кошко-девочки")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def neko(ctx: lightbulb.Context) -> None:
    await ctx.respond(embed=await build_embed("neko"), delete_after=300)


@anime.child
@lightbulb.command("лисы", "Лисы-девочки, да?")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def fox_girl(ctx: lightbulb.Context) -> None:
    await ctx.respond(embed=await build_embed("fox_girl"), delete_after=300)


@anime.child
@lightbulb.command("вайфу", "Ваши и не только вафу!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def waifu(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(description="Вайфууу", color=0x53377A)
    embed.set_image(await get_waifu_image())
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")

    await ctx.respond(embed=embed, delete_after=300)

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
    embed = hikari.Embed(description="Анимееее", color=0x53377A)
    embed.set_image(await get_anime_image(x))
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
    return embed

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
