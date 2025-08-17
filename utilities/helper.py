import time
from datetime import datetime, timedelta

# Package
from twitchAPI.chat import EventData

# Custom
import models.globals


class Helpers:

    # --- --- --- --- --- FORMATTERS --- --- --- --- --- #

    def get_now_plus_hours(delta: int):
        """Gets the current time plus the provided hours and returns that timestamp"""
        current_time = datetime.now()
        new_time = current_time + timedelta(hours=delta)
        return int(time.mktime(new_time.timetuple()))

    def parse_command_text_single(msg: str):
        """
        Used to parse a message from a ! command and get the content after the command used
        """
        spacedMsg = msg.split()
        spacedMsg.pop(0)
        results = " ".join(spacedMsg)
        return results

    # --- --- --- --- --- MISC --- --- --- --- --- #

    async def on_ready(ready_event: EventData):
        """Bot on ready event, sends a console print when ready is achieved"""
        await ready_event.chat.join_room(models.globals._TARGET_CHANNELS)
        print(f"[{models.globals._BOT_SIGIL} ] {models.globals._BOT_NAME} is ready")
