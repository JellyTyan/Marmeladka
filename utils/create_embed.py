from typing import Optional, Union

import hikari


def create_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    color: Union[int, hikari.Color] = 0x313338,
    image_url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
    footer_text: Optional[str] = None,
    footer_icon: Optional[str] = None,
    author_name: Optional[str] = None,
    author_icon: Optional[str] = None,
    url: Optional[str] = None,
) -> hikari.Embed:
    """
    Create a customized embed.

    Args:
        title (str, optional): Embed title. Defaults to None.
        description (str, optional): Embed description. Defaults to None.
        color (int or hikari.Color, optional): Embed color. Defaults to 0xFF0000.
        image_url (str, optional): URL for the embed image. Defaults to None.
        thumbnail_url (str, optional): URL for the embed thumbnail. Defaults to None.
        footer_text (str, optional): Text for the embed footer. Defaults to None.
        footer_icon (str, optional): URL for the footer icon. Defaults to None.
        author_name (str, optional): Name for the embed author. Defaults to None.
        author_icon (str, optional): URL for the author icon. Defaults to None.
        url (str, optional): URL for the embed title. Defaults to None.

    Returns:
        hikari.Embed: The created embed.
    """
    embed = hikari.Embed(
        title=title,
        description=description,
        color=color,
        url=url,
    )

    if image_url:
        embed.set_image(image_url)

    if thumbnail_url:
        embed.set_thumbnail(thumbnail_url)

    if footer_text or footer_icon:
        embed.set_footer(text=footer_text or "", icon=footer_icon)

    if author_name:
        embed.set_author(name=author_name, icon=author_icon)

    return embed
