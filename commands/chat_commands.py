import os
from twitchAPI.chat import ChatCommand
from twitchAPI.helper import first

from utilities.helper import Helpers
import models.globals


class ChatCommands:

    async def lurk(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("LURK")}")

    async def ping(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] pong")

    # --- --- --- --- --- BROADCASTER ONLY --- --- --- --- --- #

    async def update_title_cmd(cmd: ChatCommand):
        if len(cmd.text) > 1:
            await cmd.reply(f"[{models.globals._BOT_SIGIL}] Title updated")
            await models.globals._event_sub_handler_twitch.modify_channel_information(
                models.globals._PRIMARY_ACCOUNT_TWITCH_ID, None, None, cmd.text
            )
        else:
            await cmd.reply(f"[{models.globals._BOT_SIGIL}] Provide a value!")

    async def shout_out(cmd: ChatCommand):
        user = await first(
            models.globals._event_sub_handler_twitch.get_users(
                logins=Helpers.parse_command_text_single(cmd.text)
            )
        )
        await models.globals._event_sub_handler_twitch.send_a_shoutout(
            models.globals._PRIMARY_ACCOUNT_TWITCH_ID,
            user.id,
            models.globals._PRIMARY_ACCOUNT_TWITCH_ID,
        )
