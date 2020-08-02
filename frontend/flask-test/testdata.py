# File:         testdata.py
# Author:       Jeremy Evans
#
# Description:  Returns a JSON representation of test data to the caller
#               (in this case, the caller is the React front end).
#
# Use:          In flask-test/, enter the following:
#               $ export FLASK_APP=<your-python3-script>.py
#               $ flask run
# =============================================================================

from flask import Flask, json
from flask_cors import CORS
# import json
from random import seed, random

app = Flask(__name__)
CORS(app)

@app.route('/get_test_data')

# Returns 100 random values in JSON.
def get_test_data():
    print("Received request..")
    numbers = dict()
    seed()
    for i in range(100):
        value = random()
        numbers.update({i : value})
    
    data = {
        "Name:" : "Test-data",
        "numbers" : numbers
    }

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
