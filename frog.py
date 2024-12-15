import disnake
from disnake.ext import commands


class Frog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx: disnake.Message):
        if "ква?" in ctx.content.lower():
            await ctx.reply("Ква!")


def setup(bot):
    bot.add_cog(Frog(bot))
