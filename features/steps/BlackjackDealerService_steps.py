__author__ = 'dleigh'

from behave import *
import json
import time
import BlackjackDealerService
from Player import Player
from Dealer import Dealer
from Card import Card
from mock import patch

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
    BlackjackDealerService.addPlayer(playerURL, context.player)
    context.player.dealer = Dealer(playerURL, BlackjackDealerService.q)
    context.dealer = context.player.dealer

@given('the player has a king and a 5')
def step_impl(context):
    context.dealer.playersHand = [Card(4),Card(12)]
    context.dealer.dealersHand = [Card(12),Card(12)]

@then('the player will go bust')
def step_impl(context):
    context.dealer.playHand()
    context.page = context.client.get('/players')  # do a GET /players to force BlackjackDealerService to drain the queue and update player obj
    assert context.page.status_code == 200
    assert context.player.stats['lose'] == 1

@given('"{count}" player services with URL like "{url}"')
def step_impl(context,count,url):
    for i in range(1,int(count)):
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
    assert i == 20

@then('all players will have hands scored')
def step_impl(context):
    for key, value in context.playersData.iteritems():
        assert value['win'] + value['lose'] + value['tie'] != 0

@then('remove all players')
def step_impl(context):
    context.page = context.client.get('/deleteAll')
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
    context.page = context.client.get('/getPlayersNextCard', data=json.dumps({'playerURL':url}), content_type='application/json')
    assert context.page.status_code == 200
    jsonData = json.loads(context.page.data)
    context.nextCardIndex = jsonData['cardIndex']

@then('the next card will match what is expected')
def step_impl(context):
     context.dealer.playHand()
     for card in context.dealer.playersHand:
         assert card.getIndex() in [4,12,context.nextCardIndex]

@given('the player has a 2 and a 5')
def step_impl(context):
    context.dealer.playersHand = [Card(3),Card(4)]
    context.dealer.dealersHand = [Card(12),Card(12)]