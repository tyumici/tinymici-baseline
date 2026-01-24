import os
import threading
import time
from obswebsocket import obsws, requests


class OBSWebsocketThread(threading.Thread):
    def __init__(self):
        wss_ip = os.getenv("TINYMICI_OBS_WSS_IP")
        wss_port = os.getenv("TINYMICI_OBS_WSS_PORT")
        wss_password = os.getenv("TINYMICI_OBS_WSS_PASSWORD")

        threading.Thread.__init__(self)
        self.host = wss_ip
        self.port = wss_port
        self.password = wss_password
        self.ws = None
        self._stop_event = threading.Event()
        print(f"OBS Websocket Thread initialized for {wss_ip}:{wss_port}")

    def run(self):
        """Main method that runs in the thread to handle the websocket connection."""
        print("Connecting to OBS...")
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            print("Connected to OBS WebSocket.")
            
            # Example: Get the current scene collection name upon connection
            response = self.ws.call(requests.GetCurrentSceneCollectionName())
            if response.ok():
                print(f"Current Scene Collection: {response.responseData['sceneCollectionName']}")

            # Keep the thread alive until stop is called
            while not self._stop_event.is_set():
                time.sleep(0.1)

        except Exception as e:
            print(f"Connection error or exception: {e}")
        finally:
            if self.ws:
                self.ws.disconnect()
                print("Disconnected from OBS.")

    def stop(self):
        """Signals the thread to stop and disconnect."""
        self._stop_event.set()

    def set_scene(self, scene_name):
        """Example method to send a command from the main thread to OBS."""
        if self.ws and self.ws.is_connected():
            print(f"Attempting to set scene to: {scene_name}")
            try:
                # Use SetCurrentProgramScene for OBS v5+
                self.ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))
                print(f"Scene set to {scene_name}")
            except Exception as e:
                print(f"Could not set scene: {e}")
        else:
            print("Websocket not connected, cannot set scene.")
