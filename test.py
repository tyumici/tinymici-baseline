import asyncio
import os
from termcolor import colored
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from dotenv import load_dotenv
from twitchAPI.object.eventsub import ChannelSubscribeEvent
from twitchAPI.oauth import UserAuthenticator
from events.follows_manager import FollowService
from events.offline_manager import OfflineManager
from events.raid_manager import RaidManager
from events.redeems_manager import RedeemService
from models.log_level import LogLevel
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope

# Global variable
load_dotenv()
MOCK_CLIENT_ID = os.getenv("TINYMICI_MOCK_CLIENT_ID")
MOCK_CLIENT_SECRET = os.getenv("TINYMICI_MOCK_CLIENT_SECRET")
MOCK_USER_ID = os.getenv("TINYMICI_MOCK_USER_ID")


async def on_subscribe(data: ChannelSubscribeEvent):
    print(f"{data.event.user_name} just subscribed!")


async def run():
    # Create instance of Twitch Class for mock api calls
    twitch = await Twitch(
        MOCK_CLIENT_ID,
        MOCK_CLIENT_SECRET,
        base_url="http://localhost:8000/mock/",
        auth_base_url="http://localhost:8000/auth/",
    )
    twitch.auto_refresh_auth = False

    # Create fake user auth
    auth = UserAuthenticator(
        twitch,
        [AuthScope.CHANNEL_READ_SUBSCRIPTIONS],
        auth_base_url="http://localhost:8000/auth/",
    )
    token = await auth.mock_authenticate(MOCK_USER_ID)
    await twitch.set_user_authentication(token, [AuthScope.CHANNEL_READ_SUBSCRIPTIONS])

    # Get our test user
    user = await first(twitch.get_users())
    print(user.id)

    # Create instance of Event Sub Websocket for watching mock eventsub events
    eventsub = EventSubWebsocket(
        twitch,
        connection_url="ws://127.0.0.1:8080/ws",
        subscription_url="http://127.0.0.1:8080/",
    )
    eventsub.start()

    # --- --- --- --- --- Event Sub Listeners --- --- --- --- --- #

    channel_point_reward_id = (
        await eventsub.listen_channel_points_custom_reward_redemption_add(
            user.id, RedeemService.handle_redeems_mock
        )
    )
    print(
        f"twitch-cli event trigger add-reward -t {user.id} -u {channel_point_reward_id} -T websocket"
    )

    follow_id = await eventsub.listen_channel_follow_v2(
        user.id, user.id, FollowService.on_follow_mock
    )
    print(f"twitch-cli event trigger follow -t {user.id} -u {follow_id} -T websocket")

    # TODO hook to a mock and a real class
    sub_id = await eventsub.listen_channel_subscribe(user.id, on_subscribe)
    print(f"twitch-cli event trigger subscribe -t {user.id} -u {sub_id} -T websocket")

    stream_down_id = await eventsub.listen_stream_offline(
        user.id, OfflineManager.change_stream_info_mock
    )
    print(
        f"twitch-cli event trigger streamdown -t {user.id} -u {stream_down_id} -T websocket"
    )

    raid_id = await eventsub.listen_channel_raid(RaidManager.handle_raid_mock, user.id)
    print(f"twitch-cli event trigger raid -t {user.id} -u {raid_id} -T websocket")

    try:
        # Press enter in the terminal to shutdown
        input("press Enter to shut down...\n")
    except KeyboardInterrupt:
        pass
    finally:
        # Stop all listeners before terminating
        print(colored("Shutting down", LogLevel.CONNECTION_MESSAGE.value))
        await eventsub.stop()
        await twitch.close()


asyncio.run(run())
