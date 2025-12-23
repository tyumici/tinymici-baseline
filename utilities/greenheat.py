import asyncio
import os
import time

from termcolor import colored
from websockets.sync.client import connect
import websockets

from models.log_level import LogLevel


class GreenHeat:

    def start_greenheat_wss():
        """Start a websocket to receive events from GreenHeat"""

        retry_count = 0
        max_retries = 5
        wss_address = os.getenv("TINYMICI_GREENHEAT_WSS")
        while retry_count < max_retries:
            try:
                with connect(wss_address) as websocket:
                    print(colored("GreenHeat Connected", LogLevel.SUCCESS_MESSAGE.value))
                    while True:
                        message = websocket.recv()
                        print(colored(f"GreenHeat Message: {message}", LogLevel.WEBSOCKET_MESSAGE.value))
                        retry_count = 0
                        time.sleep(0.2)
            except websockets.exceptions.ConnectionClosed:
                retry_count += 1
                wait_time = 2 ** retry_count
                print(colored(f"Connection closed, attempting to reconnect in {wait_time} seconds...", LogLevel.CONNECTION_MESSAGE.value))
                GreenHeat.start_greenheat_wss()
                time.sleep(0.2)
            except Exception as e:
                print(colored(f"An unexpected error occurred: {e}", LogLevel.ERROR_MESSAGE.value))
            break
