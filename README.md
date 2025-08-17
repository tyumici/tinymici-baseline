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
    - [Linting and Formatting](#linting-and-formatting)
    - [Running](#running)

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
  - Make sure to provide it with all the necessary auth scopes (TODO ADD BASE SCOPES HERE)
- Create a Developer Application for your **Primary Account** via the [Twitch Developer Console](https://dev.twitch.tv/console/apps)

This effectively allows for the **Bot Account** to respond to commands, send messages, etc, while also allowing eventsub handling from your **Primary Account**. 

If someone actually knows if this is correct or not, please let me know, it's just how I managed to get it working :3

#### Populating the DB

The type is unique, and the schema is as follows:
- EVENT_SUB_CLIENT_ID: This is your client id from your **Primary Account**
- EVENT_SUB_CLIENT_SECRET: This is your client secret from your **Primary Account**
- BOT_CLIENT_ID: The client id from your **Bot Account**
- BOT_ACCESS_TOKEN: This is the access token from your **Bot Account**
- BOT_REFRESH_TOKEN: This is the refresh token from your **Bot Account**

### Databasing

Tinymici is built to hook to a proper relational database, MariaDB in this case. You're free to choose whichever backend your prefer, just note that the `data_service.py` is setup for mysql connections.

If you have no need for a database, just comment out the `connPrimary = DataService.connect_primary()` in `main.py`

For the DB credentials, you can use a .env or hardcode them in. If you're running a local DB on your local network, without external access, there shouldn't be harm in that.

### Global Variables

### Linting and Formatting

Please do run `flake8 .` and `black .` to lint and format the app.

### Running

I host my bot on a raspberry pi on my local network. Just activate the virtual environment, and run `python main.py` and the bot will spin up.

The TwitchAPI appears to have reconnect features, so that should be handled automatically. If you're running a database, there are also built in ping checks to the db, and a task to reconnect on a schedule.

