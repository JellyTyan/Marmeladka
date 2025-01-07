import hikari
import miru

from config.config_manager import ConfigManager

from utils.create_embed import create_embed

config_manager = ConfigManager()

class TicketsView(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(timeout=None, *args, **kwargs)

        self.add_item(QuetionButton())
        self.add_item(PropositionButton())
        self.add_item(ReportButton())


class QuetionButton(miru.Button):
    def __init__(self):
        super().__init__(
            label="Задать вопрос",
            style=hikari.ButtonStyle.PRIMARY,
            custom_id="question_button",
        )

    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(modal=QuetionModal())

class QuetionModal(miru.Modal, title="Задай вопрос"):
    question = miru.TextInput(
        label="Вопросик",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="В кратце опиши свой вопрос. Ты ограничен!",
        custom_id="input",
        required=True,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()
        guild = ctx.get_guild()
        if guild is None:
            return

        ticket_channel_id = config_manager.get_config_value("TICKET_CHANNEL_ID")
        ticket_channel = await ctx.client.rest.fetch_channel(int(ticket_channel_id))

        staff_role_id = config_manager.get_config_value("STAFF_ROLE_ID")
        staff_role = guild.get_role(int(staff_role_id))

        if staff_role is None:
            return

        if isinstance(ticket_channel, hikari.TextableGuildChannel):
            active_threads = await ctx.client.rest.fetch_active_threads(guild.id)
            ticket_count = 0
            for thread in active_threads:
                if thread.parent_id == int(ticket_channel_id):
                    ticket_count += 1

            thread: hikari.GuildThreadChannel = await ctx.client.rest.create_thread(
                ticket_channel.id,
                hikari.ChannelType.GUILD_PRIVATE_THREAD,
                f"Тикет {ticket_count}",
                invitable=False,
                auto_archive_duration=1440,
            )

            embedWelcome = create_embed(
                title="Вопрос от пользователя",
                description=f'Всех приветствую! Мы все тут собрались для обсуждения животрепещущего вопроса от {ctx.author.display_name}:\n\n```{self.question.value}```',
                color=0xA020F0,
            )

            view = miru.View()
            view.add_item(CloseThreadButton())

            await thread.send(content=staff_role.mention, embed=embedWelcome, components=view, role_mentions=True)

            await ctx.respond(f"Ваш вопрос отправлен в тикет {thread.mention}", flags=hikari.MessageFlag.EPHEMERAL)

            ctx.client.start_view(view)

            await ctx.client.rest.add_thread_member(thread, ctx.author)

class CloseThreadButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(
            style=hikari.ButtonStyle.DANGER,
            label="Закрыть ветку",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        view = miru.View()
        view.add_item(AcceptButton())

        await ctx.respond("Вы уверены, что вопросов больше не осталось?", components=view)

        ctx.client.start_view(view)

class AcceptButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.SUCCESS, label="Согласен")
        self.value = True

    async def callback(self, ctx: miru.ViewContext) -> None:
        thread = await ctx.client.rest.fetch_channel(ctx.channel_id)

        if not isinstance(thread, hikari.GuildThreadChannel):
            print("not thread")
            return

        await ctx.respond("Спасибо вам!")

        await ctx.client.rest.remove_thread_member(thread, ctx.author)


class PropositionButton(miru.Button):
    def __init__(self):
        super().__init__(
            label="Предложить",
            style=hikari.ButtonStyle.SUCCESS,
            custom_id="proposition_button",
        )
        self.value = True

    async def callback(self, ctx: miru.ViewContext):
        await ctx.respond_with_modal(modal=PropositionModal())

class PropositionModal(miru.Modal, title="Задай вопрос"):
    proposition = miru.TextInput(
        label="Предложение",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Начирикай что-нить",
        custom_id="input",
        required=True,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        proposition_channel_id = config_manager.get_config_value("PROPOSITION_CHANNEL_ID")
        proposition_channel= await ctx.client.rest.fetch_channel(int(proposition_channel_id))

        if isinstance(proposition_channel, hikari.TextableGuildChannel):
            proposition_embed = create_embed(
                title="Предложение от пользователя",
                description=f'**{ctx.author.mention}**: ```{self.proposition}```',
                color=0xA020F0,
            )

            await proposition_channel.send(embed=proposition_embed)

        await ctx.respond("Спасибо за ваше предложение!!")


class ReportButton(miru.Button):
    def __init__(self):
        super().__init__(
            label="Пожаловаться",
            style=hikari.ButtonStyle.DANGER,
            custom_id="report_button",
        )

    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(modal=ReportModal())

class ReportModal(miru.Modal, title="Пожалуйся"):
    report = miru.TextInput(
        label="Жалоба",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="В кратце опиши свой вопрос. Ты ограничен!",
        custom_id="report_input",
        required=False,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        report_channel_id = config_manager.get_config_value("REPORT_CHANNEL_ID")
        report_channel = await ctx.client.rest.fetch_channel(int(report_channel_id))

        if isinstance(report_channel, hikari.TextableGuildChannel):
            report_embed = create_embed(
                title="Жалоба",
                description=f'**{ctx.author.mention}**: ```{self.report}```',
                color=0xA020F0,
            )

            await report_channel.send(embed=report_embed)
