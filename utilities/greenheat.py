import os
import time

from websockets.sync.client import connect


class GreenHeat:

    def start_greenheat_wss():
        """Start a websocket to receive events from GreenHeat"""

        wss_address = os.getenv("TINYMICI_GREENHEAT_WSS")
        with connect(wss_address) as websocket:
            while True:
                message = websocket.recv()
                print('GREENHEAT', message)
                time.sleep(0.2)
