__author__ = 'dleigh'


import requests, json, time
import requests.exceptions
import threading
from Card import Card

class Dealer(threading.Thread):
    def __init__(self, playerURL, q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.cancelled = False
        self.playerURL = playerURL
        self.playersHand = []
        self.dealersHand = []
        self.q = q

    def run(self):
        while not self.cancelled:
            self.playersHand = [Card.getRandomCard(),Card.getRandomCard()]
            self.dealersHand = [Card.getRandomCard()]
            self.playHand()
            time.sleep(1)

    def playHand(self):
        self.playerDraw()
        self.dealerDraw()
        result = self.getHandResult()
        self.q.put({'playerURL': self.playerURL, 'result': result})

    def getHandResult(self):
        if (self.getMaxHandValue(self.playersHand) == 0 ):  # player is busted
            return "lose"
        elif (self.getMaxHandValue(self.dealersHand) == 0 ):  # dealer is busted
            return "win"
        elif (self.getMaxHandValue(self.playersHand) > self.getMaxHandValue(self.dealersHand)): # player wins
            return "win"
        elif (self.getMaxHandValue(self.playersHand) < self.getMaxHandValue(self.dealersHand)): # player loses
            return "lose"
        else:
            return "tie"

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

    def getMinHandValue(self,hand):
        values = self.getHandValues(hand)
        minValue = values[0]
        for value in values:
            if value < minValue:
                minValue = value
        return minValue

    def dealerDraw(self):
        while self.getMaxHandValue(self.dealersHand) <= 16 and self.getMinHandValue(self.dealersHand) <= 21:
           self.dealersHand.append(Card.getRandomCard())
        return self.getMaxHandValue(self.dealersHand)

    def playerDraw(self):
        playerStand = False
        playerAbort = False
        while self.getMinHandValue(self.playersHand) <= 21 and playerStand is False and playerAbort is False:
            print ("player hand value is %s" % self.getMaxHandValue(self.playersHand))
            handData = {'playersHand': [c.getIndex() for c in self.playersHand],
                        'dealersHand': [c.getIndex() for c in self.dealersHand]}
            print("handData: %s" % handData)
            try:
                r = requests.get(self.playerURL,
                                  data=json.dumps(handData),
                                  headers={'Content-type': 'application/json'},
                                  timeout=0.5)
                action = r.json()['action']
                if action == 'hit':
                    print ("player hits")
                    self.playersHand.append(Card.getRandomCard())
                else:
                    print ("player stands")
                    playerStand = True
            except requests.exceptions.Timeout:
                print "Player loses due to timeout"
                playerAbort = True
                self.playersHand = []
            except requests.exceptions.RequestException as e:
                print "Player loses due to RequestException %s" % e
                playerAbort = True
                self.playersHand = []
            print ("player hand value is now %s" % self.getMaxHandValue(self.playersHand))

    def cancel(self):
        """End this timer thread"""
        self.cancelled = True