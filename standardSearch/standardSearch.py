'''
Using venv and running app with evironment variable exports and flask command. See below.
https://flask.palletsprojects.com/en/1.1.x/installation/
https://flask.palletsprojects.com/en/1.1.x/quickstart/

Project Setup
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
$ . venv/bin/activate

Flask installation (in venv)
$ pip install Flask

Check version (in venv)
$ flask --version
Should be Python 3.8.2, Flask 1.1.2, Werkzeug 1.0.1

If using a development environment (debugging, reloading, etc.):
$ export FLASK_ENV=development

Running the app
$ export FLASK_APP=hello.py
$ flask run

Install tweepy
pip install tweepy

Resource url: https://api.twitter.com/1.1/search/tweets.json
'''
from flask import Flask, render_template, request, json
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

@app.route('/')
def index():
    try:
        auth = tweepy.OAuthHandler(KEY, SECRET)
        auth.set_access_token(ACC_TOKEN, ACC_SECRET)
        auth.secure = True
        api = tweepy.API(auth)
        search = request.args.get("q")
        # API.search(q[, lang][, locale][, rpp][, page][, since_id][, geocode][, show_user])
        pprint.pprint('search: ' + search)
        public_tweets = api.search(search, lang='en')
        pprint.pprint('public_tweets:')
        pprint.pprint(public_tweets)
        return render_template('home.html', tweets=public_tweets)
    except tweepy.TweepError as e:
        # These errors were caught because I was using the user_timeline API instead of api.search
        # Keeping them just in case
        if (e.args[0] == "Not authorized."):
            pprint.pprint(e.args[0])
            return render_template('home.html')
        # Sorry, that page does not exist.
        elif (e.args[0][0] and e.args[0][0]["code"] == 34):
            pprint.pprint('34:' + e.args[0][0]["message"])
            return render_template('home.html')
        else:
            pprint.pprint(e.args[0])
            return render_template('home.html') 