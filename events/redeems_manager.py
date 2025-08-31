# Package
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel


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
        print(
            colored(
                f"Point Redemption: {event.event.reward}",
                LogLevel.EVENT_SUB_NOTIF.value,
            )
        )

    async def handle_redeems_mock(event: ChannelPointsCustomRewardRedemptionAddEvent):
        """Logs event from a mock channel point redeem via the twitch-cli"""
        print(
            colored(
                "Point Redemption: MOCK REDEEM",
                LogLevel.EVENT_SUB_NOTIF.value,
            )
        )
