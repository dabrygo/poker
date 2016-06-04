'''
Created on Jun 3, 2016

@author: dbgod
'''
import unittest

from poker import Poker 
from poker import WinPatterns

class TestHighCard(unittest.TestCase):
    def test_low_high_card(self):
        bad_hand = Poker.Hand(["7D", "2H", "3D", "5C", "4S"])
        self.assertEqual("7", WinPatterns.HighCard(bad_hand).values()[0])
    
    def test_ace_high(self):
        good_hand = Poker.Hand(["AD", "KD", "QD", "JD", "TD"])
        self.assertEqual("A", WinPatterns.HighCard(good_hand).values()[0])


class TestPair(unittest.TestCase):    
    def test_is_pair(self):
        pair = Poker.Hand(["5H", "5S"])
        self.assertTrue(WinPatterns.Pair(pair).criterion())
                
    def test_is_not_pair(self):
        pair = Poker.Hand(["4S", "5S"])
        self.assertFalse(WinPatterns.Pair(pair).criterion())
        
    def test_know_rank_of_pair(self):
        hand = Poker.Hand(["7S", "2H", "3D", "7C", "KD"])
        self.assertEqual(["7"], WinPatterns.Pair(hand).values())


class TestTwoPair(unittest.TestCase):    
    def test_is_two_pair(self):
        two_pair = Poker.Hand(["5H", "5S", "8H", "8D"])
        self.assertTrue(WinPatterns.TwoPair(two_pair).criterion())
                
    def test_lone_pair_is_not_two_pair(self):
        pair = Poker.Hand(["4S", "4S", "7H", "8D"])
        self.assertFalse(WinPatterns.TwoPair(pair).criterion())
        
    def test_know_ranks_of_two_pair(self):
        hand = Poker.Hand(["7S", "3H", "3D", "7C", "KD"])
        self.assertEqual(["3", "7"], WinPatterns.TwoPair(hand).values())


class TestThreeOfAKind(unittest.TestCase):    
    def test_is_three_of_a_kind(self):
        pair = Poker.Hand(["5H", "5S", "5D"])
        self.assertTrue(WinPatterns.ThreeOfAKind(pair).criterion())
                
    def test_pair_is_not_three_of_a_kind(self):
        pair = Poker.Hand(["4S", "5S", "5D"])
        self.assertFalse(WinPatterns.ThreeOfAKind(pair).criterion())
        
    def test_four_of_a_kind_is_not_three_of_a_kind(self):
        hand = Poker.Hand(["7S", "7H", "3D", "7C", "7D"])
        self.assertFalse(WinPatterns.ThreeOfAKind(hand).criterion())
        
    def test_know_rank_of_three_of_a_kind(self):
        hand = Poker.Hand(["7S", "7H", "3D", "7C", "KD"])
        self.assertEqual(["7"], WinPatterns.ThreeOfAKind(hand).values())
        

class TestStraight(unittest.TestCase):
    def test_small_straight(self):
        small_straight = Poker.Hand(["2S", "3D", "4C", "5H", "6C"])
        self.assertTrue(WinPatterns.Straight(small_straight).criterion())
    
    def test_is_not_straight(self):
        straight = Poker.Hand(["8S", "3D", "4C", "5H", "6C"])
        self.assertFalse(WinPatterns.Straight(straight).criterion())
        
    def test_big_straight(self):
        big_straight = Poker.Hand(["AS", "KD", "QH", "JS", "TC"])
        self.assertTrue(WinPatterns.Straight(big_straight).criterion())
        
    def test_values(self):
        pass
    

class TestFlush(unittest.TestCase):
    def test_is_a_flush(self):
        flush = Poker.Hand(["5D", "6D", "2D", "KD", "TD"])
        self.assertTrue(WinPatterns.Flush(flush).criterion())
    
    def test_one_not_same_suit(self):
        not_flush = Poker.Hand(["5D", "6D", "2H", "KD", "TD"])
        self.assertFalse(WinPatterns.Flush(not_flush).criterion())
        

class TestFullHouse(unittest.TestCase):
    def test_is_full_house(self):
        full_house = Poker.Hand(["4S", "4D", "7H", "7C", "7D"])
        self.assertTrue(WinPatterns.FullHouse(full_house).criterion())
        
    def test_two_pair_is_not_full_house(self):
        two_pair = Poker.Hand(["4S", "4D", "7H", "7C", "8D"])
        self.assertFalse(WinPatterns.FullHouse(two_pair).criterion())
        
    def test_suits_do_not_make_a_full_house(self):
        suit_house = Poker.Hand(["2S", "4S", "7H", "6H", "8H"])
        self.assertFalse(WinPatterns.FullHouse(suit_house).criterion())
        
    def test_value_full_house(self):
        hand = Poker.Hand(["4C", "2H", "2D", "4D", "4S"])
        self.assertEqual(["4", "2"], WinPatterns.FullHouse(hand).values())
        

class TestFourOfAKind(unittest.TestCase):    
    def test_is_four_of_a_kind(self):
        pair = Poker.Hand(["5H", "5S", "5D", "5C"])
        self.assertTrue(WinPatterns.FourOfAKind(pair).criterion())
                
    def test_pair_is_not_four_of_a_kind(self):
        pair = Poker.Hand(["4S", "5S", "5D"])
        self.assertFalse(WinPatterns.FourOfAKind(pair).criterion())
         
    def test_three_of_a_kind_is_not_four_of_a_kind(self):
        hand = Poker.Hand(["7S", "7H", "3D", "2C", "7D"])
        self.assertFalse(WinPatterns.FourOfAKind(hand).criterion())
         
    def test_know_rank_of_four_of_a_kind(self):
        hand = Poker.Hand(["7S", "7H", "3D", "7C", "7D"])
        self.assertEqual(["7"], WinPatterns.FourOfAKind(hand).values())
 

class TestStraightFlush(unittest.TestCase):
    def test_is_straight_flush(self):
        hand = Poker.Hand(["2S", "3S", "4S", "5S", "6S"])
        self.assertTrue(WinPatterns.StraightFlush(hand).criterion())
        
    def test_straight_is_not_always_straight_flush(self):
        hand = Poker.Hand(["2S", "3D", "4S", "5S", "6S"])
        self.assertFalse(WinPatterns.StraightFlush(hand).criterion())
        
    def test_flush_is_not_always_straight_flush(self):
        hand = Poker.Hand(["2S", "3S", "4S", "5S", "7S"])
        self.assertFalse(WinPatterns.StraightFlush(hand).criterion())
        
    def test_straight_flush_values(self):
        hand = Poker.Hand(["7H", "5H", "8H", "4H", "6H"])
        self.assertEqual(["4", "5", "6", "7", "8"], WinPatterns.StraightFlush(hand).values())
  
     
class TestRoyalFlush(unittest.TestCase):
    def test_royal_flush(self):
        hand = Poker.Hand(["AD", "KD", "QD", "JD", "TD"])
        self.assertTrue(WinPatterns.RoyalFlush(hand).criterion())
    
    def test_straight_flush_but_not_royal(self):
        hand = Poker.Hand(["KD", "QD", "JD", "TD", "9D"])
        self.assertFalse(WinPatterns.RoyalFlush(hand).criterion())
    
    def test_straight_but_not_royal_flush(self):
        hand = Poker.Hand(["AS", "KD", "QD", "JD", "TD"])
        self.assertFalse(WinPatterns.RoyalFlush(hand).criterion())
        
