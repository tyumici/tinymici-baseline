# Package
from twitchAPI.chat import Chat
from twitchAPI.type import ChatEvent
from twitchAPI.twitch import Twitch

# Custom
from commands.chat_info import ChatInfo
from commands.chat_commands import ChatCommands
from utilities.helper import Helpers
from models.permissions import BROADCASTER_CHANNEL_MIDDLEWARE, BROADCASTER_ONLY_COMMAND
import models.globals


async def setupChatGlobal(twitch: Twitch):
    """
    Create and return a Chat instance for chat commands.
    Add command registrations here to register chat actions within this function
    """
    models.globals._chat_global = await Chat(twitch)
    models.globals._chat_global.register_event(ChatEvent.READY, Helpers.on_ready)

    # --- --- --- --- --- INFO COMMANDS --- --- --- --- --- #

    models.globals._chat_global.register_command(
        "discord", ChatInfo.discord, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "youtube", ChatInfo.youtube, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "twitter", ChatInfo.twitter, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "x", ChatInfo.x, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "bluesky", ChatInfo.bluesky, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "github", ChatInfo.github, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "throne", ChatInfo.throne, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )
    models.globals._chat_global.register_command(
        "commands", ChatInfo.commands, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )

    # --- --- --- --- --- CHAT ACTIONS --- --- --- --- --- #

    models.globals._chat_global.register_command(
        "lurk", ChatCommands.lurk, command_middleware=BROADCASTER_ONLY_COMMAND
    )
    models.globals._chat_global.register_command(
        "ping", ChatCommands.ping, command_middleware=BROADCASTER_CHANNEL_MIDDLEWARE
    )

    # --- --- --- --- --- BROADCASTER ONLY --- --- --- --- --- #

    models.globals._chat_global.register_command(
        "updateTitle",
        ChatCommands.update_title_cmd,
        command_middleware=BROADCASTER_ONLY_COMMAND,
    )

    models.globals._chat_global.register_command(
        "so", ChatCommands.shout_out, command_middleware=BROADCASTER_ONLY_COMMAND
    )

    return models.globals._chat_global
