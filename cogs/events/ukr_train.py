import lightbulb
import hikari

from utils.create_embed import create_embed
from config.config_manager import ConfigManager

config_manager = ConfigManager()

loader = lightbulb.Loader()


@loader.listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    member = event.member

    if member.is_bot:
        return

    if member:
        UKR_CHANNEL_ID = config_manager.get_config_value("UKR_CHANNEL_ID")
        ukr_channel = await event.app.rest.fetch_channel(int(UKR_CHANNEL_ID))

        if isinstance(ukr_channel, hikari.GuildTextChannel):
            embed = create_embed(
                title="Зустрічайте",
                description=f"{member.mention} прибув на наш сервер.",
                image_url="https://cdn.discordapp.com/attachments/1108629194788847637/1113354643691536465/Untitled_video_-_Made_with_Clipchamp_3.gif"
            )
            await ukr_channel.send(embed=embed)

        embed_welcome_user = create_embed(
            title=f"Ahoy, {member.nickname}!",
            description="""
                Welcome to Jelly's Server!
                Read the rules and start your way in our community.

                Good Luck!
            """,
            image_url="https://media.discordapp.net/attachments/1108629194788847637/1265273109242577007/2728FFF7-AEAD-4373-862D-C5E712E82102.gif?ex=66a0e8e8&is=669f9768&hm=c61b4ef619261cb23d54459a6a35cc665cd0acb1faef583ae28b3289d7541b24&=&width=600&height=337"
        )

        try:
            await member.send(content="||https://discord.com/invite/77keb7smna||", embed=embed_welcome_user)
        except Exception:
            return


@loader.listener(hikari.MemberDeleteEvent)
async def on_member_leave(event: hikari.MemberDeleteEvent) -> None:
    member = event.old_member

    if member is None:
        return

    if member.is_bot:
        return

    UKR_CHANNEL_ID = config_manager.get_config_value("UKR_CHANNEL_ID")
    ukr_channel = await event.app.rest.fetch_channel(int(UKR_CHANNEL_ID))

    if isinstance(ukr_channel, hikari.GuildTextChannel):
        embed = create_embed(
            title="Прощавай",
            description=f"{member.mention} поїхав від нас.",
            image_url="https://cdn.discordapp.com/attachments/1109526498299359303/1138139334550241291/gman-toes.gif"
        )
        await ukr_channel.send(embed=embed)
