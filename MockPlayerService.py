__author__ = 'dleigh'

from flask import Flask, request
from Queue import Queue
import json, time

MockPlayerService = Flask(__name__)

players = {}
q = Queue()

@MockPlayerService.route("/")
def hello():
    result = "Hello World!"
    return result

@MockPlayerService.route("/stand", methods=['POST'])
def stand():
    jsonData = {"action": "stand"}
    return json.dumps(jsonData)

if __name__ == "__main__":
    MockPlayerService.run(debug=True,port=5001)
