# tinymici-baseline

A baseline Twitch bot made in Python 3.13.5
- [tinymici-baseline](#tinymici-baseline)
  - [Rationale](#rationale)
  - [Setup](#setup)
    - [Project Init](#project-init)
    - [Secrets](#secrets)
      - [Getting Auth Tokens](#getting-auth-tokens)
      - [Populating the DB](#populating-the-db)
    - [Databasing](#databasing)
    - [Global Variables](#global-variables)
      - [Twitch Classes](#twitch-classes)
      - [Env Variables](#env-variables)
    - [Linting and Formatting](#linting-and-formatting)
    - [Running](#running)
  - [Testing With twitch-cli](#testing-with-twitch-cli)
    - [Setup](#setup-1)
    - [Start Local API](#start-local-api)
    - [Simulating events](#simulating-events)

## Rationale

I wanted to make my own bot to run more complex commands and actions than all the current ones that are mass available. I also wanted to learn a language other than JS/TS, which is why this is in python. 

This is a rewrite of the original tinymici, making it far more usable, flexible, and generally more sane to work within. Hopefully you can use this as a good start point for your bot. Please do feel free to fork and update!

## Setup

### Project Init

- Clone the repo: `git clone https://github.com/tyumici/tinymici-baseline.git`
- Create a virtual environment: `python -m venv venv`
- Activate the environment `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Secrets

This application uses a different approach to secrets management. I have opted to store secrets in a `secrets.db` sqlite file in the root of the project. This is due to this bot application being for live streams. Users typically would have a `.env` file for this, but that can accidentally be shown on stream, whereas having a binary db file eliminates this issue.

I use [DB Browser](https://sqlitebrowser.org/) to simply create the DB with a single table: 

```sql
CREATE TABLE "secrets" (
	"type"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
	PRIMARY KEY("type")
)
```

#### Getting Auth Tokens

Due to the nature of the TwitchAPI python library, or my own misunderstanding of how things work, authentication for this bot is two pronged. 

You will need to:

- Create a token for your **Bot Account** via the [Twitch Token Generator](https://twitchtokengenerator.com/)
  - Make sure to provide it with all the necessary auth scopes, this app uses the scopes added in TARGET_SCOPES from [permissions.py](./models/permissions.py)
- Create a Developer Application for your **Broadcaster Account** via the [Twitch Developer Console](https://dev.twitch.tv/console/apps)

This effectively allows for the **Bot Account** to respond to commands, send messages, etc, while also allowing eventsub handling from your **Broadcaster Account**. 

If someone actually knows if this is correct or not, please let me know, it's just how I managed to get it working :3

#### Populating the DB

The type is unique, and the schema is as follows:
- EVENT_SUB_CLIENT_ID: This is your client id from your **Broadcaster Account**
- EVENT_SUB_CLIENT_SECRET: This is your client secret from your **Broadcaster Account**
- BOT_CLIENT_ID: The client id from your **Bot Account**
- BOT_ACCESS_TOKEN: This is the access token from your **Bot Account**
- BOT_REFRESH_TOKEN: This is the refresh token from your **Bot Account**

### Databasing

Tinymici is built to hook to a proper relational database, MariaDB in this case. You're free to choose whichever backend your prefer, just note that the `data_service.py` is setup for mysql connections.

If you have no need for a database, just comment out the `connPrimary = DataService.connect_primary()` in `main.py`

For the DB credentials, you can use a .env or hardcode them in. If you're running a local DB on your local network, without external access, there shouldn't be harm in that.

### Global Variables

This bot application utilizes a central globals file for variables that need to be passed between classes.

These can be found in the [globals.py](./models/globals.py)

#### Twitch Classes

Global instance of Twitch classes for handling and performing events

- _chat_global: The global Chat class instance for your bot
- _bot_handler_twitch: The global Twitch class instance for your bot
- _event_sub_handler_twitch: The global EventSub class instance for your broadcaster account

#### Env Variables

Variables taken from the local .env file

These all have comments on their associated usage, or are named in a manner that convey purpose.

### Linting and Formatting

Please do run `flake8 .` and `black .` to lint and format the app.

### Running

I host my bot on a raspberry pi on my local network. Just activate the virtual environment, and run `python main.py` and the bot will spin up.

The TwitchAPI appears to have reconnect features, so that should be handled automatically. If you're running a database, there are also built in ping checks to the db, and a task to reconnect on a schedule.

## Testing With twitch-cli

### Setup

Setup and install the `twitch-cli` via the official docs found [here](https://dev.twitch.tv/docs/cli/)

Can also be found on the AUR [here](https://aur.archlinux.org/packages/twitch-cli)

### Start Local API

You will need to start a mock api and websocket for eventsub events:

Run: `twitch-cli mock-api start -p 8000` to start the mock api on local port 8000

Run `twitch-cli event websocket start` to start the websocket on local port 8080 (by default)

Feel free to use any ports, make sure to update [test.py](./test.py) if you do. The mock-api is set to port 8000, and the websocket is on the default 8080.

To connect to the local api and websocket, run `python test.py`

### Simulating events

All events that the CLI can trigger can be found at the docs [here](https://github.com/twitchdev/twitch-cli/blob/main/docs/event.md)

In [test.py](./test.py) the event sub is setup to handle a few common events"
- Channel Point Redeem
- Channel Follow
- Channel Subscribe
- Stream End
- Channel Raid Receive

The pattern utilized is as follows

```python
follow_id = await eventsub.listen_channel_follow_v2(user.id, user.id, FollowService.on_follow_mock)
print(f'twitch-cli event trigger follow -t {user.id} -u {follow_id} -T websocket')
```

In the above snippet the printed line is what you will copy and enter into your terminal to trigger the event.

The base event sub handlers in this application have a partner _mock function that simply prints the event that was received.