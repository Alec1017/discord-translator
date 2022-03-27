import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    TOKEN = os.environ.get('TOKEN')
    CHANNEL_ID = str(os.environ.get('CHANNEL_ID'))
    DISCORD_GATEWAY = 'wss://gateway.discord.gg/?v=9&encoding=json'
    DISCORD_API = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'