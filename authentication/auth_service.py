# Package
from twitchAPI.chat import EventData
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from termcolor import colored

# Custom
from data.data_service import DataService
from models.permissions import TARGET_SCOPES
import models.globals
from models.log_level import LogLevel


class AuthService:
    """
    A service that creates and returns Twitch classes when passed
    authentication parameters
    """

    async def setup_bot_auth(auth_dict):
        """Create and return a Twitch instance of bot Twitch Class for chat commands"""

        models.globals._bot_handler_twitch = await Twitch(
            auth_dict["BOT_CLIENT_ID"], authenticate_app=False
        )
        # TODO does this even work
        models.globals._bot_handler_twitch.user_auth_refresh_callback = (
            AuthService.user_refresh
        )
        await models.globals._bot_handler_twitch.set_user_authentication(
            auth_dict["BOT_ACCESS_TOKEN"],
            TARGET_SCOPES,
            auth_dict["BOT_REFRESH_TOKEN"],
        )
        print(colored("Bot auth instantiated", LogLevel.SUCCESS_MESSAGE.value))
        return models.globals._bot_handler_twitch

    async def setup_event_sub_auth(auth_dict):
        """Create and return a Twitch instance for the Developer Console App for Event Sub usage"""

        models.globals._event_sub_handler_twitch = await Twitch(
            auth_dict["EVENTSUB_CLIENT_ID"], auth_dict["EVENTSUB_CLIENT_SECRET"]
        )
        auth = UserAuthenticator(
            models.globals._event_sub_handler_twitch, TARGET_SCOPES
        )
        token, refresh_token = await auth.authenticate()
        await models.globals._event_sub_handler_twitch.set_user_authentication(
            token, TARGET_SCOPES, refresh_token
        )
        print(colored("Event Sub auth instantiated", LogLevel.SUCCESS_MESSAGE.value))
        return models.globals._event_sub_handler_twitch

    def user_refresh(token: str, refresh_token: str):
        """Refresh Bot Tokens"""
        DataService.update_bot_tokens(token, refresh_token)

    async def on_ready(ready_event: EventData):
        """Print the Bot Ready event to the console once ready"""
        await ready_event.chat.join_room(models.globals._TARGET_CHANNELS)
        print(
            colored(
                f"[{models.globals._BOT_SIGIL} ] {models.globals._BOT_NAME} is ready",
                LogLevel.SUCCESS_MESSAGE.value,
            )
        )
