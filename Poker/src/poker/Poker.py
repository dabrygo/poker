'''
Created on Jun 2, 2016

@author: Daniel
'''
import unittest

class Card:
    """A playing card that has rank and suit."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 
             'T', 'J', 'Q', 'K', 'A']
    def __init__(self, string):
        self.rank = string[0]
        self.suit = string[1]
    
    def __lt__(self, other):
        return Card.ranks.index(self.rank) < Card.ranks.index(other.rank)
    
    def __str__(self):
        return self.rank + self.suit
        
        
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
        self.assertLess(queen, ace)
        
    def test_ten_beats_nine(self):
        ten = Card("TH")
        nine = Card("9H")
        self.assertLess(nine, ten)
      

class Hand:
    """An unordered collection of cards."""
    def __init__(self, card_strings):
        self.cards = [Card(card) for card in card_strings]
        self.ranks = [card.rank for card in self.cards]
    
    def has_n(self, card, n):
        return self.ranks.count(card.rank) == n
    
    def find_pair(self):
        return set([card.rank for card in self.cards if self.has_n(card, 2)]) 
    
    def pair(self):
        return str(self.find_pair()) if len(self.find_pair()) == 1 else []
    
    def two_pair(self):
        return len(self.find_pair()) == 2
    
    def three_of_a_kind(self):
        return set([card.rank for card in self.cards if self.has_n(card, 3)])
    
    def straight(self):
        self.sort_hand(highest_first=False)
        start_index = Card.ranks.index(self.cards[0].rank)
        for i in range(5):
            if self.cards[i].rank != Card.ranks[start_index + i]:
                return False
        return True
    
    def sort_hand(self, highest_first=True):
        self.cards = sorted(self.cards, reverse=highest_first)
        
    def score(self):
        if self.three_of_a_kind():
            return 3
        if self.two_pair():
            return 2
        if self.pair():
            return 1
        return 0
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)
    

class HandTest(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(["5H", "5C", "6S", "7S", "KD"])
    
    def test_is_pair(self):
        pair = Hand(["5H", "5S"])
        self.assertTrue(pair.has_n(Card("5H"), 2))
        
    def test_is_not_pair(self):
        pair = Hand(["4S", "5S"])
        self.assertFalse(pair.has_n(Card("4S"), 2))
        
    def test_hand_has_pair(self):
        self.assertTrue(self.hand.pair())
        
    def test_hand_does_not_have_pair(self):
        hand = Hand(["2H", "5C", "6S", "7S", "KD"])
        self.assertFalse(hand.pair())
        
    def test_sort_hand(self):
        self.hand.sort_hand()
        self.assertEqual("K", self.hand.cards[0].rank)
        
    def test_pair_eight_beats_pair_five(self):
        eights = Hand(["8S", "8D"])
        fives = Hand(["5H", "5C"])
        
        self.assertLess(fives.pair(), eights.pair())
        
    def test_can_see_two_pair(self):
        one_pair = Hand(["2S", "2H", "3S", "4S"])
        two_pair = Hand(["2S", "2H", "4S", "4H"])
        self.assertTrue(two_pair.two_pair())
        self.assertFalse(one_pair.two_pair())
        
    def test_three_of_a_kind_has_exactly_three(self):
        two_of_a_kind = Hand(["2S", "2H", "3D", "4S", "5D"])
        three_of_a_kind = Hand(["2S", "2H", "2D", "7S", "JD"])
        four_of_a_kind = Hand(["2S", "2H", "2D", "2S", "JD"])
        self.assertFalse(two_of_a_kind.three_of_a_kind())
        self.assertTrue(three_of_a_kind.three_of_a_kind())
        self.assertFalse(four_of_a_kind.three_of_a_kind())
        
    def test_small_straight(self):
        small_straight = Hand(["2S", "3D", "4H", "5S", "6C"])
        self.assertTrue(small_straight.straight())
        
    def test_big_straight(self):
        big_straight = Hand(["AS", "KD", "QH", "JS", "TC"])
        self.assertTrue(big_straight.straight())
        

class Game:
    """A set of two hands, one of which is a winner."""
    def __init__(self, hand_1, hand_2):
        hand_1.sort_hand()
        self.hand_1 = hand_1
        hand_2.sort_hand()
        self.hand_2 = hand_2
    
    def player_one_has_a_better_hand(self):
        return self.hand_1.score() > self.hand_2.score()

    def both_players_have_pairs(self):
        return self.hand_1.score() == 1 == self.hand_2.score()

    def both_players_have_two_pair(self):
        return self.hand_1.score() == 2 == self.hand_2.score()

    def player_one_wins(self):
        if self.player_one_has_a_better_hand():
            return True
        elif self.both_players_have_two_pair():
            return self.hand_1.two_pair() > self.hand_2.two_pair() 
        elif self.both_players_have_pairs():
            return self.hand_1.pair() > self.hand_2.pair()
        return self.hand_1.cards[0] > self.hand_2.cards[0]

    def player_two_wins(self):
        return not self.player_one_wins()
    

class GameTest(unittest.TestCase):
    def test_player_1_has_high_card(self):
        hand_1 = Hand(["5D", "8C", "9S", "JS", "AC"])
        hand_2 = Hand(["2C", "5C", "7D", "8S", "QH"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
    
    def test_player_2_has_high_pair(self):
        hand_1 = Hand(["5H", "5C", "6S", "7S", "KD"])
        hand_2 = Hand(["2C", "3S", "8S", "8D", "TD"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
        
    def test_two_pair_beats_higher_pair(self):
        hand_1 = Hand(["2S", "2H", "3S", "3H"])
        hand_2 = Hand(["KS", "KH", "6S", "5H"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
    
#     def test_two_pair_jacks_beats_two_pair_tens(self):
#         hand_1 = Hand(["TH", "8H", "5C", "QS", "TC"])
#         hand_2 = Hand(["9H", "4D", "JC", "KS", "JS"])
#         
#         game = Game(hand_1, hand_2)
#         
#         self.assertTrue(game.player_two_wins())

    def test_three_of_a_kind_beats_two_pair(self):
        hand_1 = Hand(["2S", "2D", "2H", "3S", "4D"])
        hand_2 = Hand(["AS", "AD", "KH", "KS", "QD"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins)
                      
        
if __name__ == "__main__":
    with open("../../TestResources/hands.txt", 'r') as f:
        for i in range(5):
            cards = f.readline().split()
            hand_1 = Hand(cards[:5])
            hand_2 = Hand(cards[5:])
            print(hand_1)
            print(hand_2)
            game = Game(hand_1, hand_2)
        
            print(game.player_one_wins())