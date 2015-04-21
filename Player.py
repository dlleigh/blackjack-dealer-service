__author__ = 'dleigh'

class Player:
    def __init__(self):
        self.stats = {
            'win': 0,
            'lose': 0,
            'tie': 0
        }
        self.status = 'active'

    def set_dealer(self, dealer):
        self.dealer = dealer

    def scoreResult(self, result):
        self.stats[result]+=1

    def getStats(self):
        return self.stats

    def getStatus(self):
        return self.status
