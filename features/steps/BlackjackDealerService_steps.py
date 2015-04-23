__author__ = 'dleigh'

from behave import *
import json, os, etcd
import requests, requests_mock
import time
import BlackjackDealerService
import MockPlayerService
from Player import Player
from Dealer import Dealer
from Card import Card
from mock import patch
from DealerRunner import DealerRunner

globalData = {}

@given('get the page')
def step_impl(context):
    context.page = context.client.get('/')
    assert context.page

@then('service will return hello')
def step_impl(context):
    assert "Hello" in context.page.data

@given('a player service URL "{url}" is provided via POST to /players')
def step_impl(context,url):
    data = {'playerURL': url}
    context.page = context.client.post('/players', data=json.dumps(data), content_type='application/json')
    assert context.page.status_code == 200

@then('another player service URL "{url}" provided via POST to /players will be rejected')
def step_impl(context,url):
    data = {'playerURL': url}
    context.page = context.client.post('/players', data=json.dumps(data), content_type='application/json')
    assert context.page.status_code == 409

@then('the player service URL "{url}" is active on GET /players')
def step_impl(context,url):
    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    assert jsonData[url]['status'] == 'active'

@then('player service is called with 2 player cards and 1 dealer card')
def step_impl(context):
    assert len(globalData['playersHand']) == 2
    assert len(globalData['dealersHand']) == 1

@then('dealer will finish and score the hand for player "{url}"')
def step_impl(context, url):
    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    assert jsonData[url]['win'] + jsonData[url]['lose'] + jsonData[url]['tie'] != 0

@given('wait "{sec}" seconds')
def step_impl(context,sec):
    time.sleep(float(sec))

@then('remove the player service url "{url}"')
def step_impl(context,url):
    data = {'playerURL': url}
    context.page = context.client.delete('/players', data=json.dumps(data), content_type='application/json')
    assert context.page.status_code == 200

@then('there are no active players')
def step_impl(context):
    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    for player in jsonData:
        assert jsonData[player]['status'] != 'active'

@given('a player service URL "{url}" is connected')
def step_impl(context,url):
    playerURL = url
    context.player = Player()
    runner = DealerRunner()
    runner.addPlayer(playerURL, context.player)
    context.runner = runner
    context.player.dealer = runner.newDealer(playerURL)
    context.dealer = context.player.dealer

@given('the player has a king and a 5')
def step_impl(context):
    context.dealer.playersHand = [Card(4),Card(12)]
    context.dealer.dealersHand = [Card(12),Card(12)]

@then('the player will go bust')
def step_impl(context):
    context.dealer.playHand()
    context.runner.getScores()
    assert context.player.stats['lose'] == 1

@given('"{count}" player services with URL like "{url}"')
def step_impl(context,count,url):
    for i in range(0,int(count)):
        data = {'playerURL': url + '/' + str(i)}
        context.page = context.client.post('/players', data=json.dumps(data), content_type='application/json')
        assert context.page.status_code == 200

@then('there will be "{count}" players connected')
def step_impl(context,count):
    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    context.playersData = jsonData
    i = 0
    for key, value in jsonData.iteritems():
        i+=1
    assert i == int(count)

@then('all players will have hands scored')
def step_impl(context):
    for key, value in context.playersData.iteritems():
        assert value['win'] + value['lose'] + value['tie'] != 0

@then('stop all players')
def step_impl(context):
    context.page = context.client.get('/stopAll')
    assert context.page.status_code == 200

@then('the player "{url}" should have lost some hands')
def step_impl(context,url):
    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    assert jsonData[url]['lose'] > 0
    assert jsonData[url]['win'] == 0
    assert jsonData[url]['tie'] == 0

@given('the dealer cheat url is called for player "{url}"')
def step_impl(context,url):
    nextCard = context.runner.getNextCard(url)
    context.nextCardIndex = nextCard.getIndex()

@then('the next card will match what is expected')
def step_impl(context):
     context.dealer.playHand()
     assert context.dealer.playersHand[2].getIndex() == context.nextCardIndex

@given('the player has a 2 and a 5')
def step_impl(context):
    context.dealer.playersHand = [Card(3),Card(4)]
    context.dealer.dealersHand = [Card(12),Card(12)]

@given('an etcd instance is available at {endpoint}')
def step_impl(context, endpoint):
    endpoint = os.environ.get(endpoint)
    assert endpoint != None

    context.etcd = etcd.Client(host=endpoint.split(':')[0], port=int(endpoint.split(':')[1]))
    try:
        context.etcd.machines
    except Exception as e:
        raise e

@given('dealer {uuid} is starting')
def step_impl(context, uuid):
    etcd_endpoint = os.environ.get('ETCD_ENDPOINT')
    dealer_uuid = os.environ.get('DEALER_UUID')
    dealer_endpoint = os.environ.get('DEALER_ENDPOINT')
    BlackjackDealerService.registerWithEtcd(etcd_endpoint, dealer_uuid, dealer_endpoint)

@given('dealer {uuid} is stopping')
def step_impl(context, uuid):
    etcd_endpoint = os.environ.get('ETCD_ENDPOINT')
    dealer_uuid = os.environ.get('DEALER_UUID')
    BlackjackDealerService.unregisterWithEtcd(etcd_endpoint,dealer_uuid)

@then('dealer {uuid} will expose itself to service discovery via {endpoint}')
def step_impl(context, uuid, endpoint):
    uuid = os.environ.get(uuid)
    endpoint = os.environ.get(endpoint)
    assert uuid != None
    assert endpoint != None

    dealer_record = context.etcd.read('/dealers/%s' % uuid).value
    assert json.loads(dealer_record) == {
        'endpoint': endpoint
    }

@then('dealer {uuid} will remove itself from service discovery')
def step_impl(context, uuid):
    uuid = os.environ.get(uuid)
    assert uuid != None

    exception = None
    try:
        context.etcd.get('/dealers/%s' % uuid).value
    except Exception as e:
        exception = e

    assert exception is not None

@given('player service {uuid} registers in etcd at {endpoint}')
def step_imp(context, uuid, endpoint):
    endpoint = endpoint.split('/', 1)
    playerAddress = os.environ.get(endpoint[0])
    MockPlayerService.registerWithEtcd('%s/%s' % (playerAddress, endpoint[1]))

@then('dealer {uuid} will finish and score the hand for player {endpoint}')
def step_imp(context, uuid, endpoint):
    endpoint = endpoint.split('/', 1)
    playerAddress = os.environ.get(endpoint[0])

    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    assert jsonData['%s/%s' % (playerAddress, endpoint[1])]['lose'] != 0

@given('player service {uuid} un-registers in etcd at {endpoint}')
def step_impl(context, uuid, endpoint):
    MockPlayerService.unregisterWithEtcd()

@then('dealer {uuid} will stop the hand for the player {endpoint}')
def step_impl(context, uuid, endpoint):
    endpoint = endpoint.split('/', 1)
    playerAddress = os.environ.get(endpoint[0])

    context.page = context.client.get('/players')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    assert jsonData['%s/%s' % (playerAddress, endpoint[1])]['status'] == 'stopped'
