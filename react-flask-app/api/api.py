import time
from flask import Flask, request, json, g, jsonify, render_template
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
    q = request.args.get("q")
    con = db.connect_db()
    cur = con.cursor()
    cur.execute("SELECT MAX(id) FROM tweets")
    max_id = None
    for id in cur:
        max_id = id[0]
    print(max_id)
    auth = tweepy.OAuthHandler(KEY, SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_SECRET)
    tweepy_api = tweepy.API(auth)
    my_stream_listener = MyStreamListener(tweepy.StreamListener)
    my_stream_listener.init_class(con, q)
    my_stream = tweepy.Stream(auth=tweepy_api.auth, listener=my_stream_listener)
    try:
        p = multiprocessing.Process(target=my_stream.filter, name="filter", kwargs={"track": [q], "languages": ["en"]})
        p.start()
        time.sleep(5)
        p.terminate()
        p.join()
    except:
        print("Processing error: ")
    cur.execute("SELECT id, search_term, text, score, magnitude  FROM tweets WHERE id > ?", (max_id,))
    response_objects = []
    for (id, search_term, text, score, magnitude) in cur:
        response_objects.append(json.dumps({"id": id, "search_term": search_term, "text": text, "score": score, "magnitude": magnitude}))
    # for testing, when return is False for stream lister, on data
    # json_resp = {"data": response_objects}
    # resp = json.dumps(response_objects)
    # resp = json.loads(resp)
    return jsonify(response_objects)# render_template("home.html", resp=resp)


class MyStreamListener(tweepy.StreamListener):

    def init_class(self, con, query):
        self.count = 0
        self.con = con
        self.q = query

    def on_data(self, status):
        tweet = json.loads(status)
        text = tweet["text"]
        user = tweet["user"]["screen_name"]
        retweet = tweet["retweeted"]
        rt = "RT @"
        if rt in text:
            return True
        client = language.LanguageServiceClient()
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT
        )
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        try:
            self.con.cursor().execute("INSERT into tweets (search_term, user, text, score, magnitude, retweeted) values (?,?,?,?,?,?)", (self.q, user, text, sentiment.score, sentiment.magnitude, retweet))
            self.con.commit()
            self.count += 1
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
        else:
            print("other error: " + str(status))

        return False
