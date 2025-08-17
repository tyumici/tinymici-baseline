import os

from twitchAPI.object.eventsub import StreamOfflineEvent
import models.globals


class OfflineManager:

    async def change_stream_info(info: StreamOfflineEvent):
        print("Stream Ended")
        await models.globals._event_sub_handler_twitch.modify_channel_information(
            models.globals._PRIMARY_ACCOUNT_TWITCH_ID,
            None,
            None,
            {os.getenv("OFFLINE_TITLE")},
        )
