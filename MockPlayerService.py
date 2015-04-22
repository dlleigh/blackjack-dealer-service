__author__ = 'dleigh'

from flask import Flask, request
from Queue import Queue
import json, time
from Card import Card

MockPlayerService = Flask(__name__)

players = {}
q = Queue()

@MockPlayerService.route("/")
def hello():
    result = "Hello World!"
    return result

@MockPlayerService.route("/stand/<username>", methods=['POST','GET'])
def stand(username):
    for cardIndex in request.json['playersHand']:
        print("card received: %s of %s" % (Card(cardIndex).getRank(),Card(cardIndex).getSuit()))
    jsonData = {"action": "stand"}
    return json.dumps(jsonData)

@MockPlayerService.route("/hit/<username>", methods=['POST','GET'])
def hit(username):
    for cardIndex in request.json['playersHand']:
        print("card received: %s of %s" % (Card(cardIndex).getRank(),Card(cardIndex).getSuit()))
    # for card in request.json:
    #     print(card.getValue())
    #print (json.dumps(request.json))
    jsonData = {"action": "hit"}
    return json.dumps(jsonData)

if __name__ == "__main__":
    MockPlayerService.run(debug=True,port=5001)
