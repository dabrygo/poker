'''
Created on Jun 3, 2016

@author: Daniel
'''
import unittest

from poker.Poker import Hand 
from poker.WinPatterns import HighCard, Pair, TwoPair, ThreeOfAKind, Straight, Flush, FullHouse, FourOfAKind, StraightFlush, RoyalFlush

class TestHighCard(unittest.TestCase):
    def test_low_high_card(self):
        bad_hand = Hand(["7D", "2H", "3D", "5C", "4S"])
        self.assertEqual("7", HighCard(bad_hand).values()[0])
    
    def test_ace_high(self):
        good_hand = Hand(["AD", "KD", "QD", "JD", "TD"])
        self.assertEqual("A", HighCard(good_hand).values()[0])


class TestPair(unittest.TestCase):    
    def test_is_pair(self):
        pair = Hand(["5H", "5S"])
        self.assertTrue(Pair(pair).criterion())
                
    def test_is_not_pair(self):
        pair = Hand(["4S", "5S"])
        self.assertFalse(Pair(pair).criterion())
        
    def test_know_rank_of_pair(self):
        hand = Hand(["7S", "2H", "3D", "7C", "KD"])
        self.assertEqual(["7"], Pair(hand).values())


class TestTwoPair(unittest.TestCase):    
    def test_is_two_pair(self):
        two_pair = Hand(["5H", "5S", "8H", "8D"])
        self.assertTrue(TwoPair(two_pair).criterion())
                
    def test_lone_pair_is_not_two_pair(self):
        pair = Hand(["4S", "4S", "7H", "8D"])
        self.assertFalse(TwoPair(pair).criterion())
        
    def test_know_ranks_of_two_pair(self):
        hand = Hand(["7S", "3H", "3D", "7C", "KD"])
        self.assertEqual(["3", "7"], TwoPair(hand).values())


class TestThreeOfAKind(unittest.TestCase):    
    def test_is_three_of_a_kind(self):
        pair = Hand(["5H", "5S", "5D"])
        self.assertTrue(ThreeOfAKind(pair).criterion())
                
    def test_pair_is_not_three_of_a_kind(self):
        pair = Hand(["4S", "5S", "5D"])
        self.assertFalse(ThreeOfAKind(pair).criterion())
        
    def test_four_of_a_kind_is_not_three_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "7C", "7D"])
        self.assertFalse(ThreeOfAKind(hand).criterion())
        
    def test_know_rank_of_three_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "7C", "KD"])
        self.assertEqual(["7"], ThreeOfAKind(hand).values())
        

class TestStraight(unittest.TestCase):
    def test_small_straight(self):
        small_straight = Hand(["2S", "3D", "4C", "5H", "6C"])
        self.assertTrue(Straight(small_straight).criterion())
    
    def test_is_not_straight(self):
        straight = Hand(["8S", "3D", "4C", "5H", "6C"])
        self.assertFalse(Straight(straight).criterion())
        
    def test_big_straight(self):
        big_straight = Hand(["AS", "KD", "QH", "JS", "TC"])
        self.assertTrue(Straight(big_straight).criterion())
        
    def test_values(self):
        pass
    

class TestFlush(unittest.TestCase):
    def test_is_a_flush(self):
        flush = Hand(["5D", "6D", "2D", "KD", "TD"])
        self.assertTrue(Flush(flush).criterion())
    
    def test_one_not_same_suit(self):
        not_flush = Hand(["5D", "6D", "2H", "KD", "TD"])
        self.assertFalse(Flush(not_flush).criterion())
        

class TestFullHouse(unittest.TestCase):
    def test_is_full_house(self):
        full_house = Hand(["4S", "4D", "7H", "7C", "7D"])
        self.assertTrue(FullHouse(full_house).criterion())
        
    def test_two_pair_is_not_full_house(self):
        two_pair = Hand(["4S", "4D", "7H", "7C", "8D"])
        self.assertFalse(FullHouse(two_pair).criterion())
        
    def test_suits_do_not_make_a_full_house(self):
        suit_house = Hand(["2S", "4S", "7H", "6H", "8H"])
        self.assertFalse(FullHouse(suit_house).criterion())
        
    def test_value_full_house(self):
        hand = Hand(["4C", "2H", "2D", "4D", "4S"])
        self.assertEqual(["4", "2"], FullHouse(hand).values())
        

class TestFourOfAKind(unittest.TestCase):    
    def test_is_four_of_a_kind(self):
        pair = Hand(["5H", "5S", "5D", "5C"])
        self.assertTrue(FourOfAKind(pair).criterion())
                
    def test_pair_is_not_four_of_a_kind(self):
        pair = Hand(["4S", "5S", "5D"])
        self.assertFalse(FourOfAKind(pair).criterion())
         
    def test_three_of_a_kind_is_not_four_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "2C", "7D"])
        self.assertFalse(FourOfAKind(hand).criterion())
         
    def test_know_rank_of_four_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "7C", "7D"])
        self.assertEqual(["7"], FourOfAKind(hand).values())
 

class TestStraightFlush(unittest.TestCase):
    def test_is_straight_flush(self):
        hand = Hand(["2S", "3S", "4S", "5S", "6S"])
        self.assertTrue(StraightFlush(hand).criterion())
        
    def test_straight_is_not_always_straight_flush(self):
        hand = Hand(["2S", "3D", "4S", "5S", "6S"])
        self.assertFalse(StraightFlush(hand).criterion())
        
    def test_flush_is_not_always_straight_flush(self):
        hand = Hand(["2S", "3S", "4S", "5S", "7S"])
        self.assertFalse(StraightFlush(hand).criterion())
        
    def test_straight_flush_values(self):
        hand = Hand(["7H", "5H", "8H", "4H", "6H"])
        self.assertEqual(["4", "5", "6", "7", "8"], StraightFlush(hand).values())
  
     
class TestRoyalFlush(unittest.TestCase):
    def test_royal_flush(self):
        hand = Hand(["AD", "KD", "QD", "JD", "TD"])
        self.assertTrue(RoyalFlush(hand).criterion())
    
    def test_straight_flush_but_not_royal(self):
        hand = Hand(["KD", "QD", "JD", "TD", "9D"])
        self.assertFalse(RoyalFlush(hand).criterion())
    
    def test_straight_but_not_royal_flush(self):
        hand = Hand(["AS", "KD", "QD", "JD", "TD"])
        self.assertFalse(RoyalFlush(hand).criterion())
        
