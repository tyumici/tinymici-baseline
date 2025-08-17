# Package
from twitchAPI.object.eventsub import ChannelRaidEvent

# Custom
import models.globals


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
        except Exception as e:
            print(f"Error on Raid shoutout: {e}")
