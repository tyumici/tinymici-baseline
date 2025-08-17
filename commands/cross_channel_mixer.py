from twitchAPI.chat import ChatMessage
from termcolor import colored

class CrossChannelService():

    async def on_any_message(msg: ChatMessage):
        print(colored(f"{f"Channel: {msg.room.name}, User: {msg.user.display_name}, Message: {msg.text}"}", 'blue'))
