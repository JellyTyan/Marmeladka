import asyncio
import random

import hikari
import lightbulb
import miru
from miru.ext import nav

from config.config_manager import ConfigManager

loader = lightbulb.Loader()

config_manager = ConfigManager()

@loader.command
class HelpCommand(
    lightbulb.SlashCommand,
    name="commands.help.name",
    description="commands.help.description",
    contexts=(hikari.ApplicationContextType(0),),
    localize=True
):
    @lightbulb.invoke
    async def help_command(self, ctx: lightbulb.Context, cs: miru.Client) -> None:
        guild_id = ctx.guild_id
        if guild_id is None:
            return

        guild = await ctx.client.rest.fetch_guild(guild_id)
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


@loader.command
class RandomNumberCommand(
    lightbulb.SlashCommand,
    name="commands.randomnumber.name",
    description="commands.randomnumber.description",
    contexts=(hikari.ApplicationContextType(0),),
    localize=True
):
    first_number = lightbulb.integer("commands.randomnumber.options.first_number.name", "commands.randomnumber.options.first_number.description", localize=True)
    second_number = lightbulb.integer("commands.randomnumber.options.second_number.name", "commands.randomnumber.options.second_number.description", localize=True)

    @lightbulb.invoke
    async def random_number(self, ctx: lightbulb.Context) -> None:
        random_num = random.randint(self.first_number, self.second_number)
        embed = hikari.Embed(description=f"Случайное число число: {random_num}")
        await ctx.respond(embed=embed)


@loader.command
class ClearCommand(
    lightbulb.SlashCommand,
    name="commands.clear.name",
    description="commands.clear.description",
    contexts=(hikari.ApplicationContextType(0),),
    default_member_permissions=hikari.Permissions.MANAGE_MESSAGES,
    localize=True
):
    amount = lightbulb.integer("commands.clear.options.amount.name", "commands.clear.options.amount.description", localize=True)

    @lightbulb.invoke
    async def clear_messages(self, ctx: lightbulb.Context) -> None:
        await ctx.defer(ephemeral=True)
        channel = ctx.channel_id
        channel = await ctx.client.rest.fetch_channel(channel)
        if channel is None:
            return

        if isinstance(channel, hikari.TextableChannel):
            async for message in channel.fetch_history().limit(self.amount):
                try:
                    await ctx.client.rest.delete_message(channel, message)
                    await asyncio.sleep(0.3)
                except Exception:
                    continue
        await ctx.respond(f"Cleared {self.amount} messages.")
