import os

# Package
from twitchAPI.twitch import Twitch
from twitchAPI.chat import Chat
from mysql.connector.pooling import PooledMySQLConnection

# TODO there has to be a better way to expose and init these globals right
# Twitch API Globals
_chat_global: Chat = None
_bot_handler_twitch: Twitch = None
_event_sub_handler_twitch: Twitch = None

# Database Connection Globals
_connectionPrimary: PooledMySQLConnection = None
_connectionSecrets: None = None

# .env Globals
_BOT_TWITCH_ID: str = None
_BROADCASTER_TWITCH_ID: str = None
_TARGET_CHANNELS: list = None
_BOT_SIGIL: str = None
_BOT_NAME: str = None
_BROADCASTER_NAME: str = None


def init_globals():
    """Initialize all global variables and set their value to None, load .env and assign to target globals"""

    global _chat_global
    _chat_global = None

    global _bot_handler_twitch
    _bot_handler_twitch = None

    global _event_sub_handler_twitch
    _event_sub_handler_twitch = None

    global _connectionPrimary
    _connectionPrimary = None

    global _connectionSecrets
    _connectionSecrets = None

    # --- --- --- --- --- .env loading --- --- --- --- --- #

    global _BOT_TWITCH_ID
    _BOT_TWITCH_ID = os.getenv("TINYMICI_BOT_TWITCH_ID")

    global _BROADCASTER_TWITCH_ID
    _BROADCASTER_TWITCH_ID = os.getenv("TINYMICI_BROADCASTER_TWITCH_ID")

    global _TARGET_CHANNELS
    _TARGET_CHANNELS = os.getenv("TINYMICI_TARGET_CHANNELS").split(
        ","
    )  # split to a list

    global _BOT_SIGIL
    _BOT_SIGIL = os.getenv("TINYMICI_BOT_SIGIL").encode().decode("unicode_escape")

    global _BOT_NAME
    _BOT_NAME = os.getenv("TINYMICI_BOT_NAME")

    global _BROADCASTER_NAME
    _BROADCASTER_NAME = os.getenv("TINYMICI_BROADCASTER_NAME")
