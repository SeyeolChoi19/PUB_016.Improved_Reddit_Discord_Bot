import discord, asyncio 

import datetime as dt 

from utilities.generic_functions.generic_functions import logger_initialization

class DiscordBot:
    def __init__(self):
        self.current_date    = dt.datetime.now().strftime("%Y-%m-%d")
        self.data_log_object = logger_initialization(f"{self.current_date} Discord Bot Log.log", "Discord bot operations")
    
    def discord_bot_settings(self, token_string: str):
        self.__token_string                    = token_string
        self.__discord_intents                 = discord.Intents.default()
        self.__discord_intents.message_content = True
        self.discord_client                    = discord.Client(intents = self.__discord_intents)
