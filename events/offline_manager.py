import os

# Package
from twitchAPI.object.eventsub import StreamOfflineEvent
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel


class OfflineManager:
    """Performs automated actions for when the live stream goes offline"""

    async def change_stream_info(info: StreamOfflineEvent):
        """Updates the stream title to the given offline title when the stream ends"""
        print(colored("Stream Ended", LogLevel.EVENT_SUB_NOTIF.value))
        await models.globals._event_sub_handler_twitch.modify_channel_information(
            models.globals._BROADCASTER_TWITCH_ID,
            None,
            None,
            {os.getenv("OFFLINE_TITLE")},
        )

    async def change_stream_info_mock(info: StreamOfflineEvent):
        """Logs event from a mock stream offline event via the twitch-cli"""
        print(colored("Stream Ended", LogLevel.EVENT_SUB_NOTIF.value))
