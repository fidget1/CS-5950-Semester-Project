# File:         testdata.py
# Author:       Jeremy Evans
#
# Description:  Returns a JSON representation of test data representing
#               metrics returned from the GCP Natural Language API
#               sentiment analysis.
#
#               JSON data takes is of the following form (returned by)
#               analyzeSentiment):
#               {
#                   "documentSentiment": {
#                       "score": 0.2,
#                       "magnitude": 3.6
#                   },
#                   "language": "en",
#                   "sentences": [
#                   {
#                       "text": {
#                           ...,
#                           "beginOffset": 0
#                       },
#                       "sentiment": {
#                           "magnitude": 0.8,
#                           "score": 0.8
#                       }
#                   },
#                   ...
#               }
#
#               [documentSentiment] contains the overall sentiment of the
#               document, which contains the following:
#
#                   [score]: float range = [-1.0, 1.0], overall emotional
#                   leaning of the text.
#
#                   [magnitude]: float range = [0.0, +inf], overall strength
#                   of emotion in the text.
#
#               [language]: document language, either passed in the initial
#               request or automatically detected if absent.
#
#               [Sentences]: list of sentences extracted from the original
#               document, which contains:
#
#                   [sentiment] sentence-level sentiment for each sentence,
#                   which contain [score] and [magnitude] values as described
#                   above.
#
#               The frontend will use the values in [documentSentiment] and
#               [text] (concatenated).
#
# Use:          In flask-test/, enter the following:
#               $ export FLASK_APP=<your-python3-script>.py
#               $ flask run
# =============================================================================

from flask import Flask, json
from flask_cors import CORS

# import json
from random import seed, random

# import time to simulate time delay
import time

# =============================================================================
# Test class
# =============================================================================

class TestHandler:
    def __init__(self):
        self.counter = 0
        self.processing = False

    # Increment counter until it reaches a certain point
    def handle_counter(self):
        self.counter += 1
        if self.counter < 6:
            self.processing = True
        else:
            self.counter = 0
            self.processing = False
    
    # Determines a sentiment based on a given score. Each sentiment is given a
    # number and defined as:
    #
    # Positive (4): score in [0.4, 1.0]
    #
    # Mixed (3): score in (-4.0, 4.0) & magnitude in (-inf, -3.0) OR (3.0, +inf)
    #
    # Neutral (2): score in (-4.0, 4.0) & magnitude in [-3.0, 3.0]
    # 
    # Negative(1):
    def determine_sentiment(self, score, magnitude):
        return 0

    # Returns dummy sentiment data
    def return_sentiment(self):
        self.handle_counter()

        # Simulate wait
        print("Procesing...")
        time.sleep(1)
        print("Doing job %d..." % (self.counter))

        # Dummy JSON data that would return from GCP [analyzeSentiment].
        # "processing" is a manual field, true until the entire job finishes.
        data = {
            "processing": self.processing,
            "documentSentiment": {
                "score": 0.2,
                "magnitude": 3.6
            },
            "language": "en",
            "sentences": [
            {
                "text": {
                    "content" : "Sample text.",
                    "beginOffset": 0
                },
                "sentiment": {
                    "magnitude": 0.8,
                    "score": 0.8
                }
            },
            {
                "text": {
                    "content" : "More text is not always better text.",
                    "beginOffset": 0
                },
                "sentiment": {
                    "magnitude": 0.8,
                    "score": 0.8
                }
            }]
        }

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

        return response

# =============================================================================
# Flask Test
# =============================================================================

app = Flask(__name__)
CORS(app)

app_class = TestHandler()

@app.route('/get_test_data')
def get_test_data():
    # TODO: extract filter from GET request

    # end TODO

    return app_class.return_sentiment()

