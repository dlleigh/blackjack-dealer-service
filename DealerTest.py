__author__ = 'dleigh'

import unittest
from Dealer import Dealer
from Card import Card
from mock import patch

class DealerTests(unittest.TestCase):
    def test_get_simple_hand_value(self):
        hand = [Card(2),Card(3)]
        dealer = Dealer(None,None)
        self.assertIn(7,dealer.getHandValues(hand))

    def test_get_multiple_hand_values(self):
        hand = [Card(0),Card(1)]
        dealer = Dealer(None,None)
        values = dealer.getHandValues(hand)
        self.assertIn(3,values)
        self.assertIn(13,values)

    def test_get_complex_hand_values(self):
        hand = [Card(0),Card(1),Card(2),Card(13)]
        dealer = Dealer(None,None)
        values = dealer.getHandValues(hand)
        self.assertIn(7,values)
        self.assertIn(17,values)
        self.assertIn(27,values)

    def test_get_max_hand_value(self):
        hand = [Card(0),Card(1),Card(2),Card(13)]
        dealer = Dealer(None,None)
        maxValue = dealer.getMaxHandValue(hand)
        self.assertEqual(maxValue, 17)

    @patch.object(Card,'getRandomCard')
    def test_dealer_bust(self,mock_bust):
        mock_bust.return_value = Card(12) # return a King
        hand = [Card(1),Card(2),Card(13)]
        dealer = Dealer(None,None)
        dealer.dealersHand = hand
        result = dealer.dealerDraw()
        self.assertEqual(result,0)

    @patch.object(Card,'getRandomCard')
    def test_dealer_not_bust(self,mock_bust):
        mock_bust.return_value = Card(1) # return a 2
        hand = [Card(0),Card(1)]
        dealer = Dealer(None,None)
        dealer.dealersHand = hand
        result = dealer.dealerDraw()
        self.assertEqual(result,17)

    def test_hand_is_busted(self):
        hand = [Card(12),Card(12),Card(12)] # 3 kings
        dealer = Dealer(None,None)
        result = dealer.getMaxHandValue(hand)
        self.assertEqual(result,0)

    def test_player_is_busted(self):
        dealer = Dealer(None,None)
        hand = [Card(12),Card(12),Card(12)] # 3 kings
        dealer.playersHand = hand
        self.assertEqual(dealer.getHandResult(),'lose')

    def test_dealer_is_busted(self):
        dealer = Dealer(None,None)
        hand = [Card(12),Card(12)] # 2 kings
        dealer.playersHand = hand
        hand = [Card(12),Card(12),Card(12)] # 3 kings
        dealer.dealersHand = hand
        self.assertEqual(dealer.getHandResult(),'win')

    def test_tie(self):
        dealer = Dealer(None,None)
        hand = [Card(12),Card(12)] # 2 kings
        dealer.playersHand = hand
        dealer.dealersHand = hand
        self.assertEqual(dealer.getHandResult(),'tie')

    def test_player_wins(self):
        dealer = Dealer(None,None)
        hand = [Card(12),Card(12)] # 2 kings
        dealer.playersHand = hand
        hand = [Card(12),Card(3)] # 1 king, 4
        dealer.dealersHand = hand
        self.assertEqual(dealer.getHandResult(),'win')

    def test_player_loses(self):
        dealer = Dealer(None,None)
        hand = [Card(12),Card(3)] # 1 king, 4
        dealer.playersHand = hand
        hand = [Card(12),Card(12)] # 2 kings
        dealer.dealersHand = hand
        self.assertEqual(dealer.getHandResult(),'lose')

    def test_player_wins_with_blackjack(self):
        dealer = Dealer(None,None)
        hand = [Card(12),Card(0)] # 1 king, one ace
        dealer.playersHand = hand
        hand = [Card(12),Card(3)] # 1 king, 4
        dealer.dealersHand = hand
        self.assertEqual(dealer.getHandResult(),'win')

    def test_get_next_card(self):
        dealer = Dealer(None,None)
        predictedCard = dealer.getNextCardCheat()
        nextCard = dealer.dealCard()
        self.assertEqual(predictedCard.getIndex(),nextCard.getIndex())

if __name__ == '__main__':
    unittest.main()
