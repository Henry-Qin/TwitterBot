__author__ = 'henryqin'

import configparser
from random import uniform
import sched, time
from datetime import datetime

Config = configparser.ConfigParser()
Config.read(["TwitterBotConfig"])                                   #specified configuration file

def ConfigSectionMap(section):                                      #from PythonWiki
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


import tweepy                       #library to access Twitter
from random import uniform        #method to produce random numbers in a range

ckey = ConfigSectionMap("APIAccess")["consumerkey"]
csecret = ConfigSectionMap("APIAccess")["consumersecret"]
accesstoken = ConfigSectionMap("APIAccess")["accesstoken"]
tokensecret = ConfigSectionMap("APIAccess")["secrettoken"]
user_sn = ConfigSectionMap("ScreenNames")["user_sn"]
competitor_sn = ConfigSectionMap("ScreenNames")["competitor_sn"]

s = sched.scheduler(time.time, time.sleep)                                                  #instance of the scheduler

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(accesstoken, tokensecret)

api = tweepy.API(auth)
competitor_followers_ids = api.followers_ids(competitor_sn)                                 #length = 5000

query = ConfigSectionMap('FollowCriteria')["query"]
max_count = int(ConfigSectionMap('Limits')["max_count"])                                        #max number of posts to retrieve (>0)
search_results = api.search(q=query, count=max_count)
set_of_relevant_id = {status.user.id for status in search_results}                          #remove duplicates using sets
list_of_relevant_id = list(set_of_relevant_id)

max_competitor_followers = int(ConfigSectionMap('Limits')["max_competitor_followers"])           #max number of followers to retrieve
complete_list = list_of_relevant_id + competitor_followers_ids[:max_competitor_followers]
objects = api.lookup_friendships(complete_list)
filtered_list = [user.id for user in objects if not user.is_following]

today_obj = datetime.today()
weekday= today_obj.weekday()                    # Monday = 0, Sunday = 6

if weekday < 4:
    peak_begin = ConfigSectionMap('PeakInterval')['peak_begin_normal']
    peak_end = ConfigSectionMap('PeakInterval')['peak_end_normal']
    a_coefficient_upper = ConfigSectionMap('EquationCoefficients')['a_upper_normal']
    a_coefficient_lower = ConfigSectionMap('EquationCoefficients')['a_lower_normal']
    b_coefficient_upper = ConfigSectionMap('EquationCoefficients')['b_upper_normal']
    b_coefficient_lower = ConfigSectionMap('EquationCoefficients')['b_lower_normal']
    c_coefficient_upper = ConfigSectionMap('EquationCoefficients')['c_upper_normal']
    c_coefficient_lower = ConfigSectionMap('EquationCoefficients')['c_lower_normal']
elif weekday == 5:
    peak_begin = ConfigSectionMap('PeakInterval')['peak_begin_friday']
    peak_end = ConfigSectionMap('PeakInterval')['peak_end_friday']
    a_coefficient_upper = ConfigSectionMap('EquationCoefficients')['a_upper_friday']
    a_coefficient_lower = ConfigSectionMap('EquationCoefficients')['a_lower_friday']
    b_coefficient_upper = ConfigSectionMap('EquationCoefficients')['b_upper_friday']
    b_coefficient_lower = ConfigSectionMap('EquationCoefficients')['b_lower_friday']
    c_coefficient_upper = ConfigSectionMap('EquationCoefficients')['c_upper_friday']
    c_coefficient_lower = ConfigSectionMap('EquationCoefficients')['c_lower_friday']
elif weekday == 6:
    peak_begin = ConfigSectionMap('PeakInterval')['peak_begin_saturday']
    peak_end = ConfigSectionMap('PeakInterval')['peak_end_saturday']
    a_coefficient_upper = ConfigSectionMap('EquationCoefficients')['a_upper_saturday']
    a_coefficient_lower = ConfigSectionMap('EquationCoefficients')['a_lower_saturday']
    b_coefficient_upper = ConfigSectionMap('EquationCoefficients')['b_upper_saturday']
    b_coefficient_lower = ConfigSectionMap('EquationCoefficients')['b_lower_saturday']
    c_coefficient_upper = ConfigSectionMap('EquationCoefficients')['c_upper_saturday']
    c_coefficient_lower = ConfigSectionMap('EquationCoefficients')['c_lower_saturday']
else:
    peak_begin = ConfigSectionMap('PeakInterval')['peak_begin_sunday']
    peak_end = ConfigSectionMap('PeakInterval')['peak_end_sunday']
    a_coefficient_upper = ConfigSectionMap('EquationCoefficients')['a_upper_sunday']
    a_coefficient_lower = ConfigSectionMap('EquationCoefficients')['a_lower_sunday']
    b_coefficient_upper = ConfigSectionMap('EquationCoefficients')['b_upper_sunday']
    b_coefficient_lower = ConfigSectionMap('EquationCoefficients')['b_lower_sunday']
    c_coefficient_upper = ConfigSectionMap('EquationCoefficients')['c_upper_sunday']
    c_coefficient_lower = ConfigSectionMap('EquationCoefficients')['c_lower_sunday']

def equation(a,b,c):
    return 5*a*a + 5*b + c

for follower in filtered_list:
    peak_begin_obj = datetime.strptime(peak_begin, "%H:%M:%S")
    peak_end_obj = datetime.strptime(peak_end, "%H:%M:%S")
    current_time_obj = datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S")
    if current_time_obj > peak_begin_obj and current_time_obj< peak_end_obj:        #within peak
        peak_multiplier = ConfigSectionMap('EquationCoefficients')['peak_multiplier']
        a = float(peak_multiplier) * uniform(int(a_coefficient_lower), int(a_coefficient_upper))
        b = float(peak_multiplier) * uniform(int(b_coefficient_lower), int(b_coefficient_upper))
        c = float(peak_multiplier) * uniform(int(c_coefficient_lower), int(c_coefficient_upper))
        delay = equation(a, b, c)
        print(delay)
        s.enter(delay, 1, api.create_friendship, [follower])
        s.run()
    elif current_time_obj < peak_begin_obj or current_time_obj> peak_end_obj:      #outside peak
        a = uniform(int(a_coefficient_lower), int(a_coefficient_upper))
        b = uniform(int(b_coefficient_lower), int(b_coefficient_upper))
        c = uniform(int(c_coefficient_lower), int(c_coefficient_upper))
        delay = equation(a, b, c)
        s.enter(delay, 1, api.create_friendship, [follower])
        s.run()

def ratio(followers,following):
    return followers/following

desired_ratio = float(ConfigSectionMap('Limits')["follow_ratio"])
all_followers_list = api.followers_ids(user_sn)
all_following_list = api.friends_ids(user_sn)
current_ratio = ratio(len(all_followers_list),len(all_following_list))

while current_ratio < desired_ratio:
    rand_int = randrange(len(all_following_list))
    api.destroy_friendship(all_following_list[rand_int])
    current_ratio = ratio(len(api.followers_ids(user_sn)), len(api.friends_ids(user_sn)))

