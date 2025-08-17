import os

# Package
from twitchAPI.object.eventsub import StreamOfflineEvent

# Custom
import models.globals


class OfflineManager:
    """Performs automated actions for when the live stream goes offline"""
    async def change_stream_info(info: StreamOfflineEvent):
        """Updates the stream title to the given offline title when the stream ends"""
        print("Stream Ended")
        await models.globals._event_sub_handler_twitch.modify_channel_information(
            models.globals._BROADCASTER_TWITCH_ID,
            None,
            None,
            {os.getenv("OFFLINE_TITLE")},
        )
