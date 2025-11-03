import arc
import hikari
import json

from functions.user_profile_func import UserProfileFunc
from utils.create_embed import create_embed

plugin = arc.GatewayPlugin("Informaton", invocation_contexts=[hikari.ApplicationContextType.GUILD])

bio = plugin.include_slash_group("biography", "Learn the story of one of the heroines!", autodefer=arc.AutodeferMode.ON)


@bio.include
@arc.slash_subcommand("marmeladkabio", "Find out more about Marmeladka!")
async def marmeladka_bio(ctx: arc.GatewayContext) -> None:
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)
    
    bio_data = language_json["biography_commands"]["marmeladka"]
    embed = create_embed(
        title=bio_data["title"],
        description=bio_data["description"],
        image_url=bio_data["image_url"],
        color=0xFF6F61
    )
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bio.include
@arc.slash_subcommand("zefirkabio", "Find out more about Zefirka!")
async def zefirka_bio(ctx: arc.GatewayContext) -> None:
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)
    
    bio_data = language_json["biography_commands"]["zefirka"]
    embed = create_embed(
        title=bio_data["title"],
        description=bio_data["description"],
        image_url=bio_data["image_url"],
        color=0xFFC0CB
    )
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bio.include
@arc.slash_subcommand("shocomelkabio", "Find out more about Shocomelka!")
async def shocomelka_bio(ctx: arc.GatewayContext) -> None:
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)
    
    bio_data = language_json["biography_commands"]["shocomelka"]
    embed = create_embed(
        title=bio_data["title"],
        description=bio_data["description"],
        image_url=bio_data["image_url"],
        color=0x8B4513
    )
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bio.include
@arc.slash_subcommand("milkabio", "Find out more about Milka!")
async def milka_bio(ctx: arc.GatewayContext) -> None:
    user_language = await UserProfileFunc().get_lang(ctx.user.id)
    with open(f"localization/{user_language}.json", "r") as f:
        language_json = json.load(f)
    
    bio_data = language_json["biography_commands"]["milka"]
    embed = create_embed(
        title=bio_data["title"],
        description=bio_data["description"],
        image_url=bio_data["image_url"],
        color=0xFFFFFF
    )
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
