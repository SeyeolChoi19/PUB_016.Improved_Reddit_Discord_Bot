import asyncio, praw, os, json

import datetime as dt 

from collections import deque
from threading   import Lock 

from concurrent.futures                            import ThreadPoolExecutor
from utilities.PrawInterface                       import PrawInterface
from utilities.generic_functions.generic_functions import logger_initialization

class CoreMonitoringLoop:
    def __init__(self) -> None:
        self.current_date    = dt.datetime.now().strftime("%Y-%m-%d")
        self.data_log_object = logger_initialization(f"{self.current_date} Reddit Monitoring Bot.log", "Reddit monitoring operations")

    def core_monitoring_loop_settings_method(self, sort_method: str, subreddits_list: list[str], memory_size: int = 1000, *args, **kwargs) -> None:
        self.sort_method        = sort_method
        self.subreddits_list    = subreddits_list
        self.memory_queue       = deque(maxlen = len(subreddits_list) * memory_size)
        self.reddit_api_object  = PrawInterface()
        self.thread_lock_object = Lock()
        self.reddit_api_object.praw_interface_settings_method(*args, **kwargs)

    async def __get_new_threads(self) -> list[dict | None]:
        loop = asyncio.get_running_loop()
        
        with ThreadPoolExecutor(max_workers = 4) as executor:
            futures = [loop.run_in_executor(executor, self.reddit_api_object.get_latest_threads, subreddit, self.sort_method, self.memory_queue) for subreddit in self.subreddits_list]
            results = await asyncio.gather(*futures)            

        return results
        
    async def core_loop(self) -> None:
        event_loop_object = asyncio.get_running_loop()

        while True:
            subreddit_threads = await self.__get_new_threads()
            new_thread_signal = any(subreddit_threads)

            if (new_thread_signal):
                for sub_dict in subreddit_threads:
                    if (sub_dict):
                        new_threads = await event_loop_object.run_in_executor(None, self.reddit_api_object.get_latest_threads, sub_dict["subreddit"][2:], self.sort_method, self.memory_queue, 30)
                        # Insert discord bot program here

            await asyncio.sleep(60 * 2)

    @staticmethod
    def execute_monitoring_loop(**config_dict):
        monitoring_program = CoreMonitoringLoop()
        monitoring_program.core_monitoring_loop_settings_method(**config_dict["CoreMonitoringLoop"]["core_monitoring_loop_settings_method"])
        asyncio.run(monitoring_program.core_loop())

if (__name__ == "__main__"):
    with open("./config/CoreMonitoringLoopConfig.json", "r", encoding = "utf-8") as f:
        config_dict = json.load(f)
    
    CoreMonitoringLoop.execute_monitoring_loop()


import asyncio, praw, os
reddit_api_object = praw.Reddit(
    client_id       = os.getenv("SUBREDDIT_CLIENT"),
    client_secret   = os.getenv("SUBREDDIT_SECRET"),
    user_agent      = "myscript by u/bboycage",
    username        = "u/bboycage",
    check_for_async = True
)
 
for thread in threads_list:
    print(thread.title)

threads_list = reversed(list(reddit_api_object.subreddit("programming").new(limit = 1)))