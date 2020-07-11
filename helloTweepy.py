import tweepy
import json
with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    BEARER = data["bearer_token"]
    TOKEN = data["access_token"]
    ACC_SECRET = data["access_secret"]


auth = tweepy.OAuthHandler(KEY, SECRET)
auth.set_access_token(TOKEN, ACC_SECRET)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
