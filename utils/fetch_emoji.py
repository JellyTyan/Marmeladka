def find_emoji_by_name(emojis, name):
    for emoji_id, emoji in emojis.items():
        if emoji.name == name:
            return emoji.id
    return None
