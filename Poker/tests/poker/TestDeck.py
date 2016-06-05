'''
Created on Jun 4, 2016

@author: Daniel
'''
import unittest

from poker.Deck import Card, Hand
from poker import WinPatterns
from poker.WinPatterns import HighCard, Pair, TwoPair, ThreeOfAKind, Straight, Flush, FullHouse, FourOfAKind, StraightFlush, RoyalFlush

class TestCard(unittest.TestCase):
    def test_card(self):
        card = Card("AS")
        self.assertEqual("A", card.rank)
        self.assertEqual("S", card.suit)
    
    def test_ace_high(self):
        low_card = Card("2S")
        high_card = Card("AS")
        self.assertLess(low_card, high_card)
        
    def test_draw(self):
        ace_1 = Card("AS")
        ace_2 = Card("AH")
        self.assertEqual(ace_1, ace_2)
        
    def test_ace_beats_queen(self):
        queen = Card("QH")
        ace = Card("AH")
        self.assertLess(queen, ace)
        
    def test_ten_beats_nine(self):
        ten = Card("TH")
        nine = Card("9H")
        self.assertLess(nine, ten)

        
class TestHand(unittest.TestCase):
    def test_royal_flush(self):
        hand = Hand(["JH", "KH", "TH", "AH", "QH"])
        self.assertEqual(WinPatterns.order.index(RoyalFlush), hand.score())
      
    def test_straight_flush(self):
        hand = Hand(["JH", "8H", "TH", "9H", "7H"])
        self.assertEqual(WinPatterns.order.index(StraightFlush), hand.score())
        
    def test_four_of_a_kind(self):
        hand = Hand(["JH", "7H", "7D", "7C", "7S"])
        self.assertEqual(WinPatterns.order.index(FourOfAKind), hand.score())

    def test_full_house(self):
        hand = Hand(["5H", "5S", "7D", "7C", "7S"])
        self.assertEqual(WinPatterns.order.index(FullHouse), hand.score())

    def test_flush(self):
        hand = Hand(["TH", "7H", "2H", "KH", "3H"])
        self.assertEqual(WinPatterns.order.index(Flush), hand.score())
        
    def test_straight(self):
        hand = Hand(["6H", "3S", "4H", "2C", "5H"])
        self.assertEqual(WinPatterns.order.index(Straight), hand.score())
        
    def test_three_of_a_kind(self):
        hand = Hand(["6C", "KD", "3H", "3S", "3D"])
        self.assertEqual(WinPatterns.order.index(ThreeOfAKind), hand.score())
        
    def test_two_pair(self):
        hand = Hand(["6C", "KD", "6H", "3S", "3D"])
        self.assertEqual(WinPatterns.order.index(TwoPair), hand.score())
        
    def test_pair(self):
        hand = Hand(["6C", "KD", "6H", "7S", "3D"])
        self.assertEqual(WinPatterns.order.index(Pair), hand.score())
        
    def test_high_card(self):
        hand = Hand(["6C", "KD", "9H", "7S", "3D"])
        self.assertEqual(WinPatterns.order.index(HighCard), hand.score())                      
