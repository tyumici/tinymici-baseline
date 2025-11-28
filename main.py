import asyncio

# Package
from dotenv import load_dotenv
from termcolor import colored
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import ChatEvent
import schedule
import threading

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
from models.log_level import LogLevel
from utilities.database_connect import DatabaseConnector


# Global variable and database connection instantiation
load_dotenv()
models.globals.init_globals()
connPrimary = DatabaseConnector.connect_primary()
connSecrets = DatabaseConnector.connect_secrets()
schedule.every(4).hours.do(
    DatabaseConnector.reconnect_db_job
)  # run database reconnect every 4 hours
threading.Thread(target=DatabaseConnector.run_scheduler, daemon=True).start()

secrets = DataService.get_all_secrets()


async def run():
    # Initialize bot handler Twitch Class
    bot_handler_twitch = await AuthService.setup_bot_auth(secrets)

    # Initialize event sub handler Twitch Class
    event_sub_handler_twitch = await AuthService.setup_event_sub_auth(secrets)

    # Initialize Chat Class, register on any message handler from CrossChannelService
    chat_global = await setupChatGlobal(bot_handler_twitch)
    chat_global.register_event(ChatEvent.MESSAGE, CrossChannelService.on_any_message)
    chat_global.start()

    # Initialize the Event Sub WebSocket
    eventsub = EventSubWebsocket(event_sub_handler_twitch)
    eventsub.start()

    # Listen for channel point redemptions on the event sub
    await eventsub.listen_channel_points_custom_reward_redemption_add(
        models.globals._BROADCASTER_TWITCH_ID, RedeemService.handle_redeems
    )
    # Listen for channel follows on the event sub
    await eventsub.listen_channel_follow_v2(
        models.globals._BROADCASTER_TWITCH_ID,
        models.globals._BROADCASTER_TWITCH_ID,
        FollowService.on_follow,
    )
    # Listen for ad break start on the event sub
    await eventsub.listen_channel_ad_break_begin(
        models.globals._BROADCASTER_TWITCH_ID, AdManager.on_ad_start
    )
    # Listen for channel stream offline on the event sub
    await eventsub.listen_stream_offline(
        models.globals._BROADCASTER_TWITCH_ID, OfflineManager.change_stream_info
    )
    # Listen for raid into channel on the event sub
    await eventsub.listen_channel_raid(
        RaidManager.handle_raid, models.globals._BROADCASTER_TWITCH_ID
    )

    try:
        # Press enter in the terminal to shutdown
        input("press Enter to shut down...\n")
    except KeyboardInterrupt:
        pass
    finally:
        # Stop all listeners before terminating
        print(colored("Shutting down", LogLevel.CONNECTION_MESSAGE.value))
        chat_global.stop()
        await eventsub.stop()
        await event_sub_handler_twitch.close()


# Start the Twitch Bot
asyncio.run(run())
