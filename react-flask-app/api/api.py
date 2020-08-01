import time
from flask import Flask, request, json
import tweepy
import pprint

with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    ACC_TOKEN = data["access_token"]
    ACC_SECRET = data["access_secret"]
    BEARER = data["bearer_token"]

app = Flask(__name__)


@app.route('/api')
def api():
    auth = tweepy.OAuthHandler(KEY, SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_SECRET)
    api = tweepy.API(auth)
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['Obama'])


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        user = all_data["user"]["screen_name"]
        print((user, tweet))
        return True
    
    def on_error(self, status):
        print(status)
