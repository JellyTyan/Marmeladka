import asyncio
import random

import hikari
import lightbulb
import miru
from miru.ext import nav

# from welcome_buttons import InfoString, DDMColor
from config.config_manager import ConfigManager

plugin = lightbulb.Plugin("Tech")

config_manager = ConfigManager()

@plugin.command
@lightbulb.command("помощь", "Быстрый экскурс по серверу.", ephemeral=True, app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def help_command(ctx: lightbulb.SlashContext) -> None:
    guild = ctx.get_guild()
    if guild is None:
        return

    legend_role_id = config_manager.get_config_value("LEGEND_ROLE_ID")
    members = await ctx.bot.rest.fetch_members(guild.id)

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

    miru_client: miru.Client = ctx.bot.d.miru

    builder = await navigator.build_response_async(miru_client)
    await builder.create_initial_response(ctx.interaction)

    miru_client.start_view(navigator)


@plugin.command
@lightbulb.option("first_number", "Точка старта.", int, required=True, min_value=0)
@lightbulb.option("second_number", "Точка невозврата.", int, required=True, min_value=0)
@lightbulb.command("рандом-число", "Случайное число от и до.", ephemeral=False, app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def random_number(ctx: lightbulb.Context) -> None:
    first_number = ctx.options["первое-число"]
    second_number = ctx.options["второе-число"]
    random_num = random.randint(first_number, second_number)
    embed = hikari.Embed(description=f"Случайное число число: {random_num}")
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option("amount", "Количество сообщений для удаления.", int, required=True)
@lightbulb.command("clear", "Clears a specified number of messages.", ephemeral=True, auto_defer=True, app_command_default_member_permissions=hikari.Permissions.MANAGE_MESSAGES, app_command_dm_enabled=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def clear_messages(ctx: lightbulb.Context) -> None:
    channel = ctx.get_channel()
    amount = ctx.options.amount
    if channel is None:
        return

    if isinstance(channel, hikari.TextableChannel):
        async for message in channel.fetch_history().limit(amount):
            try:
                await ctx.app.rest.delete_message(channel, message)
                await asyncio.sleep(1)
            except Exception:
                continue
    await ctx.respond(f"Cleared {amount} messages.")


# @commands.slash_command(name="ruleshoock", default_member_permissions=0, dm_permission=False)
# async def ruleshook(self, inter: disnake.ApplicationCommandInteraction):
#     channel = inter.channel

#     embedImg = disnake.Embed(color=0x313338)
#     embedImg.set_image(url="https://cdn.discordapp.com/attachments/1109526498299359303/1152549191181156455/ce54fbfa9dee627fa1c5f50233a96b15.gif")

#     embedServerWelcome = disnake.Embed(
#         color=0x313338,
#         title="Привіт Юначе!",
#         description="Добро пожаловать на **Jelly's Server**! \n\n Спасибо за присоединение к серверу \n\n Хорошего тебе дня и **вкусных пельмешек**!",
#     )
#     embedServerWelcome.set_image(url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png")
#     embedServerWelcome.set_footer(
#         text="Пельмешки лучше с майонезом!",
#         icon_url="https://cdn.discordapp.com/attachments/1109526498299359303/1152553749118726164/ac35fa88716385208d2d0e8677a6941f85757b43r1-993-924v2_uhq_waifu2x_2x_3n_png.png",
#     )

#     await channel.send(embeds=[embedImg, embedServerWelcome])

# @commands.slash_command(name="infohook", default_member_permissions=0, dm_permission=False)
# async def infohook(self, inter: disnake.ApplicationCommandInteraction):
#     channel = inter.channel

#     embedImg = disnake.Embed(color=0x313338)
#     embedImg.set_image(url="https://media.discordapp.net/attachments/1109526498299359303/1152555558021374052/4e4f109955b63431d0ae5fde1b166d75.gif")

#     embedServerInfo = disnake.Embed(
#         color=0x313338,
#         title="__Информация__",
#         description="Все, возможно, интересующие тебя темы собрались тут \n\n **Чего-то не нашёл?**\n Обратись в раздел тикетов",
#     )
#     embedServerInfo.set_image(url="https://cdn.discordapp.com/attachments/883379603719200838/1030767319867215903/image.png")
#     embedServerInfo.set_footer(
#         text="Когда-то и здесь будет солнце",
#         icon_url="https://cdn.discordapp.com/attachments/1109526498299359303/1152557641806127114/82c3e4f06e12cbfd0004479c5a23796c.png",
#     )

#     view2 = InfoString()

#     await channel.send(embeds=[embedImg, embedServerInfo], view=view2)



def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
