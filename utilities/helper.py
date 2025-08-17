import time

from datetime import datetime, timedelta
from twitchAPI.chat import EventData
import models.globals

class Helpers:

# --- --- --- --- --- FORMATTERS --- --- --- --- --- #

    def get_now_plus_hours(delta: int):
        '''Gets the current time plus the provided hours and returns that timestamp'''
        current_time = datetime.now()
        new_time = current_time + timedelta(hours=delta)
        return int(time.mktime(new_time.timetuple()))

    def row_to_dict(row):
        '''Convert a row from a database into a JSON like dict'''
        return {col: row[col] for col in row.keys()}
    
    def parse_command_text_single(msg: str):
        '''Used to parse a message from a ! command'''
        spacedMsg = msg.split()
        spacedMsg.pop(0)
        results = ' '.join(spacedMsg)
        return results

# --- --- --- --- --- MISC --- --- --- --- --- #

    async def on_ready(ready_event: EventData):
        '''Bot on ready event'''
        await ready_event.chat.join_room(models.globals._TARGET_CHANNELS)
        print(f'[{models.globals._BOT_SIGIL} ] {models.globals._BOT_NAME} is ready')
