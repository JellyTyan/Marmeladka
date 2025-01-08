import textwrap
from io import BytesIO

import lightbulb
import hikari
from PIL import Image, ImageDraw, ImageFont

from functions.user_profile_func import UserProfileFunc

plugin = lightbulb.Plugin("UserProfile")

@plugin.command
@lightbulb.option("user", "Чей профиль взглянуть?", hikari.User, required=False)
@lightbulb.command("профиль", "Профиль пользователя.", auto_defer=True, app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def user_profile(ctx: lightbulb.Context) -> None:
    user: hikari.User = ctx.options.user or ctx.author

    profile_image = Image.open('src/img/userProfile.png')
    avatar_image = BytesIO(await user.display_avatar_url.read())
    img = Image.open(avatar_image).resize((252, 252))

    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + img.size, fill=255)
    rounded_avatar = Image.new('RGBA', img.size)
    rounded_avatar.paste(img, (0, 0), mask)

    profile_image.paste(rounded_avatar, (56, 64), rounded_avatar)

    idraw = ImageDraw.Draw(profile_image)
    text_font = ImageFont.truetype('src/fonts/userProfile.otf', size=43)

    user_name = truncate_text(user.display_name, 18)
    idraw.text((323, 170), user_name, font=text_font, fill=(0, 0, 0))

    user_message_count = await UserProfileFunc().get_message_count(user.id)
    user_voice_time = await UserProfileFunc().get_voice_count(user.id)
    user_bump_count = await UserProfileFunc().get_bump_count(user.id)
    user_invite_count = await UserProfileFunc().get_invite_count(user.id)

    idraw.text((211, 703), str(user_message_count), font=text_font, anchor="ms", fill=(0, 0, 0))
    idraw.text((595, 703), str(user_voice_time), font=text_font, anchor="ms", fill=(0, 0, 0))
    idraw.text((211, 846), str(user_bump_count), font=text_font, anchor="ms", fill=(0, 0, 0))
    idraw.text((595, 846), str(user_invite_count), font=text_font, anchor="ms", fill=(0, 0, 0))

    user_tag = await UserProfileFunc().get_tag(user.id)
    tag_font = ImageFont.truetype('src/fonts/userProfile.otf', size=37)
    idraw.text((511, 268), str(user_tag), font=tag_font, anchor="ms", fill=(0, 0, 0))

    user_biography = await UserProfileFunc().get_biograpgy(user.id)
    biography_font = ImageFont.truetype('src/fonts/userProfile.otf', size=38)
    wrapper = textwrap.TextWrapper(width=45, placeholder='...', break_long_words=True, max_lines=4)
    biography = wrapper.fill(text=str(user_biography))

    for offset in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        idraw.multiline_text((64 + offset[0], 420 + offset[1]), biography, font=biography_font, fill=(0, 0, 0))
    idraw.multiline_text((64, 420), biography, font=biography_font, fill=(255, 255, 255))

    with BytesIO() as image_binary:
        profile_image.save(image_binary, 'PNG')
        image_binary.seek(0)

        embedProfile = hikari.Embed()
        embedProfile.set_image(image_binary)
        embedProfile.set_footer(text="Сообщение удалиться через 5 минут", icon="https://i.gifer.com/ZKZg.gif")

        await ctx.respond(embed=embedProfile, delete_after=300)

def truncate_text(text, max_length) -> str:
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
