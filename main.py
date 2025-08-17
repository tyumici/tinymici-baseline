# Native
import asyncio

# Package
from twitchAPI.type import ChatEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from dotenv import load_dotenv

# Custom

from authentication.auth_service import AuthService
from commands.command_registration import setupChatGlobal
from commands.cross_channel_mixer import CrossChannelService
from data.data_service import DataService
from events.ad_manager import AdManager
from events.follows_manager import FollowService
from events.offline_manager import OfflineManager
from events.raid_manager import RaidManager
from events.redeems_manager import RedeemService
import models.globals

# Global variable and database connection instantiation
load_dotenv()
models.globals.init_globals()
connPrimary = DataService.connect_primary()
connSecrets = DataService.connect_secrets()
secrets = DataService.get_all_secrets()


async def run():
    # Initialize bot handler Twitch Class
    bot_handler_twitch = await AuthService.setup_bot_auth(secrets)

    # Initialize event sub handler Twitch Class
    event_sub_handler_twitch = await AuthService.setup_event_sub_auth(secrets)

    # INIT CHAT
    chat_global = await setupChatGlobal(bot_handler_twitch)
    chat_global.register_event(ChatEvent.MESSAGE, CrossChannelService.on_any_message)
    chat_global.start()

    # INIT EVENTSUB
    eventsub = EventSubWebsocket(event_sub_handler_twitch)
    eventsub.start()

    # REDEMPTION SUB
    await eventsub.listen_channel_points_custom_reward_redemption_add(
        models.globals._PRIMARY_ACCOUNT_TWITCH_ID, RedeemService.handle_redeems
    )
    # FOLLOW SUB
    await eventsub.listen_channel_follow_v2(
        models.globals._PRIMARY_ACCOUNT_TWITCH_ID,
        models.globals._PRIMARY_ACCOUNT_TWITCH_ID,
        FollowService.on_follow,
    )
    # AD BREAK SUB
    await eventsub.listen_channel_ad_break_begin(
        models.globals._PRIMARY_ACCOUNT_TWITCH_ID, AdManager.on_ad_start
    )
    # OFFLINE SUB
    await eventsub.listen_stream_offline(
        models.globals._PRIMARY_ACCOUNT_TWITCH_ID, OfflineManager.change_stream_info
    )
    # RAID SUB
    await eventsub.listen_channel_raid(
        RaidManager.handle_raid, models.globals._PRIMARY_ACCOUNT_TWITCH_ID
    )

    try:
        input("press Enter to shut down...\n")
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down")
        chat_global.stop()
        await eventsub.stop()
        await event_sub_handler_twitch.close()


# RUN MAIN
asyncio.run(run())
