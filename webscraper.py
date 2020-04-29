#!/usr/bin/python3
import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import json

consumer_key = "slYfexdRTOOJFZCe2BIQiMzA1"
consumer_secret = "NiBNPHghHJkLC3cWYW9EsHQBGDV7QW3GP9QkFJMjG0f88eukaa"
access_token = "477340723-CFpJTYUBmFlxD0YPsbrsCqvGHwOvnGcOD4uuTeXO"
access_secret = "bSAGNnLlGynJFnFQG9BNg8mNsd2B89MrmDDoTk5dMtTIl"

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user, exclude_replies=True).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
	
    def get_hastag(self, num_tweets):
        hashtag = []
        for tweet in Cursor(self.twitter_client.search, q="#science", lang="en", since="2020-04-16").items(num_tweets):
            #print(tweet.text)
            hashtag.append(tweet)
        return hashtag

# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)

# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data) # Prints to console
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)], columns=['tweets'])
        df['id_str'] = np.array([tweet.id_str for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)])
        df['len'] = np.array([len(tweet.text) for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)])
        df['date'] = np.array([tweet.created_at for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)])
        df['source'] = np.array([tweet.source for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets if (not tweet.retweeted) and ('RT @' not in tweet.text)])
        
        return df

if __name__ == '__main__':

    handle = 'ChriSpringstead'
    num_tweets = 1000

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()
    user = api.get_user(handle)
	
    #friends = twitter_client.get_friend_list(len(user.friends))
    #print(friends)

    #tweets = api.user_timeline(screen_name=handle, count=num_tweets) # Enter twitter handle to target specific user
    tweets = twitter_client.get_hastag(num_tweets)
    
	#print(dir(tweets[0]))
    #print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['label'] = 4

    # Outputting data frame
    print("printing to file")
    out_filename = "#science.csv"
    df.to_csv(out_filename, encoding='utf-8', index=False) # Commented just to make testing faster, undo later

    # # Get average length over all tweets:
    # print("Mean tweet length: " + str(np.mean(df['len'])))

    # # Get the number of likes for the most liked tweet:
    # print("Most likes: " + str(np.max(df['likes'])))

    # # Get the number of retweets for the most retweeted tweet:
    # print("Most RTs: " + str(np.max(df['retweets'])))

    # print(df.head(10))

    # Time Series

    '''
    # Tweet Length
    plt.figure(1)
    time_len = pd.Series(data=df['len'].values, index=df['date'])
    time_len.plot(figsize=(16, 4), color='r')
    plt.show()
​
    # Num Likes
    plt.figure(2)
    time_favs = pd.Series(data=df['likes'].values, index=df['date'])
    time_favs.plot(figsize=(16, 4), color='r')
    plt.show()
​
    # Num RTs
    plt.figure(3)
    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16, 4), color='r')
    plt.show()
    '''

    # Layered Time Series:
    # plt.figure(4)
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    # plt.show()