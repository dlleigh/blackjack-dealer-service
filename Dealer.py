__author__ = 'dleigh'


import requests, json, time
import threading
from Card import Card

class Dealer(threading.Thread):
    def __init__(self, playerURL, q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.cancelled = False
        self.playerURL = playerURL
        self.playersHand = {}
        self.dealersHand = {}
        self.q = q

    def run(self):
        while not self.cancelled:
            print "looping"
            r = requests.post(self.playerURL, data=json.dumps({'playersHand': [1, 2], 'dealersHand': [1]}),
                              headers={'content_type': 'application/json'})
            action = r.json()['action']
            if action == 'stand':
                self.q.put({'playerURL': self.playerURL, 'result': 'tie'})
            time.sleep(1)

    def getHandValues(self,hand):
        numAces = 0
        values = []
        value = 0
        for card in hand:
            if card.getRank() == 'Ace':
                numAces += 1
                value += 1
            else:
                value += card.getValue()
        values.append(value)
        for i in range(0,numAces):
            values.append(value + 10*(i+1))
        return values

    def getMaxHandValue(self,hand):
        values = self.getHandValues(hand)
        maxValue = 0
        for value in values:
            if value <= 21:
                if value > maxValue:
                    maxValue = value
        return maxValue

    def dealerDraw(self):
        while self.getMaxHandValue(self.dealersHand) <= 16 and self.getMinHandValue(self.dealersHand) <= 21:
           self.dealersHand.append(Card.getRandomCard())
        return self.getMaxHandValue(self.dealersHand)

    def cancel(self):
        """End this timer thread"""
        self.cancelled = True