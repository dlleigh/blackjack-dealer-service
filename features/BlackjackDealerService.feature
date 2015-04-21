Feature: Test the Blackjack Dealer Service

    Scenario: startup
      Given get the page
        then service will return hello

    Scenario: add a player service
      Given a player service URL "http://localhost:5001/stand" is provided via POST to /players
        and wait "5" seconds
        then the player service URL "http://localhost:5001/stand" is active on GET /players
        #and player service is called with 2 player cards and 1 dealer card
        and dealer will finish and score the hand for player "http://localhost:5001/stand"

      Scenario: add and remove a player service
      Given a player service URL "http://localhost:5001/stand" is provided via POST to /players
        and wait "2" seconds
        then the player service URL "http://localhost:5001/stand" is active on GET /players
        then remove the player service URL "http://localhost:5001/stand"
        then there are no active players