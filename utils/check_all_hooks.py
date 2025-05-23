import json

import arc
import hikari
import miru

from ui.ticketsUI import TicketsView
from ui.welcomeUI import MainView
from utils.create_embed import create_embed


async def check_info_view(arc_client: arc.GatewayClient, cx: miru.Client):
    with open('config/hooks.json', 'r') as file:
        data = json.load(file)

    info_channel_json = data.get("info_channel", {})

    info_message_id = info_channel_json["message_id"]

    view = MainView()
    try:
        info_message = await arc_client.rest.fetch_message(info_channel_json.get("channel_id"), info_message_id)

        cx.start_view(view, bind_to=info_message)

    except hikari.NotFoundError:
        title = info_channel_json["title"]
        description = info_channel_json["description"]
        footer = info_channel_json["footer"]
        footer_image = info_channel_json["footer_image"]
        image_url = info_channel_json["image_url"]
        image_cat_url = info_channel_json["image_cat_url"]
        embedImg = create_embed(
            image_url=image_url
        )
        embedMain = create_embed(
            title=title,
            description=description,
            footer_text=footer,
            footer_icon=footer_image,
            image_url=image_cat_url
        )

        info_channel_id = info_channel_json["channel_id"]

        message = await arc_client.rest.create_message(info_channel_id, embeds=[embedImg, embedMain], components=view)

        info_channel_json["message_id"] = message.id

        with open('config/hooks.json', 'w') as f:
            json.dump(data, f, indent=4)

        cx.start_view(view, bind_to=message)


async def check_ticket_view(arc_client: arc.GatewayClient, cx: miru.Client):
    with open('config/hooks.json', 'r') as file:
        data = json.load(file)

    ticket_channel_json = data.get("ticket_channel", {})

    ticket_message_id = ticket_channel_json["message_id"]

    view = TicketsView()
    try:
        info_message = await arc_client.rest.fetch_message(ticket_channel_json.get("channel_id"), ticket_message_id)

        cx.start_view(view, bind_to=info_message)

    except hikari.NotFoundError:
        title = ticket_channel_json["title"]
        description = ticket_channel_json["description"]
        footer = ticket_channel_json["footer"]
        footer_image = ticket_channel_json["footer_image"]
        image_url = ticket_channel_json["image_url"]
        image_cat_url = ticket_channel_json["image_cat_url"]
        embedImg = create_embed(
            image_url=image_url
        )
        embedMain = create_embed(
            title=title,
            description=description,
            footer_text=footer,
            footer_icon=footer_image,
            image_url=image_cat_url
        )

        info_channel_id = ticket_channel_json["channel_id"]

        message = await arc_client.rest.create_message(info_channel_id, embeds=[embedImg, embedMain], components=view)

        ticket_channel_json["message_id"] = message.id

        with open('config/hooks.json', 'w') as f:
            json.dump(data, f, indent=4)

        cx.start_view(view, bind_to=message)
