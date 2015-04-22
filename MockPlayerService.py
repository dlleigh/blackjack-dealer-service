__author__ = 'dleigh'

from flask import Flask, request
from Queue import Queue
import json, time, os, etcd
from Card import Card

MockPlayerService = Flask(__name__)

players = {}
q = Queue()

def registerWithEtcd(playerURL):
    etcd_endpoint = os.environ.get('ETCD_ENDPOINT')
    player_uuid = os.environ.get('PLAYER_UUID')

    assert etcd_endpoint is not None and player_uuid is not None

    # assumpe ipv4 endpoint
    client = etcd.Client(host=etcd_endpoint.split(':')[0], port=int(etcd_endpoint.split(':')[1]))

    # expose self to service discovery
    client.write(
        '/players/%s' % player_uuid,
        json.dumps(
            {
                'endpoint': playerURL
            }
        )
    )

def unregisterWithEtcd():
    etcd_endpoint = os.environ.get('ETCD_ENDPOINT')
    player_uuid = os.environ.get('PLAYER_UUID')

    assert etcd_endpoint is not None and player_uuid is not None

    # assumpe ipv4 endpoint
    client = etcd.Client(host=etcd_endpoint.split(':')[0], port=int(etcd_endpoint.split(':')[1]))

    try:
        # remove self from service discovery
        client.delete('/players/%s' % player_uuid)
    except:
        # TODO: pass for now until we figure out why this is happening twice
        pass

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

    jsonData = {"action": "hit"}
    return json.dumps(jsonData)

@MockPlayerService.route("/broken/<username>", methods=['POST','GET'])
def broken(username):
    for cardIndex in request.json['playersHand']:
        print("card received: %s of %s" % (Card(cardIndex).getRank(),Card(cardIndex).getSuit()))

    jsonData = {"action": "hit"}
    time.sleep(10)
    return json.dumps(jsonData)

if __name__ == "__main__":
    MockPlayerService.run(debug=True, use_reloader=False, port=5002)
