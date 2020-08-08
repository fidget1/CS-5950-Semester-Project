# File:         testdata.py
# Author:       Jeremy Evans
#
# Description:  Returns a JSON representation of test data (100 random numbers) 
#               to the caller (in this case, the caller is the React front end).
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

    def handle_counter(self):
        # Increment counter
        self.counter += 1
        if self.counter < 6:
            self.processing = True
        else:
            self.counter = 0
            self.processing = False

    # Returns 100 random values in JSON.
    def generate_numbers(self):
        self.handle_counter()

        # Simulate wait
        print("Procesing...")
        time.sleep(1)
        print("Doing job %d..." % (self.counter))

        numbers = dict()
        seed()
        for i in range(100):
            value = random()
            numbers.update({i : value})
        
        data = {
            "Name" : "Test-data",
            "processing" : self.processing,
            "numbers" : numbers
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
    return app_class.generate_numbers()

