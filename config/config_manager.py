import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self, mode='dev'):
        self.config = {}
        self.mode = mode
        self.load_config()

    def load_config(self):
        if self.mode == 'prod':
            env_path = os.path.join('config/production', '.env')
        else:
            env_path = os.path.join('config/development', '.env')

        if not os.path.exists(env_path):
            raise FileNotFoundError(f"The environment file '{env_path}' does not exist.")

        load_dotenv(env_path)
        self.config = {key: os.getenv(key) for key in os.environ if os.getenv(key) is not None}

    def get_config_value(self, key, value_type=str):
        value = self.config.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found in config.")

        try:
            return value_type(value)
        except ValueError:
            raise ValueError(f"Value for key '{key}' cannot be converted to {value_type.__name__}")
