from twitchAPI.object.eventsub import ChannelRaidEvent

import models.globals

class RaidManager:
    
    # TODO need something to handle the shoutout cooldown
    async def handle_raid(info: ChannelRaidEvent):
        try:
            await models.globals._event_sub_handler_twitch.send_a_shoutout(models.globals._PRIMARY_ACCOUNT_TWITCH_ID, info.event.from_broadcaster_user_id, models.globals._PRIMARY_ACCOUNT_TWITCH_ID)
        except Exception as e:
            print(f"Error on Raid shoutout: {e}")
