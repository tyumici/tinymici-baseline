from twitchAPI.chat.middleware import UserRestriction, ChannelRestriction
from twitchAPI.type import AuthScope
import models.globals

# Broadcaster only commands
BROADCASTER_ONLY_COMMAND = [
    UserRestriction(allowed_users=[models.globals._BROADCASTER_NAME])
]

# Broadcaster channel siloed commands
BROADCASTER_CHANNEL_MIDDLEWARE = [
    ChannelRestriction(allowed_channel=[models.globals._BROADCASTER_NAME])
]

# SHARED COMMAND MIDDLEWARE
# Add middleware here for commands you want to use in other streamers channels
"""
ex:
SHARED_MIDDLEWARE = [
    ChannelRestriction(
        allowed_channel=[
            "some_channel_1",
            "some_channel_2",
            "some_channel_3",
        ]
    )
]
"""

# SINGLE CHANNEL MIDDLEWARE
# Add middleware here for commands you only allow in specific channels
"""
ex:
SOME_CHANNEL_1_MIDDLEWARE = [ChannelRestriction(allowed_channel=["some_channel_1"])]
SOME_CHANNEL_2_MIDDLEWARE = [ChannelRestriction(allowed_channel=["some_channel_2"])]

"""

# Baseline Scopes, expand or reduce as needed
TARGET_SCOPES = [
    AuthScope.USER_BOT,
    AuthScope.USER_READ_CHAT,
    AuthScope.USER_WRITE_CHAT,
    AuthScope.CHAT_READ,
    AuthScope.CHAT_EDIT,
    AuthScope.MODERATOR_READ_FOLLOWERS,
    AuthScope.MODERATOR_MANAGE_BANNED_USERS,
    AuthScope.MODERATOR_MANAGE_CHAT_MESSAGES,
    AuthScope.MODERATOR_READ_SHOUTOUTS,
    AuthScope.MODERATOR_MANAGE_SHOUTOUTS,
    AuthScope.CHANNEL_BOT,
    AuthScope.CHANNEL_MANAGE_ADS,
    AuthScope.CHANNEL_MANAGE_BROADCAST,
    AuthScope.CHANNEL_MANAGE_POLLS,
    AuthScope.CHANNEL_MANAGE_RAIDS,
    AuthScope.CHANNEL_MANAGE_REDEMPTIONS,
    AuthScope.CHANNEL_MANAGE_VIPS,
    AuthScope.CHANNEL_MODERATE,
    AuthScope.CHANNEL_READ_ADS,
    AuthScope.CHANNEL_READ_POLLS,
    AuthScope.CHANNEL_READ_REDEMPTIONS,
    AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
    AuthScope.CHANNEL_READ_VIPS,
]
