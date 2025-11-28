import asyncio
import os

# Package
from twitchAPI.object.eventsub import ChannelAdBreakBeginEvent
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel


class AdManager:
    """
    Handles ad break event for the current Broadcaster

    Add additional sleep segments based on how long your ad breaks are

    Default is three one minute sleeps for a standard three minute ad break per hour
    """

    async def on_ad_start(info: ChannelAdBreakBeginEvent):
        """
        Sends messages in the chat room for ad break start, and end

        Default will post links to the broadcasters Discord and Bluesky
        """
        print(colored("An ad break has started", LogLevel.EVENT_SUB_NOTIF.value))
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] Ads are in progress...",
        )
        await asyncio.sleep(60)
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] {os.getenv("TINYMICI_DISCORD")}",
        )
        await asyncio.sleep(60)
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] {os.getenv("TINYMICI_BLUESKY")}",
        )
        await asyncio.sleep(60)
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] Ads are over!",
        )
        print(colored("An ad break has ended", LogLevel.EVENT_SUB_NOTIF.value))
