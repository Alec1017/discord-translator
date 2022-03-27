import websocket
import json
import threading
import time
import requests
import os

from googletrans import Translator
from rich import print
# from dotenv import load_dotenv

# base_dir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

TOKEN = "MTkwODk1OTU5MzgxNzcwMjQx.YYb5RQ.1-VcAUZoOCcbzHnkRj0D6ONWvNE" # os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = '956990761835053067'
DISCORD_GATEWAY = 'wss://gateway.discord.gg/?v=9&encoding=json'
DISCORD_API = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'

ws = None
translator = None

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response: 
        return json.loads(response)

def heartbeat(interval, ws):
    while True:
        time.sleep(interval)
        heartbeat_json = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeat_json)

def display_message(message):
    global translator

    username = message['author']['username']
    message_text = message['content']
    detection = translator.detect(message_text)

    if detection.lang == 'zh-CN':
        message_text = translator.translate(message_text).text

    print(f"[bold yellow]{username}[/bold yellow]: {message_text}")

def initiate_connection():
    global ws
    global translator

    ws = websocket.WebSocket()
    translator = Translator()
    ws.connect(DISCORD_GATEWAY)
    event = receive_json_response(ws)

    heartbeat_interval = event['d']['heartbeat_interval'] / 1000
    threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

    payload = {
        'op': 2,
        'd': {
            'token': TOKEN,
            'properties': {
                "$os": "linux",
                "$browser": "chrome",
                "$device": "pc"
            }
        }
    }
    send_json_request(ws, payload)

def load_initial_messages():
    headers = {
        'authorization': TOKEN
    }

    options = {
        'limit': 10
    }

    r = requests.get(DISCORD_API, headers=headers, params=options)

    j = json.loads(r.text)
    for message in reversed(j):
        display_message(message)

def load_realtime_messages():
    global ws

    while True: 
        response = receive_json_response(ws)
        response_content = response['d']

        try: 
            
            if response_content['channel_id'] == CHANNEL_ID:
                display_message(response_content)

        except ConnectionResetError:
            print('connection reset error. Restarting socket connection...')
            initiate_connection()
            print('connection restarted')
        except:
            pass


initiate_connection()
load_initial_messages()
load_realtime_messages()
