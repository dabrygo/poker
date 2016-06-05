'''
Created on Jun 3, 2016

@author: Daniel
'''
import unittest

from poker.Deck import Hand, Card 
from poker.WinPatterns import HighCard, Pair, TwoPair, ThreeOfAKind, Straight, Flush, FullHouse, FourOfAKind, StraightFlush, RoyalFlush

class TestHighCard(unittest.TestCase):
    def test_low_high_card(self):
        bad_hand = Hand(["7D", "2H", "3D", "5C", "4S"])
        self.assertEqual("7", HighCard(bad_hand).values().rank)
    
    def test_ace_high(self):
        good_hand = Hand(["AD", "KD", "QD", "JD", "TD"])
        self.assertEqual("A", HighCard(good_hand).values().rank)
        
    def test_ace_trumps_king(self):
        ace = HighCard(Hand(["AD"]))
        king = HighCard(Hand(["KD"]))
        
        self.assertTrue(Card("AD"), ace.values())
        self.assertTrue(ace.trumps(king))
        
    def test_to_string(self):
        ace = HighCard(Hand(["AS"]))
        self.assertEqual("HighCard (AS)", str(ace))


class TestPair(unittest.TestCase):    
    def test_is_pair(self):
        pair = Hand(["5H", "5S"])
        self.assertTrue(Pair(pair).criterion())
                
    def test_is_not_pair(self):
        pair = Hand(["4S", "5S"])
        self.assertFalse(Pair(pair).criterion())
        
    def test_know_rank_of_pair(self):
        hand = Hand(["7S", "2H", "3D", "7C", "KD"])
        self.assertEqual("7", Pair(hand).values().rank)
        
    def test_to_string(self):
        pair = Pair(Hand(["5H", "5S"]))
        self.assertEqual("Pair (5)", str(pair))


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
    
    def test_to_string(self):
        two_pair = TwoPair(Hand(["5H", "5S", "8H", "8D"]))
        self.assertEqual("TwoPair (5,8)", str(two_pair))


class TestThreeOfAKind(unittest.TestCase):    
    def test_is_three_of_a_kind(self):
        three_of_a_kind = Hand(["5H", "5S", "5D"])
        self.assertTrue(ThreeOfAKind(three_of_a_kind).criterion())
                
    def test_pair_is_not_three_of_a_kind(self):
        pair = Hand(["4S", "5S", "5D"])
        self.assertFalse(ThreeOfAKind(pair).criterion())
        
    def test_four_of_a_kind_is_not_three_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "7C", "7D"])
        self.assertFalse(ThreeOfAKind(hand).criterion())
        
    def test_know_rank_of_three_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "7C", "KD"])
        self.assertEqual("7", ThreeOfAKind(hand).values().rank)
        
    def test_to_string(self):
        three_of_a_kind = ThreeOfAKind(Hand(["5H", "5S", "5D"]))
        self.assertEqual("ThreeOfAKind (5)", str(three_of_a_kind))
        

class TestStraight(unittest.TestCase):
    def test_small_straight(self):
        small_straight = Hand(["2S", "3D", "4C", "5H", "6C"])
        self.assertTrue(Straight(small_straight).criterion())
    
    def test_is_not_straight(self):
        not_straight = Hand(["8S", "3D", "4C", "5H", "6C"])
        self.assertFalse(Straight(not_straight).criterion())
        
    def test_big_straight(self):
        big_straight = Hand(["AS", "KD", "QH", "JS", "TC"])
        self.assertTrue(Straight(big_straight).criterion())
    
    def test_to_string(self):
        straight = Straight(Hand(["2S", "3D", "4C", "5H", "6C"]))
        self.assertEqual("Straight (2-6)", str(straight))
    

class TestFlush(unittest.TestCase):
    def test_is_a_flush(self):
        flush = Hand(["5D", "6D", "2D", "KD", "TD"])
        self.assertTrue(Flush(flush).criterion())
    
    def test_one_not_same_suit(self):
        not_flush = Hand(["5D", "6D", "2H", "KD", "TD"])
        self.assertFalse(Flush(not_flush).criterion())
        
    def test_to_string(self):
        flush = Flush(Hand(["5D", "6D", "2D", "KD", "TD"]))
        self.assertEquals("Flush (D)", str(flush))
        

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
        
    def test_to_string(self):
        full_house = FullHouse(Hand(["4S", "4D", "7H", "7C", "7D"]))
        self.assertEquals("FullHouse (7,4)", str(full_house))


class TestFourOfAKind(unittest.TestCase):    
    def test_is_four_of_a_kind(self):
        four_of_a_kind = Hand(["5H", "5S", "5D", "5C"])
        self.assertTrue(FourOfAKind(four_of_a_kind).criterion())
                
    def test_pair_is_not_four_of_a_kind(self):
        pair = Hand(["4S", "5S", "5D"])
        self.assertFalse(FourOfAKind(pair).criterion())
         
    def test_three_of_a_kind_is_not_four_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "2C", "7D"])
        self.assertFalse(FourOfAKind(hand).criterion())
         
    def test_know_rank_of_four_of_a_kind(self):
        hand = Hand(["7S", "7H", "3D", "7C", "7D"])
        self.assertEqual("7", FourOfAKind(hand).values().rank)
        
    def test_to_string(self):
        four_of_a_kind = FourOfAKind(Hand(["5H", "5S", "5D", "5C"]))
        self.assertEqual("FourOfAKind (5)", str(four_of_a_kind))
 

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
        
    def test_to_string(self):
        straight_flush = StraightFlush(Hand(["2S", "3S", "4S", "5S", "6S"]))
        self.assertEqual("StraightFlush (2-6S)", str(straight_flush))
  
     
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
        
    def test_to_string(self):
        hand = RoyalFlush(Hand(["AD", "KD", "QD", "JD", "TD"]))
        self.assertEquals("RoyalFlush (D)", str(hand))
        
