import time
from flask import Flask, request, json, g
import tweepy
import sqlite3
import db
# from xml.etree import ElementTree
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    ACC_TOKEN = data["access_token"]
    ACC_SECRET = data["access_secret"]

app = Flask(__name__)


@app.route('/api')
def api():
    db.open_db()
    print("db creation completed")
    auth = tweepy.OAuthHandler(KEY, SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_SECRET)
    tweepy_api = tweepy.API(auth)
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=tweepy_api.auth, listener=my_stream_listener)
    my_stream.filter(track=['Obama'])
    # for testing, when return is False for stream lister, on data
    return "hello"


class MyStreamListener(tweepy.StreamListener):
    # this.cur =
    def on_data(self, status):
        con = db.open_db()
        # print(status)
        tweet = json.loads(status)
        # only return non-retweeted tweets
        if tweet["retweeted"]:
            return True
        # get data
        user = tweet["user"]["screen_name"]
        text = tweet["text"]
        retweeted = tweet["retweeted"]

        # get sentiment analysis
        client = language.LanguageServiceClient()
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT
        )
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        print('Text: {}'.format(text))
        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

        try:
            con.cursor().execute("INSERT into tweets (user, text, retweeted, score, magnitude) values (?,?,?,?,?)", (user, text, retweeted, sentiment.score, sentiment.magnitude))
            con.commit()
            print("Successful insert")
        except IOError as e:
            con.rollback()
            print("Insert failed: " + str(e))


        # Testing
        # return False
        return True

    def on_error(self, status):
        print(status)
        if status == 88:
            print("tweepError rate limited?: ")
        elif status == 401:
            print("bad auth: " + str(status))
        elif status == 403:
            print("forbidden: " + str(status))
        elif status == 404:
            print("not found: " + str(status))
        elif status == 420:
            print("rate limited: " + str(status))
            # backoff handled by Tweepy API
            return True
        elif status == 429:
            print("too many requests: " + str(status))
        elif status == 500:
            print("internal server error: " + str(status))
        elif status == 502:
            print("bad gateway: " + str(status))
        elif status == 503:
            print("service unavailable: " + str(status))
        elif status == 504:
            print("gateway timeoff: " + str(status))

        return False
