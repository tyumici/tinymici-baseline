# Package
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent

# Custom
import models.globals


class RedeemService:
    """Service for handling channel point redeems"""

    # TODO update this to use a match case
    async def handle_redeems(event: ChannelPointsCustomRewardRedemptionAddEvent):
        """Handles channel point redemptions by reward title name"""
        if event.event.reward.title == "test":
            await models.globals._chat_global.send_message(
                event.event.broadcaster_user_name,
                f"[{models.globals._BOT_SIGIL}] test confirmed",
            )
        print(f"Point Redemption: {event.event.reward}")
