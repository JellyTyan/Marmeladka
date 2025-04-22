import arc
import hikari

plugin = arc.GatewayPlugin("Informaton", invocation_contexts=[hikari.ApplicationContextType.GUILD])

bio = plugin.include_slash_group("biography", "Learn the story of one of the heroines!", autodefer=arc.AutodeferMode.ON)


@bio.include
@arc.slash_subcommand("marmeladkabio", "Find out more about Marmeladka!")
async def marmeladka_bio(ctx: arc.GatewayContext) -> None:
    embed = hikari.Embed(
        title="Приветик, я Мармеладка!",
        description="""
            🦊✨ Лисичка заботы и уюта на сервере Желешки! ✨🦊\n
            ❤️ Тепло, забота и внимание — моя суперсила! ❤️\n
            🍵 Выполняю главный функционал сервера, чтобы вам всегда было уютно и весело! 🍪\n
            🌈 А знаете, почему меня зовут Мармеладка? Говорят, что я сладкая, как мармелад, и могу согреть ваше сердечко, даже если у вас тяжёлый день! 🌟💛
        """,
        color=0xFF6F61,
    )
    embed.set_image("https://static.zerochan.net/Senko.%28Sewayaki.Kitsune.no.Senko-san%29.full.2738566.jpg")
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bio.include
@arc.slash_subcommand("zefirkabio", "Find out more about Zefirka!")
async def zefirka_bio(ctx: arc.GatewayContext) -> None:
    embed = hikari.Embed(
        title="Привет, я Зефирка!",
        description="""
            🦊🍡 Бедни и голодни лисичка! 🍡🦊\n
            🎶 Помогаю расслабиться и наслаждаться музыкой на сервере. 🎧\n
            🌙 Говорят, что мои плейлисты уносят вас прямо в мир грёз... ✨\n
            🌟 Немного загадочная, но всегда на вашей стороне! 💫
        """,
        color=0xFFC0CB,  # Розовый цвет, как зефир
    )
    embed.set_image("https://safebooru.org//samples/3072/sample_af8dc25e5edbf26c3fb0981dbd2f917fc55513eb.jpg?5213035")
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bio.include
@arc.slash_subcommand("shocomelkabio", "Find out more about Shocomelka!")
async def shocomelka_bio(ctx: arc.GatewayContext) -> None:
    embed = hikari.Embed(
        title="Привет, я Шокомелька!",
        description="""
            🎵✨ Мили Енотик, которая знает, как создать атмосферу. ✨🎵\n
            🍫 Я подбираю музыку в зависимости от вашего настроения — от мягкого lofi до вдохновляющих мелодий. 🎼\n
            🛋️ Заходите на трибуну, берите плед и чашку какао — я позабочусь, чтобы вам было уютно. ☕💛
        """,
        color=0x8B4513,
    )
    embed.set_image("https://preview.redd.it/7x5n9tieagd41.png?auto=webp&s=ba3405f28de9a249e1c9972bb8a3214876ede29d")
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bio.include
@arc.slash_subcommand("milkabio", "Find out more about Milka!")
async def milka_bio(ctx: arc.GatewayContext) -> None:
    embed = hikari.Embed(
        title="Привет, я Милка!",
        description="""
            🍫 Немного другая версия Зефирки — более мягкая и весёлая! 🍫\n
            🥛 Я люблю уют и спокойствие. Думаю, что мягкость — моя суперсила. ☁️\n
            🌸 Вместе мы сделаем наш сервер особенным! 💖
        """,
        color=0xFFFFFF,
    )
    embed.set_image("https://static.wikia.nocookie.net/mudae/images/0/05/Yozora_%28SKnS%292.png/revision/latest/scale-to-width/360?cb=20210420071604")
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
