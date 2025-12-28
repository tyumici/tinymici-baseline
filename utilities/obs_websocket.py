import os
import time

from termcolor import colored
from obswebsocket import obsws, requests

from models.log_level import LogLevel


class OBSWebsocket:

    def start_obs_wss():
        retry_count = 0
        max_retries = 5
        wss_ip = os.getenv("TINYMICI_OBS_WSS_IP")
        wss_port = os.getenv("TINYMICI_OBS_WSS_PORT")
        wss_password = os.getenv("TINYMICI_OBS_WSS_PASSWORD")
        while retry_count < max_retries:
            try:
                client = obsws(wss_ip, wss_port, wss_password)
                client.connect()
                client.register(OBSWebsocket.on_event)
                print(
                    colored(f"OBS Connected: Version {client.call(requests.GetVersion()).getObsVersion()} ", LogLevel.SUCCESS_MESSAGE.value)
                )
            except Exception as e:
                print(
                    colored(
                        f"An unexpected error occurred: {e}",
                        LogLevel.ERROR_MESSAGE.value,
                    )
                )
            break

    def on_event(message):
        print("Got message: {}".format(message))
