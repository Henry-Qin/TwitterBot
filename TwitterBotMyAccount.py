__author__ = 'henryqin'

import tweepy                       #library to access Twitter
from time import sleep              #method to delay execution
from random import randrange        #method to produce random numbers in a range


ckey = "6EFOiqLUP2HU8WZsu8RjKGRNX"
csecret = "kzb36zr4MBF4kZCJw0kD4TPzs3rY0hhSYqbXugiYblToENVHrQ"
accesstoken = "3250287278-Ckzxz63hbgJdjMMqwmUHqq3MvOzTBreQsmZuVea"
tokensecret = "X5dJW5My1TaUDFe2o5KWzKht9K87WDjPZDR4aaOAqNtCZ"
user_sn = "twitter"
competitor_sn = "goodreads"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(accesstoken, tokensecret)

api = tweepy.API(auth)
competitor_followers_ids = api.followers_ids(competitor_sn)                     #length = 5000

query = "#books"
max_count = 1
search_results = api.search(q=query, count=max_count)
set_of_relevant_sn = {status.user.screen_name for status in search_results}     #remove duplicates using sets
list_of_relevant_sn = list(set_of_relevant_sn)

complete_list = list_of_relevant_sn + competitor_followers_ids[:1]

"""for follower in complete_list:
    api.create_friendship(follower)
    wait = randrange(0, 5)                                                      #random second interval
    sleep(wait)"""

print(api.show_friendship(user_sn, 'Bernice_Fischer'))

