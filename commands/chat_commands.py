import os

# Package
from twitchAPI.chat import ChatCommand
from twitchAPI.helper import first

# Custom
from utilities.helper import Helpers
import models.globals


class ChatCommands:
    """Chat commands that perform work, or are not solely informational"""

    async def lurk(cmd: ChatCommand):
        """Lets the Broadcaster know you're lurking"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("TINYMICI_LURK")}")

    async def ping(cmd: ChatCommand):
        """Effectively a live check for chat to the Bot"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] pong")

    # --- --- --- --- --- BROADCASTER ONLY --- --- --- --- --- #

    async def update_title_cmd(cmd: ChatCommand):
        """Updates the current broadcast title"""
        # TODO add a length check for max title at 140 char
        if len(cmd.text) > 1:
            await cmd.reply(f"[{models.globals._BOT_SIGIL}] Title updated")
            await models.globals._event_sub_handler_twitch.modify_channel_information(
                models.globals._BROADCASTER_TWITCH_ID,
                None,
                None,
                Helpers.parse_command_text_single(cmd.text),
            )
        else:
            await cmd.reply(f"[{models.globals._BOT_SIGIL}] Provide a value!")

    async def shout_out(cmd: ChatCommand):
        """Give a shout out to the provided user"""

        # Get the user via their username from the command
        user = await first(
            models.globals._event_sub_handler_twitch.get_users(
                logins=Helpers.parse_command_text_single(cmd.text)
            )
        )
        await models.globals._event_sub_handler_twitch.send_a_shoutout(
            models.globals._BROADCASTER_TWITCH_ID,
            user.id,
            models.globals._BROADCASTER_TWITCH_ID,
        )
