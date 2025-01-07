import lightbulb
import hikari

plugin = lightbulb.Plugin("Information")

@plugin.command
@lightbulb.command("био", "Узнай историю одной из героинь!", app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def bio(ctx: lightbulb.Context) -> None:
    pass

@bio.child
@lightbulb.command("мармеладка", "Узнай больше о Мармеладке!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bioMarmeladka(ctx: lightbulb.Context) -> None:
    guild_emojis = ctx.get_guild().get_emojis()
    emoji_mhm = lightbulb.utils.get(guild_emojis, name="mhm")
    emoji_hmury = lightbulb.utils.get(guild_emojis, name="hmury")

    embed = hikari.Embed(
        title="Приветик, я Мармеладка!",
        description=f"""
            {emoji_mhm} Лисичка для сервера Желешки {emoji_mhm}\n
            ❤️ У нас интима не было ❤️ \n
            {emoji_hmury} Выполняю весь гланвый функционал сервера! {emoji_hmury}
        """,
    )
    embed.set_image("https://img.artpal.com/320651/6-20-6-10-16-5-45m.jpg")
    await ctx.respond(embed=embed)


@bio.child
@lightbulb.command("зефирка", "Узнай больше о Зефирке!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bioZefirka(ctx: lightbulb.Context) -> None:
    guild_emojis = ctx.get_guild().get_emojis()
    emoji_uwu = lightbulb.utils.get(guild_emojis, name="cool")
    emoji_plak = lightbulb.utils.get(guild_emojis, name="angry")
    emoji_wink = lightbulb.utils.get(guild_emojis, name="wink")

    embed = hikari.Embed(
        title="Хай, я Зефирка!",
        description=f"""
            {emoji_uwu} Бели Голодни Лисичка {emoji_uwu}\n
            {emoji_wink} У нас был тройничёк {emoji_wink}\n
            {emoji_plak} Могу проигрывать для тебя композиции {emoji_plak}
            """,
    )
    embed.set_image("https://i1.sndcdn.com/artworks-000542697177-o00sgu-t500x500.jpg")
    await ctx.respond(embed=embed)


@bio.child
@lightbulb.command("шокомелька", "Узнай о нашей подружке!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bioShocomelka(ctx: lightbulb.Context) -> None:
    guild_emojis = ctx.get_guild().get_emojis()
    emoji_woah = lightbulb.utils.get(guild_emojis, name="kogasawoah")
    emoji_dead = lightbulb.utils.get(guild_emojis, name="mokoudeadinside")

    embed = hikari.Embed(
        title="Приветик, я Шокомелька",
        description=f"""
            🤎 Мили енотик и подружка 🤎 \n
            {emoji_woah} У него уже гарем {emoji_woah}\n
            {emoji_dead} По настроению сижу у себя и слушаю музыку {emoji_dead}
            """,
    )
    embed.set_image("https://cdn.discordapp.com/attachments/1109526498299359303/1152864808752914503/cdum6zjvawx51.png")
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
