import hikari
import lightbulb

from utils.guild import get_guild_categories, get_channels_in_category

loader = lightbulb.Loader()

@loader.command
class SetupPrivateVoiceCommnad(
    lightbulb.SlashCommand,
    name="setup-private-voice",
    description="Setup private voice channelks",
    contexts=(hikari.ApplicationContextType(0),),
    default_member_permissions=hikari.Permissions.MANAGE_GUILD,
):
    @lightbulb.invoke
    async def setup_command(self, ctx: lightbulb.Context) -> None:
        await ctx.defer(ephemeral=True)

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
