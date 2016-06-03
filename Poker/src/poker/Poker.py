'''
Created on Jun 2, 2016

@author: Daniel
'''
import unittest

class Card:
    """A playing card that has rank and suit"""
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


class Hand:
    """An unordered collection of five cards"""
    def __init__(self, card_strings):
        self.cards = [Card(card) for card in card_strings]
        self.ranks = [card.rank for card in self.cards]
        
    def has_pair(self):
        return any([self.ranks.count(card.rank) == 2 for card in self.cards])
    
    def sort_hand(self):
        self.cards = sorted(self.cards, reverse=True)
    

class HandTest(unittest.TestCase):
    def test_hand_has_pair(self):
        cards = ["5H", "5C", "6S", "7S", "KD"]
        hand = Hand(cards)
        self.assertTrue(hand.has_pair())
        
    def test_hand_does_not_have_pair(self):
        cards = ["2H", "5C", "6S", "7S", "KD"]
        hand = Hand(cards)
        self.assertFalse(hand.has_pair())
        
    def test_sort_hand(self):
        cards = ["2H", "5C", "6S", "7S", "KD"]
        hand = Hand(cards)
        hand.sort_hand()
        self.assertEqual("K", hand.cards[0].rank)
        

class Game:
    """A set of two hands, one of which is a winner"""
    def __init__(self, hand_1, hand_2):
        hand_1.sort_hand()
        self.hand_1 = hand_1
        hand_2.sort_hand
        self.hand_2 = hand_2
        
    def player_one_wins(self):
        return self.hand_1.cards[0] > self.hand_2.cards[0]
    

class GameTest(unittest.TestCase):
    def test_player_1_has_high_card(self):
        hand_1 = Hand(["5D", "8C", "9S", "JS", "AC"])
        hand_2 = Hand(["2C", "5C", "7D", "8S", "QH"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())        
        
    