__author__ = 'dleigh'

from random import randint

deck = [
        { 'suit': 'clubs', 'rank': 'Ace', 'value': [ 1, 11 ] },
        { 'suit': 'clubs', 'rank': '2', 'value': 2 },
        { 'suit': 'clubs', 'rank': '3', 'value': 3 },
        { 'suit': 'clubs', 'rank': '4', 'value': 4 },
        { 'suit': 'clubs', 'rank': '5', 'value': 5 },
        { 'suit': 'clubs', 'rank': '6', 'value': 6 },
        { 'suit': 'clubs', 'rank': '7', 'value': 7 },
        { 'suit': 'clubs', 'rank': '8', 'value': 8 },
        { 'suit': 'clubs', 'rank': '9', 'value': 9 },
        { 'suit': 'clubs', 'rank': '10', 'value': 10 },
        { 'suit': 'clubs', 'rank': 'Jack', 'value': 10 },
        { 'suit': 'clubs', 'rank': 'Queen', 'value': 10 },
        { 'suit': 'clubs', 'rank': 'King', 'value': 10 },

        { 'suit': 'diamonds', 'rank': 'Ace', 'value': [ 1, 11 ] },
        { 'suit': 'diamonds', 'rank': '2', 'value': 2 },
        { 'suit': 'diamonds', 'rank': '3', 'value': 3 },
        { 'suit': 'diamonds', 'rank': '4', 'value': 4 },
        { 'suit': 'diamonds', 'rank': '5', 'value': 5 },
        { 'suit': 'diamonds', 'rank': '6', 'value': 6 },
        { 'suit': 'diamonds', 'rank': '7', 'value': 7 },
        { 'suit': 'diamonds', 'rank': '8', 'value': 8 },
        { 'suit': 'diamonds', 'rank': '9', 'value': 9 },
        { 'suit': 'diamonds', 'rank': '10', 'value': 10 },
        { 'suit': 'diamonds', 'rank': 'Jack', 'value': 10 },
        { 'suit': 'diamonds', 'rank': 'Queen', 'value': 10 },
        { 'suit': 'diamonds', 'rank': 'King', 'value': 10 },

        { 'suit': 'hearts', 'rank': 'Ace', 'value': [ 1, 11 ] },
        { 'suit': 'hearts', 'rank': '2', 'value': 2 },
        { 'suit': 'hearts', 'rank': '3', 'value': 3 },
        { 'suit': 'hearts', 'rank': '4', 'value': 4 },
        { 'suit': 'hearts', 'rank': '5', 'value': 5 },
        { 'suit': 'hearts', 'rank': '6', 'value': 6 },
        { 'suit': 'hearts', 'rank': '7', 'value': 7 },
        { 'suit': 'hearts', 'rank': '8', 'value': 8 },
        { 'suit': 'hearts', 'rank': '9', 'value': 9 },
        { 'suit': 'hearts', 'rank': '10', 'value': 10 },
        { 'suit': 'hearts', 'rank': 'Jack', 'value': 10 },
        { 'suit': 'hearts', 'rank': 'Queen', 'value': 10 },
        { 'suit': 'hearts', 'rank': 'King', 'value': 10 },

        { 'suit': 'spades', 'rank': 'Ace', 'value': [ 1, 11 ] },
        { 'suit': 'spades', 'rank': '2', 'value': 2 },
        { 'suit': 'spades', 'rank': '3', 'value': 3 },
        { 'suit': 'spades', 'rank': '4', 'value': 4 },
        { 'suit': 'spades', 'rank': '5', 'value': 5 },
        { 'suit': 'spades', 'rank': '6', 'value': 6 },
        { 'suit': 'spades', 'rank': '7', 'value': 7 },
        { 'suit': 'spades', 'rank': '8', 'value': 8 },
        { 'suit': 'spades', 'rank': '9', 'value': 9 },
        { 'suit': 'spades', 'rank': '10', 'value': 10 },
        { 'suit': 'spades', 'rank': 'Jack', 'value': 10 },
        { 'suit': 'spades', 'rank': 'Queen', 'value': 10 },
        { 'suit': 'spades', 'rank': 'King', 'value': 10 }]

class Card:
    def __init__(self,cardNumber):
        self.cardNumber = cardNumber
        self.deck = deck


    def getSuit(self):
        return self.deck[self.cardNumber]['suit']

    def getRank(self):
        return self.deck[self.cardNumber]['rank']

    def getValue(self):
        return self.deck[self.cardNumber]['value']

    def getIndex(self):
        for i in range(0,len(deck)):
            if self.getSuit() == deck[i]['suit'] and self.getRank() == deck[i]['rank']:
                return i

    def getDescription(self):
        return self.deck[self.cardNumber]['rank'] + ' of ' + self.deck[self.cardNumber]['suit']

    @classmethod
    def getRandomCard(self):
        return Card(randint(0, 51))