__author__ = 'dleigh'

from flask import Flask, request
from Player import Player
#from PlayerListener import PlayerListener
from DealerRunner import DealerRunner
import json, time, os, logging, logging.config
#import etcd

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("dealerService")

BlackjackDealerService = Flask(__name__)

playerListener = None
dealerRunner = DealerRunner()

# @BlackjackDealerService.route("/unregisterWithEtcd")
# def unregisterWithEtcdPOST():
#     jsonData = request.json
#     etcd_endpoint = jsonData['etcdEndpoint']
#     dealer_uuid = jsonData['dealerUUID']
#     return unregisterWithEtcd(etcd_endpoint,dealer_uuid)
#
# def unregisterWithEtcd(etcd_endpoint,dealer_uuid):
#     assert etcd_endpoint is not None and dealer_uuid is not None
#
#     # assumpe ipv4 endpoint
#     client = etcd.Client(host=etcd_endpoint.split(':')[0], port=int(etcd_endpoint.split(':')[1]))
#
#     try:
#         # remove self from service discovery
#         client.delete('/dealers/%s' % dealer_uuid)
#         logging.info('Unregistered dealer uuid %s' % dealer_uuid)
#     except:
#         # TODO: pass for now until we figure out why this is happening twice
#         pass
#
# @BlackjackDealerService.route("/registerWithEtcd")
# def registerWithEtcdPOST():
#     jsonData = request.json
#     etcd_endpoint = jsonData['etcdEndpoint']
#     dealer_uuid = jsonData['dealerUUID']
#     dealer_endpoint = jsonData['dealerEndpoint']
#     return registerWithEtcd(etcd_endpoint, dealer_uuid, dealer_endpoint)
#
# def registerWithEtcd(etcd_endpoint, dealer_uuid, dealer_endpoint):
#     assert etcd_endpoint is not None and dealer_uuid is not None and dealer_endpoint is not None
#
#     # assumpe ipv4 endpoint
#     client = etcd.Client(host=etcd_endpoint.split(':')[0], port=int(etcd_endpoint.split(':')[1]))
#
#     # expose self to service discovery
#     client.write(
#         '/dealers/%s' % dealer_uuid,
#         json.dumps(
#             {
#                 'endpoint': dealer_endpoint
#             }
#         )
#     )

# def listenForPlayers(endpoint, runner):
#     playerListener = PlayerListener(endpoint, runner)
#     playerListener.start()

@BlackjackDealerService.route("/")
def hello():
    result = "Hello World!"
    return result

@BlackjackDealerService.route("/players", methods=['POST','GET','DELETE'])
def playersRequest():
    if request.method == 'POST':
        jsonData = request.json
        playerURL = jsonData['playerURL']

        if dealerRunner.playerExistsAndActive(playerURL):
            return "error: player %s already exists and is active" % playerURL, 409

        dealerRunner.addPlayer(playerURL, Player())
        dealerRunner.startPlayer(playerURL)
        return "ok"
    elif request.method == 'GET':
        stats = dealerRunner.getScores()
        return json.dumps(stats)
    elif request.method == 'DELETE':
        jsonData = request.json
        playerURL = jsonData['playerURL']
        return dealerRunner.stopPlayer(playerURL)

@BlackjackDealerService.route("/deleteAll")
def deleteAll():
    dealerRunner.removeAllPlayers()
    return "ok"

@BlackjackDealerService.route("/stopAll")
def stopAll():
    dealerRunner.stopAllPlayers()
    return "ok"

@BlackjackDealerService.route("/getPlayersNextCard", methods=['GET'])
def cheat():
    jsonData = request.json
    playerURL = jsonData['playerURL']
    nextCard = dealerRunner.getNextCard(playerURL)
    result = {"cardIndex": nextCard.getIndex()}
    return json.dumps(result)

# Etcd Player Discovery
# endpoint = os.environ.get('ETCD_ENDPOINT')
# assert endpoint is not None
# listenForPlayers(endpoint, dealerRunner)

if __name__ == "__main__":
    # etcd_endpoint = os.environ.get('ETCD_ENDPOINT')
    # dealer_uuid = os.environ.get('DEALER_UUID')
    # dealer_endpoint = os.environ.get('DEALER_ENDPOINT')
    #registerWithEtcd()

    BlackjackDealerService.run(debug=True, use_reloader=False, host='0.0.0.0')

    # unregisterWithEtcd()
