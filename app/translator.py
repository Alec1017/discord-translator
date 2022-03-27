import websocket
import json
import threading
import time
import requests
import os

from googletrans import Translator
from rich import print


class DiscordTranslator:

    def __init__(self, config):
        self.config = config
        self.ws = None
        self.translator = None

    def _send_json_request(self, request):
        self.ws.send(json.dumps(request))

    def _receive_json_response(self):
        response = self.ws.recv()
        if response: 
            return json.loads(response)

    def _heartbeat(self, interval):
        while True:
            time.sleep(interval)
            heartbeat_json = {
                "op": 1,
                "d": "null"
            }
            self._send_json_request(heartbeat_json)

    def _display_message(self, message):
        username = message['author']['username']
        message_text = message['content']
        detection = self.translator.detect(message_text)

        if detection.lang == 'zh-CN':
            message_text = self.translator.translate(message_text).text

        print(f"[bold yellow]{username}[/bold yellow]: {message_text}")

    def initiate_connection(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(self.config.DISCORD_GATEWAY)

        self.translator = Translator()

        event = self._receive_json_response()
        heartbeat_interval = event['d']['heartbeat_interval'] / 1000
        threading._start_new_thread(self._heartbeat, (heartbeat_interval, ))

        payload = {
            'op': 2,
            'd': {
                'token': self.config.TOKEN,
                'properties': {
                    "$os": "linux",
                    "$browser": "chrome",
                    "$device": "pc"
                }
            }
        }
        self._send_json_request(payload)

    def load_initial_messages(self):
        headers = {
            'authorization': self.config.TOKEN
        }

        options = {
            'limit': 10
        }

        response = requests.get(self.config.DISCORD_API, headers=headers, params=options)
        messages = json.loads(response.text)
        for message in reversed(messages):
            self._display_message(message)

    def load_realtime_messages(self):
        while True: 
            response = self._receive_json_response()
            response_content = response['d']

            try: 
                if response_content['channel_id'] == self.config.CHANNEL_ID:
                    self._display_message(response_content)

            except ConnectionResetError:
                print('connection reset error. Restarting socket connection...')
                self.initiate_connection()
                print('connection restarted')
            except:
                pass
