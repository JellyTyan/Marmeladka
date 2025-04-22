import asyncio
import random

import arc
import hikari
import miru
from miru.ext import nav

from config.config_manager import ConfigManager

plugin = arc.GatewayPlugin("Tech", invocation_contexts=[hikari.ApplicationContextType.GUILD])

config_manager = ConfigManager()

@plugin.include
@arc.slash_command("help", "A quick tour of the server.")
async def help_command(ctx: arc.GatewayContext, cs: miru.Client = arc.inject()) -> None:
    guild = ctx.get_guild()
    if guild is None:
        return

    legend_role_id = config_manager.get_config_value("LEGEND_ROLE_ID")
    members = await ctx.client.rest.fetch_members(guild.id)

    legends = [member for member in members if int(legend_role_id) in member.role_ids]

    guild_owner = await guild.fetch_owner()

    first_descr = f"""
    Ты находишься на простом и ламповом сервере Желешки! \n\nУникальные(почти) боты, функции.\n **Давайте начнём ядерную войну!**
    Владелец сервера: {guild_owner.mention}\n
    Дата создания сервера: `{guild.created_at.strftime("%d-%m-%Y")}`\n
    Всего участников: `{len(guild.get_members())}`\n
    Текущая легенда: {legends[0].mention}
    """
    embed_1 = hikari.Embed(title=guild.name, description=first_descr, color=0x2B2D31)
    embed_1.set_thumbnail(guild.icon_url)

    second_descr = """
    `/био` - информация о сладостях.\n
    `/профиль` - профиль пользователя.\n
    `/топ` - таблицы лидеров по разным направлениям.\n
    `/мило` - миленькие картиночки животных.\n
    `/эмоция` - обнимашки, целовашки и т.п.\n
    `/ядерка`, `/арсенал` - управление системой Ядерка.\n
    `/суицид` - Press F.\n
    `/рандом-число` - случайное число.\n
    """
    embed_2 = hikari.Embed(title="Мои команды:", description=second_descr, color=0x2B2D31)

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
    random_num = random.randint(first_number, second_number)
    embed = hikari.Embed(description=f"Случайное число число: {random_num}")
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
    await ctx.respond(f"Cleared {amount} messages.")

@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
