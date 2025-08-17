# Package
from twitchAPI.object.eventsub import ChannelFollowEvent
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel


class FollowService:
    """Service to provide actions on a user following the channel"""

    async def on_follow(data: ChannelFollowEvent):
        """Send a message in the broadcasters chat room welcoming in the new follower"""
        await models.globals._chat_global.send_message(
            data.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] Welcome in {data.event.user_name}, thanks for the follow!",
        )
        print(
            colored(
                f"{data.event.user_name} has followed", LogLevel.EVENT_SUB_NOTIF.value
            )
        )
