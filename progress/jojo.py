import asyncio

import lightbulb
import hikari
import ongaku

from main import client

plugin = lightbulb.Plugin("Jojo")


@plugin.command
@lightbulb.command("jojo", "Jojo")
@lightbulb.implements(lightbulb.PrefixCommand)
async def jojo(ctx: lightbulb.Context) -> None:
    client.create_session(
        ssl=False,
        name="yanwu",
        host="lava.catfein.com",
        port=4000,
        password="catfein"
    )

    player = client.create_player(guild=1149398120694825061)

    print(player)

    await player.connect(1149398121558855681)

    track = await client.rest.load_track("src/audio/jojo.mp3")

    await player.play(track)


@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    author_id = event.author_id
    bot = event.app.rest
    try:
        if (author_id == 1109771047709978716 or author_id == 1233085999031255205):
            embed = event.embeds[0]

            if embed.description is None:
                return

            if embed and any(keyword in embed.description.lower() for keyword in ["jojo", "джоджо", "жожо", "ジョジョ"]):
                if any(keyword in embed.description.lower() for keyword in ["Добавлено в очередь"]):
                    return

                guild = event.get_guild()
                if guild is None:
                    return

                member_voice_state = guild.get_voice_state(author_id)
                if member_voice_state is None:
                    return

                member_voice_channel = member_voice_state.channel_id
                if member_voice_channel is None:
                    return

                print(client)

                player = client.create_player(guild=guild.id)

                print(player)

                await player.connect(member_voice_channel)

                track = await client.rest.load_track("src/audio/jojo.mp3")

                print(track)

                await player.play(track)

                # vc.play(disnake.FFmpegPCMAudio("src/audio/jojo.mp3"))

                # while vc.is_playing():
                #     await asyncio.sleep(1)

                # await vc.disconnect()
    except Exception:
        pass


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
