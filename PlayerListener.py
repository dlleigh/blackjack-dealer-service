import json
import threading
import etcd
from Player import Player
import requests

class PlayerListener(threading.Thread):
    def __init__(self, endpoint, runner):
        threading.Thread.__init__(self)
        self.daemon = True
        self.cancelled = False
        self.client = etcd.Client(host=endpoint.split(':')[0], port=int(endpoint.split(':')[1]))
        self.runner = runner

    def run(self):
        while not self.cancelled:
            try:
                players_change = self.client.read('/players', recursive=True, wait=True, timeout=30)
                if players_change.action == 'set':
                    print('New player registration discovered')
                    playerURL = json.loads(players_change.value)['endpoint']
                    player = Player()
                    self.runner.addPlayer(playerURL, player)
                    self.runner.startPlayer(playerURL)
                elif players_change.action == 'delete':
                    playerURL = json.loads(players_change._prev_node.value)['endpoint']
                    self.runner.stopPlayer(playerURL)
            except etcd.EtcdException:
                pass

    def cancel(self):
        """End this timer thread"""
        self.cancelled = True
