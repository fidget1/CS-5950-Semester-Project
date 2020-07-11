# https://developer.twitter.com/en/docs/labs/sampled-stream/quick-start
# MJA - This API will be deprecated in six months, but I'm assuming it's the one we should use for streaming. 

# Getting started with the sampled stream endpoint
# The sampled stream endpoint allows developers to stream, in real-time, roughly a 1% sample of all public Tweets. 
# Before you can start, you will need the following:

# An approved developer account
# A registered Twitter developer app
# Activating the “Sampled Stream” preview in the Labs dashboard
 

# Authentication
# This endpoint is authenticated using OAuth 2.0 Bearer token (also known as app-only authentication). This means you will need to generate a Bearer token, and pass this token in all of your requests. 

# You can use the Run in Postman button to download a collection that will handle the generation of a Bearer token for you. Other clients like curl and Insomnia will require you to generate a token manually.

# REST client
# REST applications such as Postman can be used for organizing, testing, and debugging HTTP requests.

# Run in Postman ❯ 
 
# Python 3RubyJavaScript (Node.js)Java
# To run this example, you will need to add your consumer key and secret to this example.

# To add your consumer key and secret:

# Navigate to your app dashboard.
# Select the app you've enabled with the Filtered stream preview, then click Details.
# Select the Keys and tokens tab.
# In the Consumer API keys section, copy the values for API key into consumer_key and API secret key into consumer_secret.
 
# Important: Never check consumer keys and secrets into source control. Learn how to secure your credentials.

import os
import requests
import json
from pprint import pprint
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
with open("keys.json") as json_keys:
    data = json.load(json_keys)
    KEY = data["api_key"]
    SECRET = data["api_secret_key"]
    BEARER = data["bearer_token"]

consumer_key = KEY # Add your API key here
consumer_secret = SECRET # Add your API secret key here

stream_url = "https://api.twitter.com/labs/1/tweets/stream/sample"

# Gets a bearer token
class BearerTokenAuth(AuthBase):
  def __init__(self, consumer_key, consumer_secret):
    self.bearer_token_url = "https://api.twitter.com/oauth2/token"
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.bearer_token = self.get_bearer_token()

  def get_bearer_token(self):
    response = requests.post(
      self.bearer_token_url, 
      auth=(self.consumer_key, self.consumer_secret),
      data={'grant_type': 'client_credentials'},
      headers={"User-Agent": "TwitterDevSampledStreamQuickStartPython"})

    if response.status_code is not 200:
      raise Exception(f"Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

    body = response.json()
    return body['access_token']

  def __call__(self, r):
    r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
    return r

def stream_connect(auth):
  response = requests.get(stream_url, auth=auth, headers={"User-Agent": "TwitterDevSampledStreamQuickStartPython"}, stream=True)
  for response_line in response.iter_lines():
    if response_line:
      pprint(json.loads(response_line))

bearer_token = BearerTokenAuth(consumer_key, consumer_secret)

# Listen to the stream. This reconnection logic will attempt to reconnect as soon as a disconnection is detected.
while True:
  stream_connect(bearer_token)
