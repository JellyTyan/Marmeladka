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
            {emoji_mhm} Лисичка заботы и уюта на сервере Желешки! {emoji_mhm}\n
            ❤️ Забота и внимание — моя суперсила! ❤️ \n
            {emoji_hmury} Выполняю главный функционал сервера, чтобы вам всегда было уютно и весело! {emoji_hmury}\n
            🌟 А знаете, почему меня зовут Мармеладка? Говорят, что я сладкая, как мармелад, и могу согреть ваше сердечко, даже если у вас тяжёлый день! 🌟
        """,
        color=0xFF6F61,
    )
    embed.set_image("https://static.zerochan.net/Senko.%28Sewayaki.Kitsune.no.Senko-san%29.full.2738566.jpg")
    await ctx.respond(embed=embed)


@bio.child
@lightbulb.command("зефирка", "Узнай больше о Зефирке!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bioZefirka(ctx: lightbulb.Context) -> None:
    guild_emojis = ctx.get_guild().get_emojis()
    emoji_fox = lightbulb.utils.get(guild_emojis, name="fox")

    embed = hikari.Embed(
        title="Привет, я Зефирка!",
        description=f"""
            {emoji_fox} Бедни и голодни лисичка! {emoji_fox}\n
            🎵 Помогаю расслабиться и наслаждаться музыкой на сервере.\n
            🌙 Говорят, что мои плейлисты уносят вас прямо в мир грёз.\n
            🌟 Немного загадочная, но всегда на вашей стороне! 🌟
        """,
        color=0xFFC0CB,  # Розовый цвет, как зефир
    )
    embed.set_image("https://safebooru.org//samples/3072/sample_af8dc25e5edbf26c3fb0981dbd2f917fc55513eb.jpg?5213035")
    await ctx.respond(embed=embed)


@bio.child
@lightbulb.command("шокомелька", "Узнай больше о Шокомельке!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bioShokomelka(ctx: lightbulb.Context) -> None:
    guild_emojis = ctx.get_guild().get_emojis()
    emoji_lofi = lightbulb.utils.get(guild_emojis, name="lofi")

    embed = hikari.Embed(
        title="Привет, я Шокомелька!",
        description=f"""
            {emoji_lofi} Мили Енотик, которая знает, как создать атмосферу. {emoji_lofi}\n
            🍫 Я подбираю музыку в зависимости от вашего настроения — от мягкого lofi до вдохновляющих мелодий.\n
            🛋️ Заходите на трибуну, берите плед и чашку какао. Я позабочусь, чтобы вам было уютно. 🛋️
        """,
        color=0x8B4513,
    )
    embed.set_image("https://preview.redd.it/7x5n9tieagd41.png?auto=webp&s=ba3405f28de9a249e1c9972bb8a3214876ede29d")
    await ctx.respond(embed=embed)


@bio.child
@lightbulb.command("милка", "Узнай больше о Милке!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bioMilka(ctx: lightbulb.Context) -> None:
    guild_emojis = ctx.get_guild().get_emojis()
    emoji_choco = lightbulb.utils.get(guild_emojis, name="choco")

    embed = hikari.Embed(
        title="Привет, я Милка!",
        description=f"""
            {emoji_choco} Немного другая версия Зефирки — более мягкая и весёлая! {emoji_choco}\n
            🥛 Я люблю уют и спокойствие. Думаю, что мягкость — моя суперсила.\n
            🌸 Вместе мы сделаем наш сервер особенным! 🌸
        """,
        color=0xFFFFFF,
    )
    embed.set_image("https://static.wikia.nocookie.net/mudae/images/0/05/Yozora_%28SKnS%292.png/revision/latest/scale-to-width/360?cb=20210420071604")
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
