'''
Created on Jun 2, 2016

@author: Daniel
'''
import unittest

class Card:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 
             '10', 'J', 'Q', 'K', 'A']
    def __init__(self, string):
        self.rank = string[0]
        self.suit = string[1]
    
    def __lt__(self, other):
        return Card.ranks.index(self.rank) < Card.ranks.index(other.rank)
        
        
class CardTest(unittest.TestCase):
    
    def test_card(self):
        card = Card("AS")
        self.assertEqual("A", card.rank)
        self.assertEqual("S", card.suit)
    
    def test_ace_beats_2(self):
        low_card = Card("2S")
        high_card = Card("AS")
        self.assertLess(low_card, high_card)
        
    def test_ace_ace_draw(self):
        ace_1 = Card("AS")
        ace_2 = Card("AH")
        self.assertFalse(ace_1 < ace_2)
        
    def test_ace_beats_queen(self):
        queen = Card("QH")
        ace = Card("AH")
        self.assertTrue(ace > queen)