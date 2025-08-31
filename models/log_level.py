from enum import Enum


class LogLevel(Enum):
    CHANNEL_MESSAGE = "blue"
    ERROR_MESSAGE = "red"
    CONNECTION_MESSAGE = "yellow"
    SUCCESS_MESSAGE = "green"
    EVENT_SUB_NOTIF = "magenta"
