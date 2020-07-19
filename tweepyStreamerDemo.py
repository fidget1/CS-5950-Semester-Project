# ========================================================================================
# File:         tweepyStreamerDemo.py
# 
# Description:  A demo python script that demonstrates how to use Tweepy to stream
#               Tweets that pass a filter for keywords. It prints incoming tweets to
#               stdout (console) and (optionally) writes them to a JSON file.
#
#               Code refers to the first two sections of this YouTube tutorial:
#               https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# ========================================================================================

import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Get Twitter API credentials from JSON (may need to consider an alternative method
# in production due to security).
with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    BEARER = data["bearer_token"]
    TOKEN = data["access_token"]
    ACC_SECRET = data["access_secret"]

# Handles Twitter API Authentication
class TwitterAuthenticater():
    def authenticate_twitter_app(self):
        # 0Auth2 authentication & set token
        auth = OAuthHandler(KEY, SECRET)
        auth.set_access_token(TOKEN, ACC_SECRET)

        return auth

# Handles the streaming and processing of live tweets
class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticater()

    # Streams incoming Tweets through a Tweepy Stream object.
    #
    # IN:
    #   fetched_tweets_filename: JSON file to write the incoming tweets to.
    #   write_to_file: True/False; if true, write to the name file.
    def stream_tweets(self, fetched_tweets_filename, filter_list, write_to_file):
        listener = TwitterListener(fetched_tweets_filename, write_to_file)

        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        
        # Apply filter
        stream.filter(track=filter_list)

# A basic listener that merely prints received tweets to stdout and writes them to a
# given JSON file.
class TwitterListener(StreamListener):
    # Constructor
    #
    # IN:
    #   fetched_tweets_filename: JSON file to write the incoming tweets to.
    #   write_to_file: True/False; if true, write to the name file.
    def __init__(self, fetched_tweets_filename, write_to_file):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.write_to_file = write_to_file

    # Executes upon receiving a Tweet from the streamer.
    #
    # IN:
    #   data: the incoming data from Tweepy (given in JSON format)
    def on_data(self, data):
        try:
            print(data)
            if self.write_to_file:
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(data)
            return True

        except BaseException as e:
            print("Error on data: %s" % str(e)) 
            return True

    # Executes upon receiving an error in processing data
    # 
    # IN:
    #   status: error code
    def on_error(self, status):
        # Exits the connection immediately if stream usage exceeds Twitter API stream rate limit.
        if status == 420:
            print("Exceeded rate limit: %d. Killing connection..." % status)
            return False
        print(status)

# Main (note: in a real use-case, the filter_list will be determined by the user)
if __name__ == "__main__":
    filter_list = ["cats", "dogs"]
    fetched_tweets_filename = "myTweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, filter_list, False)
    