__author__ = "Priagung Khusumanegara"
__copyright__ = "Copyright 2018, Twitter Crawler"
__credits__ = ["Twitter API"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Prigung Khusumanegara"
__email__ = "priagung.123@gmail.com"
__status__ = "Development"

import tweepy 
import csv

#Twitter API credentials
consumer_key = "<consumer_key>"
consumer_secret = "<consumer secret>"
access_token = "<access token>"
access_token_secret = "<access token secret>"

#read list of targeted account
with open('list.txt', 'r') as targets_file:
     targets_list = targets_file.readlines()

#initialize a list to hold all targeted account     
usernames = []

for item in targets_list:
     usernames.append(item.strip('\n'))

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with  this method
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []  

    #make initial request for most recent tweets (200 is the maximum   allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.coordinates , tweet.source, tweet.entities , tweet.user.location, tweet.retweet_count, tweet.user.lang,  tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(['id','cor','source','entities','location','retweet','lang','created_at','text'])
        writer.writerows(outtweets)

    pass

if __name__ == '__main__':
    #pass in the username of the account you want to download
    for x in usernames:
        get_all_tweets(x)
        
