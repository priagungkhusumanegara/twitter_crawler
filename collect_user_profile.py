__author__ = "Priagung Khusumanegara"
__copyright__ = "Copyright 2018, Twitter Crawler"
__credits__ = ["Twitter API"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Prigung Khusumanegara"
__email__ = "priagung.123@gmail.com"
__status__ = "Development"

#import lib
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import csv

#API credential
consumer_key = "<consumer key>"
consumer_secret = "<consumer secret>"
access_token = "<consumer token>"
access_token_secret = "<access_token_secret>"
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

auth_api = API(auth, wait_on_rate_limit=True)


with open('list.txt', 'r') as targets_file:
     targets_list = targets_file.readlines()

account_list = []

for item in targets_list:
     account_list.append(item.strip('\n'))

if len(account_list) > 0:
	with open('_FetchProfile.csv','w', newline='') as f:
		writer = csv.writer(f, delimiter='|')
		writer.writerow(['ScreenName','Name','UserID','c_follower','status','url','friend_count','description','twitter_age','avg_tweets'])
		for target in account_list:
			item = auth_api.get_user(target)
			tweets = item.statuses_count
			account_created_date = item.created_at
			delta = datetime.utcnow() - account_created_date
			account_age_days = delta.days
			Average_tweets_per_day = float(tweets)/float(account_age_days)
			writer.writerow([item.screen_name, item.name, item.id, item.followers_count, item.statuses_count, item.url, item.friends_count, item.description,account_age_days,Average_tweets_per_day ])

                                                    
