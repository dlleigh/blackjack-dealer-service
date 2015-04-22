from Queue import Queue
from Dealer import Dealer

class DealerRunner():
  def __init__(self):
    self.players = {}
    self.q = Queue()

  def flushQueue(self):
    while not self.q.empty():
      score = self.q.get()

      if self.players.get(score['playerURL']):
        print('Received score from queue for player that is no longer in players store')
        self.players[score['playerURL']].scoreResult(score['result'])

      self.q.task_done()

  def getScores(self):
    self.flushQueue()

    stats = {}

    for playerURL, player in self.players.iteritems():
      stats[playerURL] = player.getStats()
      stats[playerURL]['status'] = player.getStatus()

    return stats

  def getNextCard(self, playerURL):
    return self.players[playerURL].dealer.getNextCardCheat()

  def playerExistsAndActive(self, playerURL):
    player = self.players.get(playerURL)

    if player is not None and player.status == 'active':
      return True

    return False

  def addPlayer(self, playerURL, player):
    self.players[playerURL] = player

  def newDealer(self, playerURL):
    return Dealer(playerURL, self.q)

  def startPlayer(self, playerURL):
    dealer = self.newDealer(playerURL)
    self.players[playerURL].set_dealer(dealer)
    dealer.start()

  def stopPlayer(self, playerURL):
    self.players[playerURL].status = 'stopped'
    self.players[playerURL].dealer.cancel()

  def stopAllPlayers(self):
    for _, player in self.players.iteritems():
      player.status = 'stopped'
      player.dealer.cancel()

  def removeAllPlayers(self):
    self.flushQueue()
    self.stopAllPlayers()
    self.players = {}
