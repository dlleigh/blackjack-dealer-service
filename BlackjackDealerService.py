__author__ = 'dleigh'

from flask import Flask, request
from Queue import Queue
from Dealer import Dealer
import json, time

BlackjackDealerService = Flask(__name__)

players = {}
q = Queue()

@BlackjackDealerService.route("/")
def hello():
    result = "Hello World!"
    return result

@BlackjackDealerService.route("/players", methods=['POST','GET','DELETE'])
def playersRequest():
    if request.method == 'POST':
        jsonData = request.json
        playerURL = jsonData['playerURL']
        players[playerURL] = {}
        players[playerURL]['stats'] = {}
        players[playerURL]['stats']['win'] = 0
        players[playerURL]['stats']['lose'] = 0
        players[playerURL]['stats']['tie'] = 0
        dealer = Dealer(playerURL, q)
        players[playerURL]['dealer'] = dealer
        players[playerURL]['status'] = 'active'
        dealer.start()
        return "ok"
    elif request.method == 'GET':
        while not q.empty():
            score = q.get()
            players[score['playerURL']]['stats'][score['result']] += 1
            q.task_done()
        stats = {}
        for playerURL in players:
            stats[playerURL] = players[playerURL]['stats']
            stats[playerURL]['status'] = players[playerURL]['status']
        return json.dumps(stats)
    elif request.method == 'DELETE':
        jsonData = request.json
        playerURL = jsonData['playerURL']
        players[playerURL]['status'] = 'stopped'
        players[playerURL]['dealer'].cancel()
        return "ok"

@BlackjackDealerService.route("/deleteAll")
def deleteAll():
    for playerURL in players:
        players[playerURL]['status'] = 'stopped'
        players[playerURL]['dealer'].cancel()
    return "ok"

if __name__ == "__main__":
    BlackjackDealerService.run(debug=True)
