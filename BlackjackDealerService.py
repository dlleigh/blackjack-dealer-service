__author__ = 'dleigh'

from flask import Flask, request
from Queue import Queue
from Dealer import Dealer
from Player import Player
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
        if players.has_key(playerURL):
            if players[playerURL].getStatus() == 'active':
                return "error: player %s already exists and is active" % playerURL, 409
        addPlayer(playerURL, Player())
        dealer = Dealer(playerURL, q)
        players[playerURL].set_dealer(dealer)
        dealer.start()
        return "ok"
    elif request.method == 'GET':
        while not q.empty():
            score = q.get()
            players[score['playerURL']].scoreResult(score['result'])
            q.task_done()
        stats = {}
        for playerURL in players:
            stats[playerURL] = players[playerURL].getStats()
            stats[playerURL]['status'] = players[playerURL].getStatus()
        return json.dumps(stats)
    elif request.method == 'DELETE':
        jsonData = request.json
        playerURL = jsonData['playerURL']
        players[playerURL].status = 'stopped'
        players[playerURL].dealer.cancel()
        return "ok"

def addPlayer(playerURL, player):
    players[playerURL] = player

@BlackjackDealerService.route("/deleteAll")
def deleteAll():
    for playerURL in players:
        players[playerURL].status = 'stopped'
        players[playerURL].dealer.cancel()
    return "ok"

if __name__ == "__main__":
    BlackjackDealerService.run(debug=True)
