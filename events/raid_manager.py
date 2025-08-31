# Package
from twitchAPI.object.eventsub import ChannelRaidEvent
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel


class RaidManager:
    """Performs automated actions when a user raids the broadcaster"""

    # TODO need something to handle the shoutout cooldown
    async def handle_raid(info: ChannelRaidEvent):
        """Performs an automated shout out to the use that is raiding into the broadcaster"""
        try:
            await models.globals._event_sub_handler_twitch.send_a_shoutout(
                models.globals._BROADCASTER_TWITCH_ID,
                info.event.from_broadcaster_user_id,
                models.globals._BROADCASTER_TWITCH_ID,
            )
            print(
                colored(
                    f"Raid received by: {info.event.from_broadcaster_user_name}",
                    LogLevel.EVENT_SUB_NOTIF.value,
                )
            )
        except Exception as e:
            print(colored(f"Error on Raid shoutout: {e}", LogLevel.ERROR_MESSAGE.value))

    async def handle_raid_mock(info: ChannelRaidEvent):
        """Logs event from a mock raid via the twitch-cli"""
        print(
            colored(
                f"Raid received by: {info.event.from_broadcaster_user_name}",
                LogLevel.EVENT_SUB_NOTIF.value,
            )
        )
