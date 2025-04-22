import random

import yaml


def get_random_gif(type: str):
    with open("src/yaml/gifs.yaml", "r") as file:
        gifs = yaml.safe_load(file)
        gif_list = gifs["gif_types"][type]
        return random.choice(gif_list)
