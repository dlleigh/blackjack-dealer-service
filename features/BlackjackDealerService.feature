Feature: Test the Blackjack Dealer Service

    Scenario: startup
      Given get the page
        then service will return hello

    Scenario: add a player service
      Given a player service URL "http://localhost:5001/stand/one" is provided via POST to /players
        and wait "5" seconds
        then the player service URL "http://localhost:5001/stand/one" is active on GET /players
        and dealer will finish and score the hand for player "http://localhost:5001/stand/one"

      Scenario: add and remove a player service
      Given a player service URL "http://localhost:5001/stand/one" is provided via POST to /players
        and wait "2" seconds
        then the player service URL "http://localhost:5001/stand/one" is active on GET /players
        then remove the player service URL "http://localhost:5001/stand/one"
        then there are no active players

      Scenario: attempt to add the same player service twice
      Given a player service URL "http://localhost:5001/stand/one" is provided via POST to /players
        then another player service URL "http://localhost:5001/stand/one" provided via POST to /players will be rejected
        then remove the player service URL "http://localhost:5001/stand/one"
        then there are no active players

      Scenario: play a hand where player goes bust
        Given a player service URL "http://localhost:5001/hit/one" is connected
        and the player has a king and a 5
        then the player will go bust

      Scenario: start many player services
        Given "10" player services with URL like "http://localhost:5001/hit"
        and "10" player services with URL like "http://localhost:5001/stand"
        and wait "5" seconds
        then remove all players
        then there will be "20" players connected
        and all players will have hands scored
        then there are no active players

      Scenario: broken player loses
        Given a player service URL "http://localhost:5001/broken/one" is provided via POST to /players
        and wait "2" seconds
        then remove the player service URL "http://localhost:5001/broken/one"
        then the player "http://localhost:5001/broken/one" should have lost some hands

      Scenario: cheat service
        Given a player service URL "http://localhost:5001/hit/one" is connected
        and the player has a king and a 5
        and the dealer cheat url is called for player "http://localhost:5001/hit/one"
        then the next card will match what is expected