import asyncio
import os

from twitchAPI.object.eventsub import ChannelAdBreakBeginEvent

import models.globals

class AdManager:

    async def on_ad_start(info: ChannelAdBreakBeginEvent):
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] Ads are in progress...",
        )
        await asyncio.sleep(60)
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] {os.getenv("DISCORD")}",
        )
        await asyncio.sleep(60)
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name,
            f"[{models.globals._BOT_SIGIL}] {os.getenv("BLUESKY")}",
        )
        await asyncio.sleep(60)
        await models.globals._chat_global.send_message(
            info.event.broadcaster_user_name, f"[{models.globals._BOT_SIGIL}] Ads are over!"
        )
