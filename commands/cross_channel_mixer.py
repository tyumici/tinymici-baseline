# Package
from twitchAPI.chat import ChatMessage
from termcolor import colored


class CrossChannelService:
    """
    Provides local logging for all messages received from channels the bot is listening to.
    
    You can provide custom functionality here to perform actions on messages from these subscribed channels.
    
    For example, a user sends term-x in a subscribed channel and you want the bot to reply in that channel.
    
    Please use this with caution and confirmation from the other party(s)
    """

    async def on_any_message(msg: ChatMessage):
        """Prints a message to the local console on any message from subscribed channels"""
        print(
            colored(
                f"{f"Channel: {msg.room.name}, User: {msg.user.display_name}, Message: {msg.text}"}",
                "blue",
            )
        )
