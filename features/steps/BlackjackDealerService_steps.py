__author__ = 'dleigh'

from behave import *
import json
import requests, requests_mock
import time

globalData = {}


def _always_stand_callback(request, context):
    context.status_code = 200
    data = json.loads(request.text)
    globalData['playersHand'] = data['playersHand']
    globalData['dealersHand'] = data['dealersHand']
    return {'action': 'stand'}

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
    # with requests_mock.mock() as m:
    #     m.post(url, json=_always_stand_callback)
    #     context.page = context.client.post('/players', data=json.dumps(data), content_type='application/json')
    assert context.page.status_code == 200

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