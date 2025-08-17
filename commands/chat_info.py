import os
from twitchAPI.chat import ChatCommand
import models.globals


class ChatInfo:
    """Basic info commands for chat"""

    # My links
    async def discord(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("DISCORD")}")

    async def youtube(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("YOUTUBE")}")

    async def twitter(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("TWITTER")}")

    async def x(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("X")}")

    async def bluesky(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("BLUESKY")}")

    async def github(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}]{os.getenv("GITHUB")}")

    async def throne(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("THRONE")}")

    async def commands(cmd: ChatCommand):
        await cmd.reply(f"[{models.globals._BOT_SIGIL}]{os.getenv("COMMANDS")}")
