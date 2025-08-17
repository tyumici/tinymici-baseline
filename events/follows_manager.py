from twitchAPI.object.eventsub import ChannelFollowEvent
import models.globals

class FollowService():
    
    async def on_follow(data: ChannelFollowEvent):
        await models.globals._chat_global.send_message(
            data.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] Welcome in {data.event.user_name}, thanks for the follow!",
        )