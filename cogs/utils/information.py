import lightbulb
import hikari

loader = lightbulb.Loader()

group = lightbulb.Group("commands.biography.name", "commands.biography.description", dm_enabled=False, localize=True)


@group.register
class MarmeladkaBioCommand(
    lightbulb.SlashCommand,
    name="commands.marmeladkabio.name",
    description="commands.marmeladkabio.description",
    dm_enabled=False,
    localize=True
):
    @lightbulb.invoke
    async def marmeladka_bio(self, ctx: lightbulb.Context) -> None:
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


@group.register
class ZefirkaBioCommand(
    lightbulb.SlashCommand,
    name="commands.zefirkabio.name",
    description="commands.zefirkabio.description",
    dm_enabled=False,
    localize=True
):
    @lightbulb.invoke
    async def zefirka_bio(self, ctx: lightbulb.Context) -> None:
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


@group.register
class ShocomelkaBioCommand(
    lightbulb.SlashCommand,
    name="commands.shocomelkabio.name",
    description="commands.shocomelkabio.description",
    dm_enabled=False,
    localize=True
):
    @lightbulb.invoke
    async def shocomelka_bio(self, ctx: lightbulb.Context) -> None:
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


@group.register
class MilkaBioCommand(
    lightbulb.SlashCommand,
    name="commands.milkabio.name",
    description="commands.milkabio.description",
    dm_enabled=False,
    localize=True
):
    @lightbulb.invoke
    async def milka_bio(self, ctx: lightbulb.Context) -> None:
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


loader.command(group)
