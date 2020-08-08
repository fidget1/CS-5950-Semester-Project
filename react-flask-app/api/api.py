import time
from flask import Flask, request, json, g
import tweepy
import db
import multiprocessing
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
    con = db.connect_db()
    q = request.args.get("q")
    auth = tweepy.OAuthHandler(KEY, SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_SECRET)
    tweepy_api = tweepy.API(auth)
    my_stream_listener = MyStreamListener(tweepy.StreamListener)
    my_stream_listener.init_class(con, q)
    my_stream = tweepy.Stream(auth=tweepy_api.auth, listener=my_stream_listener)
    p = multiprocessing.Process(target=my_stream.filter, name="filter", kwargs={"track": [q], "languages": ["en"]})
    p.start()
    time.sleep(5)
    p.terminate()
    p.join()
    con.close()
    # for testing, when return is False for stream lister, on data
    return "hello"


class MyStreamListener(tweepy.StreamListener):

    def init_class(self, con, query):
        self.count = 0
        self.con = con
        self.q = query

    # def init_counter(self):
        # self.count = 0

    # def set_queue(self, query):
        # self.q = query

    def on_data(self, status):
        print(tweepy.StreamListener)
        tweet = json.loads(status)
        if tweet["retweeted"]:
            print(time.time() - self.start_time)
            return True
        user = tweet["user"]["screen_name"]
        text = tweet["text"]
        retweeted = tweet["retweeted"]
        print(text)
        client = language.LanguageServiceClient()
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT
        )
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        try:
            self.con.cursor().execute("INSERT into tweets (search_term, user, text, retweeted, score, magnitude) values (?,?,?,?,?,?)", (self.q, user, text, retweeted, sentiment.score, sentiment.magnitude))
            self.con.commit()
            self.count += 1
            print(self.count)
            if self.count > 100:
                self.con.close()
                return False
        except IOError as e:
            self.con.rollback()
            print("Insert failed: " + str(e))

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
