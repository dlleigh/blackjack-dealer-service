__author__ = 'dleigh'

import unittest
from Card import Card

class TestCard(unittest.TestCase):
    def test_getSuit(self):
        card = Card(43)
        self.assertEqual(card.getSuit(), 'spades')

    def test_getRank(self):
        card = Card(43)
        self.assertEqual(card.getRank(),'5')

    def test_getValue(self):
        card = Card(0)
        self.assertEqual(card.getValue(),[1, 11])
        card = Card(44)
        self.assertEqual(card.getValue(),6)

    def test_get_random_card(self):
        card = Card.getRandomCard()
        self.assertIsInstance(card,Card)

    def test_getDescription(self):
        card = Card(10)
        self.assertEqual(card.getDescription(), 'Jack of clubs')
        card = Card(17)
        self.assertEqual(card.getDescription(), '5 of diamonds')

if __name__ == '__main__':
    unittest.main()
