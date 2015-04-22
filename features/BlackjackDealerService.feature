Feature: Test the Blackjack Dealer Service

    Scenario: play a hand where player goes bust
      Given a player service URL "http://localhost:5002/hit/one" is connected
        and the player has a king and a 5
        then the player will go bust

    Scenario: cheat service
      Given a player service URL "http://localhost:5002/hit/one" is connected
        and the player has a king and a 5
        and the dealer cheat url is called for player "http://localhost:5002/hit/one"
        then the next card will match what is expected

    Scenario: add a player service
      Given a player service URL "http://localhost:5002/stand/one" is provided via POST to /players
        and wait "5" seconds
        then the player service URL "http://localhost:5002/stand/one" is active on GET /players
        and dealer will finish and score the hand for player "http://localhost:5002/stand/one"

    Scenario: add and remove a player service
      Given a player service URL "http://localhost:5002/stand/one" is provided via POST to /players
        and wait "2" seconds
        then the player service URL "http://localhost:5002/stand/one" is active on GET /players
        then remove the player service URL "http://localhost:5002/stand/one"
        then there are no active players

    Scenario: attempt to add the same player service twice
      Given a player service URL "http://localhost:5002/stand/one" is provided via POST to /players
        then another player service URL "http://localhost:5002/stand/one" provided via POST to /players will be rejected
        then remove the player service URL "http://localhost:5002/stand/one"
        then there are no active players

   Scenario: start many player services
      Given "10" player services with URL like "http://localhost:5002/hit"
        and "10" player services with URL like "http://localhost:5002/stand"
        and wait "5" seconds
        then stop all players
        then there will be "20" players connected
        then all players will have hands scored
        then there are no active players

@etcd
    Scenario: starting
     Given an etcd instance is available at ETCD_ENDPOINT
       and dealer DEALER_UUID is starting
       then dealer DEALER_UUID will expose itself to service discovery via DEALER_ENDPOINT

@etcd
    Scenario: stopping
     Given an etcd instance is available at ETCD_ENDPOINT
       and dealer DEALER_UUID is stopping
       then dealer DEALER_UUID will remove itself from service discovery

@etcd
    Scenario: discover a player service
     Given an etcd instance is available at ETCD_ENDPOINT
       and player service PLAYER_UUID registers in etcd at PLAYER_ENDPOINT/hit/one
       and wait "5" seconds
       then dealer DEALER_UUID will finish and score the hand for player PLAYER_ENDPOINT/hit/one

@etcd
    Scenario: handle a player service un-registering
      Given an etcd instance is available at ETCD_ENDPOINT
        and player service PLAYER_UUID registers in etcd at PLAYER_ENDPOINT/hit/one
        and wait "2" seconds
        and player service PLAYER_UUID un-registers in etcd at PLAYER_ENDPOINT/hit/one
        and wait "1" seconds
        then dealer DEALER_UUID will stop the hand for the player PLAYER_ENDPOINT/hit/one

   Scenario: add a player service
     Given a player service URL "http://localhost:5002/stand/one" is provided via POST to /players
       and wait "5" seconds
       then the player service URL "http://localhost:5002/stand/one" is active on GET /players
       and dealer will finish and score the hand for player "http://localhost:5002/stand/one"

   Scenario: add and remove a player service
     Given a player service URL "http://localhost:5002/stand/one" is provided via POST to /players
       and wait "2" seconds
       then the player service URL "http://localhost:5002/stand/one" is active on GET /players
       then remove the player service URL "http://localhost:5002/stand/one"
       then there are no active players

    Scenario: broken player loses
      Given a player service URL "http://localhost:5002/broken/one" is provided via POST to /players
        and wait "2" seconds
        then remove the player service URL "http://localhost:5002/broken/one"
        then the player "http://localhost:5002/broken/one" should have lost some hands
