import os

# Package
from twitchAPI.chat import ChatCommand

# Custom
import models.globals


class ChatInfo:
    """Basic info commands for chat, like links, socials, etc"""

    async def discord(cmd: ChatCommand):
        """Reply with your Discord link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("DISCORD")}")

    async def youtube(cmd: ChatCommand):
        """Reply with your Youtube link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("YOUTUBE")}")

    async def twitter(cmd: ChatCommand):
        """Reply with your Twitter link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("TWITTER")}")

    async def x(cmd: ChatCommand):
        """Reply with your X.com link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("X")}")

    async def bluesky(cmd: ChatCommand):
        """Reply with your Bluesky link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("BLUESKY")}")

    async def github(cmd: ChatCommand):
        """Reply with your Github link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}]{os.getenv("GITHUB")}")

    async def throne(cmd: ChatCommand):
        """Reply with your Throne link"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}] {os.getenv("THRONE")}")

    async def commands(cmd: ChatCommand):
        """Reply with a list of all of your ! commands"""
        await cmd.reply(f"[{models.globals._BOT_SIGIL}]{os.getenv("COMMANDS")}")
