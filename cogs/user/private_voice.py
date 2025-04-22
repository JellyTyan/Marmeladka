import arc
import hikari

from utils.guild import get_channels_in_category, get_guild_categories

plugin = arc.GatewayPlugin("PrivateVoice", invocation_contexts=(hikari.ApplicationContextType(0), ))


@plugin.include
@arc.slash_command(
    "setup-private-voice",
    "Setup private voice channels",
    default_permissions=hikari.Permissions.MANAGE_GUILD,
    autodefer=arc.AutodeferMode.EPHEMERAL
    )
async def setup_voice_command(ctx: arc.GatewayContext) -> None:
        guild_id = ctx.guild_id
        if not guild_id:
            return

        guild_categories = await get_guild_categories(ctx.client.app, guild_id)

        private_category_id = None
        for category in guild_categories:
            if "private" in category.name.lower():
                private_category_id = category.id
                break

        if private_category_id is None:
            private_category = await ctx.client.app.rest.create_guild_category(guild_id, "Private")
            private_category_id = private_category.id

        category_channels = await get_channels_in_category(ctx.client.app, guild_id, private_category_id)

        create_private_voice_id = None
        for channel in category_channels:
            if "create" in channel.name.lower():
                create_private_voice_id = channel.id
                break

        if create_private_voice_id is None:
            created = await ctx.client.app.rest.create_guild_voice_channel(
                guild_id,
                "Join to Create",
                category=private_category_id
            )
            create_private_voice_id = created.id

        await ctx.respond("✅ Приватная голосовая категория и канал готовы.")

@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
