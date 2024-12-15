""" Module for generating random neko pictures"""
import disnake
from disnake.ext import commands

from core.functions.animeFunc import get_anime_image, get_waifu_image

def build_embed(x: str):
    embed = disnake.Embed(description="Анимееее", color=0x53377A)
    embed.set_image(url=get_anime_image(x))
    embed.set_footer(text="Сообщение удалиться через 5 минут", icon_url="https://i.gifer.com/ZKZg.gif")
    return embed

class Neko(commands.Cog):
    """Neko!!! :3"""

    def __init__(self, bot):
        """Initialize neko class"""
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    async def аниме(self, inter):
        pass

    @аниме.sub_command(name="неко", description="Кошко-девочки")
    async def neko(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(embed=build_embed("neko"))
        response = await inter.original_message()
        await response.delete(delay=300)

    @аниме.sub_command(name="лисы", description="Лисы-девочки, да?")
    async def fox_girl(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(embed=build_embed("fox_girl"))
        response = await inter.original_message()
        await response.delete(delay=300)

    @аниме.sub_command(name="вайфу", description="Ваши и не только вафу")
    async def waifu(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(description="Вайфууу", color=0x53377A)
        embed.set_image(url=get_waifu_image())
        embed.set_footer(text="Сообщение удалиться через 5 минут", icon_url="https://i.gifer.com/ZKZg.gif")

        await inter.send(embed=embed)
        response = await inter.original_message()
        await response.delete(delay=300)

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


def setup(bot):
    bot.add_cog(Neko(bot))
