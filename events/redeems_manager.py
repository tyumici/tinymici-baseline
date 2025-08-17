from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent
import models.globals


class RedeemService:

    async def handle_redeems(event: ChannelPointsCustomRewardRedemptionAddEvent):
        if event.event.reward.title == "test":
            await models.globals._chat_global.send_message(
                event.event.broadcaster_user_name,
                f"[{models.globals._BOT_SIGIL}] test confirmed",
            )
        print(f"Point Redemption: {event.event.reward}")
