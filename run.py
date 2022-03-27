from app.translator import DiscordTranslator
from config import BaseConfig

discordTranslator = DiscordTranslator(BaseConfig)

discordTranslator.initiate_connection()
discordTranslator.load_initial_messages()
discordTranslator.load_realtime_messages()