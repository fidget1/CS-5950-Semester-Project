import time
from flask import Flask, request, json, g
import tweepy
import sqlite3
import pprint

with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    ACC_TOKEN = data["access_token"]
    ACC_SECRET = data["access_secret"]

DATABASE = 'database.db'
# init_db()
# print("db initialized")
# cur = get_db().cursor()
# print("cursor created")


app = Flask(__name__)
# conn = sqlite3.connect('database.db')
# print("Opened database successfully")

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print("Table created successfully")
# conn.close()


@app.route('/api')
def api():
    auth = tweepy.OAuthHandler(KEY, SECRET)
    auth.set_access_token(ACC_TOKEN, ACC_SECRET)
    tweepy_api = tweepy.API(auth)
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=tweepy_api.auth, listener=my_stream_listener)
    my_stream.filter(track=['Obama'])
# for testing, when return is False for stream lister, on data
    return "hello"


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


class MyStreamListener(tweepy.StreamListener):

    def on_data(self, status):
        tweet = json.loads(status)
        # only return non-retweeted tweets
        if tweet["retweeted"]:
            return True
        # get data
        retweeted = tweet["retweeted"]
        text = tweet["text"]
        user = tweet["user"]["screen_name"]

        # get sentiment analysis
        # get db
        # insert into db


        '''
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO tweets (user,text,retweeted) VALUES(?,?,?)", (user, text, retweeted))
                con.commit()
                all_data = cur.fetchall()
                pprint.pprint(all_data)
                print('all_data' + str(all_data))
                print("Record successfully added")
        except:
            con.rollback()
            print("error in insert operation")

        finally:
            # return render_template("result.html", msg=msg)
            print("conn closing")
            con.close()
        '''
        # Testing
        return False
        # return True

    def on_error(self, status):
        print(status)
