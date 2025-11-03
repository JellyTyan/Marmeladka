import asyncio
import json
import random

import arc
import hikari
import miru
from miru.ext import nav

from config.config_manager import ConfigManager
from functions.user_profile_func import UserProfileFunc
from utils.create_embed import create_embed

plugin = arc.GatewayPlugin("Tech", invocation_contexts=[hikari.ApplicationContextType.GUILD])

config_manager = ConfigManager()

@plugin.include
@arc.slash_command("help", "A quick tour of the server.")
async def help_command(ctx: arc.GatewayContext, cs: miru.Client = arc.inject()) -> None:
    guild = ctx.get_guild()
    if guild is None:
        return

    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)

    legend_role_id = config_manager.get_config_value("LEGEND_ROLE_ID")
    members = await ctx.client.rest.fetch_members(guild.id)
    legends = [member for member in members if int(legend_role_id) in member.role_ids]
    guild_owner = await guild.fetch_owner()

    help_data = language_json["help_command"]

    first_descr = help_data["first_description"].format(
        guild_owner=guild_owner,
        guild=guild,
        len=len,
        legends=legends
    )
    embed_1 = create_embed(
        title=help_data["title"],
        description=first_descr,
        color=0x2B2D31
    )

    embed_1.set_thumbnail(guild.make_icon_url(file_format="PNG"))

    embed_2 = create_embed(
        title=help_data["title"],
        description=help_data["second_description"],
        color=0x2B2D31
    )

    embeds = [embed_1, embed_2]
    navigator = nav.NavigatorView(pages=embeds)
    builder = await navigator.build_response_async(cs, ephemeral=True)
    await builder.create_initial_response(ctx.interaction)
    cs.start_view(navigator)


@plugin.include
@arc.slash_command("randomnumber", "A random number from and to.")
async def random_number(
    ctx: arc.GatewayContext,
    first_number: arc.Option[int, arc.IntParams("A number")],
    second_number: arc.Option[int, arc.IntParams("A number")]
    ) -> None:
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)

    random_num = random.randint(first_number, second_number)
    response = language_json["random_number_command"]["response"].format(random_num=random_num)
    embed = create_embed(description=response)
    await ctx.respond(embed=embed)


@plugin.include
@arc.slash_command(
    "clear",
    "Clears a specified number of messages.",
    default_permissions=hikari.Permissions.MANAGE_MESSAGES,
    )
async def clear_messages(
    ctx: arc.GatewayContext,
    amount: arc.Option[int, arc.IntParams("A number")]
    ) -> None:
    await ctx.defer(flags=hikari.MessageFlag.EPHEMERAL)
    channel_id = ctx.channel_id
    channel = ctx.client.cache.get_guild_channel(channel_id)
    if channel is None:
        return

    if isinstance(channel, hikari.TextableChannel):
        async for message in channel.fetch_history().limit(amount):
            try:
                await ctx.client.rest.delete_message(channel, message)
                await asyncio.sleep(0.3)
            except Exception:
                continue
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)

    response = language_json["clear_command"]["response"].format(amount=amount)
    await ctx.respond(response)

@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
