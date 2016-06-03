'''
Created on Jun 2, 2016

@author: Daniel
'''

import unittest
import poker.Poker

class PokerTest(unittest.TestCase):
    
    def test_ace_of_spades_from_AS(self):
        card = poker.Poker.Card("AS")
        self.assertEqual("A", card.rank)
        self.assertEqual("S", card.suit)