# Green Heat, by Prodzpod

- [Green Heat, by Prodzpod](#green-heat-by-prodzpod)
  - [Python Setup](#python-setup)
    - [GreenHeat Class](#greenheat-class)
    - [Main Thread](#main-thread)
  - [Values Received](#values-received)
    - [Websocket Message](#websocket-message)
    - [On the Coordinate Plane](#on-the-coordinate-plane)

An interactive click-map extension for Twitch.tv.

It's an enhanced version of the Heat plugin, allowing for dragging, hovering, release, and other features from within your streams video player on Twitch.

Checkout the author here [Prodzpod](https://www.twitch.tv/prodzpod)

[Home Page](https://heat.prod.kr/)

[Docs/Tutorials](https://heat.prod.kr/tutorial)

[Plugin Page](https://dashboard.twitch.tv/extensions/yvswtbzy4fj9h89rk06e0wuw2ghfwv)

You can test out the plugin while offline at `https://heat.prod.kr/[YOUR_CHANNEL_NAME]`

## Python Setup

### GreenHeat Class

A basic class to listen to the websocket. The sleep is optional but possibly needed based on activity present from the wss.

```python
# greenheat.py
import time

# install with pip install websockets
from websockets.sync.client import connect


class GreenHeat:

    def start_greenheat_wss():
        wss_address = "wss://heat.prod.kr/[YOUR_CHANNEL_NAME]"
        with connect(wss_address) as websocket:
            while True:
                message = websocket.recv()
                print('GreenHeat Event', message)
                # do work with the message
                time.sleep(0.2)
```

### Main Thread

This snippet will start the websocket from a `main.py` in its own thread as to prevent io blocking.

```python
# main.py
import threading

from utilities.greenheat import GreenHeat

#...

# Start GreenHeat
if enable_green_heat == 'true':
    threading.Thread(target=GreenHeat.start_greenheat_wss, daemon=True).start()

#...
```

## Values Received

### Websocket Message

The messages from the websocket are a standard JSON object with the following properties:

- id: Id of the user clicking, will be a twitch id, an anonymous id if prefixed with `A`, and a not logged in id if prefixed with `U`
- x: Decimal value of the x coordinate
- y: Decimal value of the y coordinate
- button: Mouse button used, can be `left`, `right`, or `middle`
- shift: Boolean value for if `shift` click was sent
- ctrl: Boolean value for if `ctrl` click was sent
- alt: Boolean value for if `alt` click was sent
- time: Integer epoch value for seconds, timestamp of when the click was formed
- latency: The stream latency between source and viewer
- type: Click event type, can be `click`, `drag`, `hover` or `release`

Note: This is super set of the original Heat Plugin output, so if you're migrating, it should be seamless.

### On the Coordinate Plane

Consider the XY plane to be the fourth quadrant on a coordinate grid, except where the Y values are positive.

The origin (0,0) is in the top left corner of the GreenHeat area.

Use this to specify events from specific regions of your stream viewport
```
(0,0)___________________________________________________________1(x)
|
|
|
|
|
|
|
|                            (0.5,0.5)
|
|
|
|
|
|
|
1(y)                                                             (1,1)
```
