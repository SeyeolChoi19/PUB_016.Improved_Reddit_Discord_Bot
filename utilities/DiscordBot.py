import discord, asyncio 

import datetime as dt 

from utilities.generic_functions.generic_functions import logger_initialization
from utilities.generic_functions.generic_functions import operation_indicator
from utilities.generic_functions.generic_functions import logging_function

class DiscordBot:
    def __init__(self, token_string: str):
        self.current_date                      = dt.datetime.now().strftime("%Y-%m-%d")
        self.data_log_object                   = logger_initialization(f"{self.current_date} Discord Bot Log.log", "Discord bot operations")
        self.__discord_intents                 = discord.Intents.default()
        self.__discord_intents.message_content = True
        self.discord_client                    = discord.Client(intents = self.__discord_intents)
        self.__token_string                    = token_string
        self.__embedding_object                = None
            
    @property
    def embedding_object(self):
        return self.__embedding_object
    
    @embedding_object.setter
    def set_embedding(self, embedding_object: discord.Embed):
        self.__embedding_object = embedding_object

    @operation_indicator("Discord bot operation")
    def discord_bot_initialization(self):
        @self.discord_client.event
        async def on_read():
            print(f"{self.discord_client.user} is now running")

        @self.discord_client.event
        async def on_message(message: object):
            if (message.author == self.discord_client.user):
                return 
            
            username     = str(message.author)
            user_msg     = str(message.content)
            channel_name = str(message.channel)
            self.channel = message.channel
            logging_function(f"{username} said: {user_msg} ({channel_name})")

            if (user_msg == "?begin"):
                await channel_name.send("Beginning monitoring")
                await self.send_message()
        
        self.discord_client.run(self.__token_string)
            
    def __add_embedding_attributes(preview_text: str, results_dictionary: dict, embedding_object: discord.Embed):
        embedding_object.set_author(name = results_dictionary["subreddit"], url = f"https://www.reddit.com/{results_dictionary['subreddit']}/new")
        
        if (results_dictionary["thread_content"]):
            setattr(embedding_object, "description", preview_text)
        
        if (not results_dictionary["preview_yn"]):
            embedding_object.set_image(url = results_dictionary["preview_yn"]["images"][0]["resolutions"][len(results_dictionary["preview_yn"]["images"][0]["resolutions"]) - 1]["url"])

        embedding_object.add_field(name = '', value = f"[Thread Link]({results_dictionary['thread_url']})")

        return embedding_object

    @operation_indicator("Creating embeddings")
    def embed_message(self, results_dictionary: dict):
        temp_string  = f'{results_dictionary["thread_title"][0:200]}....'  if (len(results_dictionary["thread_title"]) >= 250) else results_dictionary["thread_title"]
        title_string = f"**{temp_string} (spoiler)**" if (results_dictionary["spoiler_yn"]) else f"**{temp_string}**"
        preview_text = f"{results_dictionary["thread_content"][0:300]}...." if (len(results_dictionary["thread_content"]) > 300) else results_dictionary["thread_content"]
        embed_object = discord.Embed(url = results_dictionary["thread_url"])
        embed_object.set_footer(text = f"Post by: /u/{results_dictionary['thread_author']}")
        setattr(embed_object, "title", title_string)

        return self.__add_embedding_attributes(preview_text, results_dictionary, embed_object)
    
    @operation_indicator("Sending embeddings")
    async def send_message(self):
        while True: 
            if (self.__embedding_object == None):
                await self.channel.send(embed = self.__embedding_object)