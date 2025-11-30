import praw, os

from collections import deque
from typing      import Union

class PrawInterface:
    def praw_interface_settings_method(self, client_id_variable: str, client_secret_variable: str, user_agent: str, username: str):
        self.reddit_api_object = praw.Reddit(
            client_id       = os.getenv(client_id_variable),
            client_secret   = os.getenv(client_secret_variable),
            user_agent      = user_agent, 
            username        = username,
            check_for_async = True
        )

    def get_latest_threads(self, subreddit: str, sort_method: str, memory_bank: Union[list[str] | deque], fetch_size: int = 1) -> dict | None:
        match (sort_method.lower()):
            case "new" : threads_list = reversed(list(self.reddit_api_object.subreddit(subreddit.lower()).new(limit = fetch_size)))
            case "top" : threads_list = reversed(list(self.reddit_api_object.subreddit(subreddit.lower()).top(limit = fetch_size)))
            case "hot" : threads_list = reversed(list(self.reddit_api_object.subreddit(subreddit.lower()).hot(limit = fetch_size)))
            
        results_dictionary = None

        for thread in threads_list: 
            if (thread.permalink not in memory_bank):
                results_dictionary = {
                    "subreddit"      : f"r/{subreddit}",
                    "thread_url"     : f"https://www.reddit.com{thread.permalink}",
                    "thread_title"   : thread.title,
                    "thread_content" : thread.selftext,
                    "thread_author"  : thread.author.name
                }
            
            if ((fetch_size > 1) and (thread.permalink not in memory_bank)):
                memory_bank.append(thread.permalink)

        return results_dictionary 