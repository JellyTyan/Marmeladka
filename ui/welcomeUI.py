import json
from typing import Optional

import hikari
import miru

from functions.user_profile_func import UserProfileFunc
from ui.profileUI import EditProfileButton
from utils.create_embed import create_embed

role_color_mapping = {
    "Red": 1106244113587785829,
    "Orange": 1106244211138887780,
    "Yellow": 1106244235411345408,
    "Green": 1106244181602603038,
    "Blue": 1106244160958255225,
    "Aqua": 1124257706321125439,
    "Pink": 1121558196046270466,
    "Purple": 1106250927805042708,
    "Grey": 1135230107095662602,
    "White": 1135231008413855795,
}

class MainView(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(timeout=None, *args, **kwargs)

    @miru.text_select(
        placeholder="📚 ┋ Server member rules",
        options=[
            miru.SelectOption(label="General Provisions", emoji="📱"),
            miru.SelectOption(label="Posting Links", emoji="🖥️"),
            miru.SelectOption(label="Voice Chat", emoji="🎤"),
            miru.SelectOption(label="Nickname Usage", emoji="🏷️"),
            miru.SelectOption(label="Private Channels", emoji="⛔"),
        ], min_values=1, max_values=1, custom_id="rules_select_menu")
    async def rules_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.author.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        selected_option = select.values[0]
        embedRules = hikari.Embed()

        if selected_option == "General Provisions":
            embedRules = create_embed(
                title=language_json["MainView"]["rules_select"]["options"]["General_Provisions"]["embed"]["title"],
                description=language_json["MainView"]["rules_select"]["options"]["General_Provisions"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png",
                )

        elif selected_option == "Posting Links":
            embedRules = create_embed(
                title=language_json["MainView"]["rules_select"]["options"]["Restrictions_links"]["embed"]["title"],
                description=language_json["MainView"]["rules_select"]["options"]["Restrictions_links"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

        elif selected_option == "Voice Chat":
            embedRules = create_embed(
                title=language_json["MainView"]["rules_select"]["options"]["Voice_Chat"]["embed"]["title"],
                description=language_json["MainView"]["rules_select"]["options"]["Voice_Chat"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

        elif selected_option == "Nickname Usage":
            embedRules = create_embed(
                title=language_json["MainView"]["rules_select"]["options"]["Nickname_Usage"]["embed"]["title"],
                description=language_json["MainView"]["rules_select"]["options"]["Nickname_Usage"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

        elif selected_option == "Private Channels":
            embedRules = create_embed(
                title=language_json["MainView"]["rules_select"]["options"]["Private_Channels"]["embed"]["title"],
                description=language_json["MainView"]["rules_select"]["options"]["Private_Channels"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

        embedRules.set_footer(language_json["MainView"]["rules_select"]["options"]["General_Provisions"]["embed"]["footer"])
        await ctx.respond(embed=embedRules, flags=hikari.MessageFlag.EPHEMERAL)

    @miru.text_select(
        placeholder="🛠️ ┋ Server functionality",
        options=[
            miru.SelectOption(label="Sweets", emoji="🥞"),
            miru.SelectOption(label="Customization", emoji="🎨"),
            miru.SelectOption(label="Language", emoji="🌍"),
        ], min_values=1, max_values=1, custom_id="functions_select_menu"
    )
    async def functions_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.author.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        selected_option = select.values[0]

        if selected_option == "Sweets":
            embedFunc = create_embed(
                color=0x313338,
                title=language_json["MainView"]["functions_select"]["options"]["Sweets"]["embed"]["title"],
                description=language_json["MainView"]["functions_select"]["options"]["Sweets"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

            sweet_view = SelectMainBots()

            await ctx.respond(embed=embedFunc, components=sweet_view, flags=hikari.MessageFlag.EPHEMERAL)

            ctx.client.start_view(sweet_view)

        elif selected_option == "Customization":
            embedFunc = create_embed(
                color=0x313338,
                title=language_json["MainView"]["functions_select"]["options"]["Customization"]["embed"]["title"],
                description=language_json["MainView"]["functions_select"]["options"]["Customization"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png"
            )

            color_view = SelectColor().add_item(EditProfileButton())

            await ctx.respond(embed=embedFunc, components=color_view, flags=hikari.MessageFlag.EPHEMERAL)

            ctx.client.start_view(color_view)

        elif selected_option == "Language":
            embedFunc = create_embed(
                color=0x313338,
                title=language_json["MainView"]["functions_select"]["options"]["Language"]["embed"]["title"],
                description=language_json["MainView"]["functions_select"]["options"]["Language"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/1201221560267190446/1354433309815472269/anime-sign.gif?ex=67e545d1&is=67e3f451&hm=1126cfe592feecb4fc7bc63b4feb56218625985b100c3c5fdea666fde3f2ff4d&"
            )

            language_view = SelectLanguage()

            await ctx.respond(embed=embedFunc, components=language_view, flags=hikari.MessageFlag.EPHEMERAL)

            ctx.client.start_view(language_view)


class SelectMainBots(miru.View):
    @miru.text_select(
        placeholder="🧁 ┋ Who's up now?",
        options=[
            miru.SelectOption(label="Marmeladka", emoji="🧡"),
            miru.SelectOption(label="Zefirka", emoji="🤍"),
            miru.SelectOption(label="Shocomelka", emoji="🤎"),
            miru.SelectOption(label="Milka", emoji="💜"),
            miru.SelectOption(label="Kriska", emoji="🐀"),
        ], min_values=1, max_values=1, custom_id="bots_select_menu"
    )
    async def callback(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.author.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        selected_option = select.values[0]

        embedFunc = hikari.Embed()

        if selected_option == "Marmeladka":
            embedFunc = create_embed(
                color=0xFFA500,
                title=language_json["SelectMainBots"]["options"]["Marmeladka"]["embed"]["title"],
                description=language_json["SelectMainBots"]["options"]["Marmeladka"]["embed"]["description"],
                image_url="https://c4.wallpaperflare.com/wallpaper/138/566/373/anime-girls-sewayaki-kitsune-no-senko-san-fox-girl-yellow-eyes-portrait-display-hd-wallpaper-preview.jpg"
            )

        elif selected_option == "Zefirka":
            embedFunc = create_embed(
                color=0xFFFFFF,
                title=language_json["SelectMainBots"]["options"]["Zefirka"]["embed"]["title"],
                description=language_json["SelectMainBots"]["options"]["Zefirka"]["embed"]["description"],
                image_url="https://preview.redd.it/shiro-san-rtx-on-v0-u7i864vg31sb1.png?auto=webp&s=6e07bf650a35f79eb4ea69d58af218c02c98cfb9"
            )

        elif selected_option == "Shocomelka":
            embedFunc = create_embed(
                color=0x964B00,
                title=language_json["SelectMainBots"]["options"]["Shocomelka"]["embed"]["title"],
                description=language_json["SelectMainBots"]["options"]["Shocomelka"]["embed"]["description"],
                image_url="https://cdn.discordapp.com/attachments/1109526498299359303/1322581174727479327/EdL9VcH.png?ex=67716534&is=677013b4&hm=34ab50dd67868bac2be59eb4577392b178e03c3cd7921c8a5494a4f8ca434531&"
            )

        elif selected_option == "Milka":
            embedFunc = create_embed(
                color=0xA020F0,
                title=language_json["SelectMainBots"]["options"]["Milka"]["embed"]["title"],
                description=language_json["SelectMainBots"]["options"]["Milka"]["embed"]["description"],
                image_url="https://i.redd.it/what-are-your-thoughts-on-yozora-v0-62t00vvtr3nd1.jpg?width=1170&format=pjpg&auto=webp&s=43b4c815d4c9f24a03616c8146763f31c5eea752"
            )

        elif selected_option == "Kriska":
            embedFunc = create_embed(
                color=0x808080,
                title=language_json["SelectMainBots"]["options"]["Kriska"]["embed"]["title"],
                description=language_json["SelectMainBots"]["options"]["Kriska"]["embed"]["description"],
                image_url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzQ2MWljY2VseW1ibTdkeHQwdGo1YTNqMG15cGNkaGpmZ25yMjYyYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eK12uCsrAh4wmTXejp/giphy.gif"
            )

        await ctx.respond(embed=embedFunc, flags=hikari.MessageFlag.EPHEMERAL)

class SelectColor(miru.View):
    def __init__(self):
        super().__init__(timeout=None)

    @miru.text_select(
        placeholder="🌈 ┋Choose color",
        options=[
            miru.SelectOption(label="Red", emoji="❤️"),
            miru.SelectOption(label="Orange", emoji="🧡"),
            miru.SelectOption(label="Yellow", emoji="💛"),
            miru.SelectOption(label="Green", emoji="💚"),
            miru.SelectOption(label="Blue", emoji="💙"),
            miru.SelectOption(label="Aqua", emoji="💙"),
            miru.SelectOption(label="Pink", emoji="💗"),
            miru.SelectOption(label="Purple", emoji="💜"),
            miru.SelectOption(label="Grey", emoji="🖤"),
            miru.SelectOption(label="White", emoji="🤍"),
            miru.SelectOption(label="Clear", emoji="💟"),
        ], min_values=1, max_values=1, custom_id="color_select_menu")

    async def basic_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        user_language = await UserProfileFunc().get_lang(ctx.author.id)
        with open (f"localization/{user_language}.json", "r") as f:
            language_json = json.load(f)

        selected_option = select.values[0]

        member_id = ctx.author.id
        guild = ctx.get_guild()
        if guild is None:
            return
        member = guild.get_member(member_id)
        if member is None:
            return

        if selected_option == "Clear":
            await update_member_role(member, role_color_mapping, None)
            await ctx.respond(language_json["SelectColor"]["response_messages"]["remove"], flags=hikari.MessageFlag.EPHEMERAL)
        else:
            role_id = role_color_mapping.get(selected_option)
            if role_id:
                await update_member_role(member, role_color_mapping, role_id)
                await ctx.respond(language_json["SelectColor"]["response_messages"]["change"].format(selected_option), flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond(language_json["SelectColor"]["response_messages"]["invalid"], flags=hikari.MessageFlag.EPHEMERAL)
            return

    async def on_error(
        self,
        error: Exception,
        item: miru.abc.ViewItem | None = None,
        ctx: miru.ViewContext | None = None
    ) -> None:
        if ctx is not None:
            await ctx.respond(f"Oh no! This error occured: {error}", flags=hikari.MessageFlag.EPHEMERAL)


async def update_member_role(member: hikari.Member, role_ids, new_role_id: Optional[int] = None) -> None:
    """Update users color roles

    Args:
        member (disnake.Member): Member object to change
        new_role_id (disnake.Role): Role color object, which need to add
        role_ids (List): Member roles ids
    """
    member_roles = member.get_roles()
    current_role_ids = [role.id for role in member_roles if role.id in role_ids.values()]

    if current_role_ids:
        await member.remove_role(*[role for role in member_roles if role.id in current_role_ids])

    if new_role_id:
        guild = member.get_guild()
        if guild is None:
            return
        new_role = guild.get_role(new_role_id)
        if new_role is None:
            return

        await member.add_role(new_role)


class SelectLanguage(miru.View):
    @miru.text_select(
        placeholder="🌍 ┋ Polyglot?",
        options=[
            miru.SelectOption(label="English", emoji="🇺🇸󠁧󠁢󠁥󠁮󠁧󠁿"),
            miru.SelectOption(label="Russian", emoji="🇷🇺"),
            miru.SelectOption(label="Ukrainian", emoji="🇺🇦"),
        ], min_values=1, max_values=1, custom_id="language_select_menu"
    )
    async def callback(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        selected_option = select.values[0]

        embedFunc = hikari.Embed()

        if selected_option == "English":
            embedFunc = create_embed(
                color=0xFFA500,
                title="Set language to English",
                description="Ohhh, u are from England?"
            )

            await UserProfileFunc().set_lang(ctx.author.id, "en-EN")

        elif selected_option == "Russian":
            embedFunc = create_embed(
                color=0xFFFFFF,
                title="Язык установлен на Русский",
                description="Но ти курва...",
            )

            await UserProfileFunc().set_lang(ctx.author.id, "ru-RU")

        elif selected_option == "Ukrainian":
            embedFunc = create_embed(
                color=0x005BBB,
                title="Мову встановлено на Українську",
                description="Слава Україні!",
            )

            await UserProfileFunc().set_lang(ctx.author.id, "uk-UA")

        await ctx.respond(embed=embedFunc, flags=hikari.MessageFlag.EPHEMERAL)
