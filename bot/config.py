from os import path, getenv

import dotenv

PROJECT_DIR = path.abspath(path.dirname(__file__))
ROOT_DIR = path.abspath(path.dirname(__file__) + "/..")
ENV_PATH = path.join(ROOT_DIR, ".env")

defaults = {
    "HTTP_PROVIDER_URL": "http://127.0.0.1:8545",
    "USER_ADDRESS": "0x11BdE3126f46Cfb3851a9102c60b510B1305aF5b",
    "SHROOM_MARKET_CONTRACT_ADDRESS": "0x577C66469b5df2781B3a77a9dC825eC2de76c4a4",
    "INVENTORY_PATH": ROOT_DIR + "/inventory",
    "EVENT_LISTENER_POLL_INTERVAL": 15,
    "PROJECT_DIR": PROJECT_DIR,
    "ROOT_DIR": ROOT_DIR,
    "ENV_PATH": ENV_PATH
}


class Settings:

    def __init__(self):
        dotenv.load_dotenv(ENV_PATH)

    def __getattribute__(self, name):
        default = defaults.get(name)
        if getenv(name, default) != dotenv.get_key(ENV_PATH, name):
            dotenv.load_dotenv(ENV_PATH, override=True)
        return getenv(name, default)

    def __setattr__(self, item, value):
        dotenv.set_key(ENV_PATH, item, value)
        dotenv.load_dotenv(ENV_PATH, override=True)


settings = Settings()
