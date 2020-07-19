# ========================================================================================
# File:         tweepyStreamerDemo.py
# 
# Description:  A demo python script that demonstrates how to use Tweepy to retrieve the
#               most recent n tweets from a given user (n is a positive integer).
#
#               Code refers to the first two sections of this YouTube tutorial:
#               https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# ========================================================================================

import json
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler

# Get Twitter API credentials from JSON (may need to consider an alternative method
# in production due to security).
with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    BEARER = data["bearer_token"]
    TOKEN = data["access_token"]
    ACC_SECRET = data["access_secret"]

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticater().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

# Handles Twitter API Authentication
class TwitterAuthenticater():
    def authenticate_twitter_app(self):
        # 0Auth2 authentication & set token
        auth = OAuthHandler(KEY, SECRET)
        auth.set_access_token(TOKEN, ACC_SECRET)

        return auth

# Main (note: in a real use-case, the Twitter will be determined by the app user)
if __name__ == "__main__":
    twitter_client = TwitterClient(twitter_user='pycon') # Hardcoded: @[twitter_user]
    print(twitter_client.get_user_timeline_tweets(num_tweets=1))