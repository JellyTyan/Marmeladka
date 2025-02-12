""" Module for generating random neko pictures"""
import hikari
import lightbulb
import asyncio

from functions.anime_func import get_nekos_gif

loader = lightbulb.Loader()

group = lightbulb.Group("аниме", "Анимешные картинки.", dm_enabled=False)


@group.register
class NekoCommand(
    lightbulb.SlashCommand,
    name="неко",
    description="Кошко-девочки"
):

    @lightbulb.invoke
    async def neko(self, ctx: lightbulb.Context) -> None:
        response = await ctx.respond(embed=await build_embed("neko"))
        await asyncio.sleep(300)
        await ctx.delete_response(response)


@group.register
class FoxCommand(
    lightbulb.SlashCommand,
    name="лисы",
    description="Лисы-девочки, да?"
):

    @lightbulb.invoke
    async def fox_girl(self, ctx: lightbulb.Context) -> None:
        response = await ctx.respond(embed=await build_embed("kitsune"))
        await asyncio.sleep(300)
        await ctx.delete_response(response)


@group.register
class WaifuCommand(
    lightbulb.SlashCommand,
    name="вайфу",
    description="Ваши и не только вафу!"
):

    @lightbulb.invoke
    async def waifu(self, ctx: lightbulb.Context) -> None:
        response = await ctx.respond(embed=await build_embed("waifu"))
        await asyncio.sleep(300)
        await ctx.delete_response(response)

@group.register
class HusbandoCommand(
    lightbulb.SlashCommand,
    name="хусбандо",
    description="Ваши и не только вафу!"
):

    @lightbulb.invoke
    async def husbando(self, ctx: lightbulb.Context) -> None:
        response = await ctx.respond(embed=await build_embed("husbando"))
        await asyncio.sleep(300)
        await ctx.delete_response(response)

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
    embed.set_image(await get_nekos_gif(x))
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")
    return embed

loader.command(group)
