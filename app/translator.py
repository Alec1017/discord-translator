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

            try: 
                self._send_json_request(heartbeat_json)
            except ConnectionResetError:
                print('[bold red]WARNING: Connection was reset by Discord. Reconnecting the socket...[/bold red]')
                self.initiate_connection()
                print('[bold green]Socket was successfully reset. Resuming translation...[/bold green]')
            except:
                pass

    def _display_message(self, message):
        username = message['author']['username']
        message_text = message['content']

        # detect the language of the text
        detection = self.translator.detect(message_text)

        # if the text is in the specified language, then translate it
        if detection.lang.lower() == self.config.LANGUAGE_FROM.lower():
            message_text = self.translator.translate(message_text, dest=self.config.LANGUAGE_TO).text

        print(f"[bold yellow]{username}[/bold yellow]: {message_text}")

    def initiate_connection(self):

        # connection the websocket to the discord gateway
        self.ws = websocket.WebSocket()
        self.ws.connect(self.config.DISCORD_GATEWAY)

        # create a google translator object
        self.translator = Translator()

        # begin the heartbeat thread
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

        # send the initial connection payload
        self._send_json_request(payload)

    def load_initial_messages(self):
        headers = {
            'authorization': self.config.TOKEN
        }

        options = {
            'limit': 10
        }

        # retrieve the 10 most recent messages from the channel
        response = requests.get(self.config.DISCORD_API, headers=headers, params=options)
        messages = json.loads(response.text)
        for message in reversed(messages):
            try:
                self._display_message(message)
            except:
                pass

    def load_realtime_messages(self):
        while True: 
            response = self._receive_json_response()
            response_content = response['d']
            
            try: 
                # only retrieve messages from the desired discord channel
                if response_content['channel_id'] == self.config.CHANNEL_ID:
                    self._display_message(response_content)

            except ConnectionResetError:
                print('[bold red]WARNING: Connection was reset by Discord. Reconnecting the socket...[/bold red]')
                self.initiate_connection()
                print('[bold green]Socket was successfully reset. Resuming translation...[/bold green]')
            except:
                pass
