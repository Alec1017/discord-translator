from app.translator import DiscordTranslator
from config import BaseConfig

# create an instance of the discord translator
discordTranslator = DiscordTranslator(BaseConfig)

# run the translator
discordTranslator.initiate_connection()
discordTranslator.load_initial_messages()
discordTranslator.load_realtime_messages()
