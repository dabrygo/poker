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
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __str__(self):
        return self.rank + self.suit
        
        
class CardTest(unittest.TestCase):
    
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
      

class WinPattern:
    """ """
    def __init__(self, hand):
        self.cards = hand.cards
        self.ranks = [card.rank for card in self.cards]
    
    def criterion(self):
        """What it takes to win with this pattern."""
        pass
    
    def score(self):
        """The ranking of this pattern to others."""
        pass
    
    # TODO: Make property?
    def values(self):
        """A list ranks of the cards involved, highest first."""
        pass
    
    def has_n(self, card, n):
        return self.ranks.count(card.rank) == n


class HighCard(WinPattern):
    def __init__(self, hand):
        self.cards = hand.cards
    
    def criterion(self):
        pass
    
    def values(self):
        sort_by_rank = sorted(self.cards, reverse=True)
        return [sort_by_rank[0].rank]
    
    @staticmethod
    def score():
        return 0
   
   
class TestHighCard(unittest.TestCase):
    def test_low_high_card(self):
        bad_hand = Hand(["7D", "2H", "3D", "5C", "4S"])
        self.assertEqual("7", HighCard(bad_hand).values()[0])
    
    def test_ace_high(self):
        good_hand = Hand(["AD", "KD", "QD", "JD", "TD"])
        self.assertEqual("A", HighCard(good_hand).values()[0])

    
class Pair(WinPattern):
    """A hand has two cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return len(set([card.rank for card in self.cards if self.has_n(card, 2)])) == 1 
    
    def values(self):
        return sorted(list(set([card.rank for card in self.cards if self.has_n(card, 2)])))
    
    @staticmethod
    def score():
        return 1


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


class TwoPair(WinPattern):
    """A hand has two cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return len(set([card.rank for card in self.cards if self.has_n(card, 2)])) == 2 
    
    def values(self):
        return sorted(list(set([card.rank for card in self.cards if self.has_n(card, 2)])))
    
    @staticmethod
    def score():
        return 2


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

        
class ThreeOfAKind(WinPattern):
    """A hand has three cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return any([self.has_n(card, 3) for card in self.cards])
    
    def values(self):
        return sorted(list(set([card.rank for card in self.cards if self.has_n(card, 3)])))
    
    @staticmethod
    def score():
        return 3


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


class Hand:
    """An unordered collection of cards."""
    def __init__(self, card_strings):
        self.cards = [Card(card) for card in card_strings]
    
    def straight(self):
        self.sort_hand(highest_first=False)
        start_index = Card.ranks.index(self.cards[0].rank)
        for i in range(5):
            if self.cards[i].rank != Card.ranks[start_index + i]:
                return False
        return True
    
    def flush(self):
        return all([card.suit == self.cards[0].suit for card in self.cards])
    
    def full_house(self):
        return Pair(self).criterion() and ThreeOfAKind(self).criterion()
    
    def sort_hand(self, highest_first=True):
        self.cards = sorted(self.cards, reverse=highest_first)
        
    def win_pattern(self):
        if ThreeOfAKind(self).criterion():
            return ThreeOfAKind(self)
        if TwoPair(self).criterion():
            return TwoPair(self)
        if Pair(self).criterion():
            return Pair(self)
        return HighCard(self)
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)
    

class HandTest(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(["5H", "5C", "6S", "7S", "KD"])
        
    def test_sort_hand(self):
        self.hand.sort_hand()
        self.assertEqual("K", self.hand.cards[0].rank)
        
    def test_small_straight(self):
        small_straight = Hand(["2S", "3D", "4H", "5S", "6C"])
        self.assertTrue(small_straight.straight())
        
    def test_big_straight(self):
        big_straight = Hand(["AS", "KD", "QH", "JS", "TC"])
        self.assertTrue(big_straight.straight())
        
    def test_all_same_suit(self):
        flush = Hand(["AS", "2S", "5S", "7S", "9S"])
        self.assertTrue(flush.flush())
    
    def test_all_not_same_suit(self):
        not_flush = Hand(["AS", "2S", "5H", "7S", "9S"])
        self.assertFalse(not_flush.flush())
    
    def test_is_full_house(self):
        full_house = Hand(["4S", "4D", "7H", "7C", "7D"])
        self.assertTrue(full_house.full_house())
        

class Game:
    """A set of two hands, one of which is a winner."""
    def __init__(self, hand_1, hand_2):
        hand_1.sort_hand()
        self.hand_1 = hand_1
        hand_2.sort_hand()
        self.hand_2 = hand_2
    
    def player_one_has_a_better_win_pattern(self):
        return self.hand_1.win_pattern().score() > self.hand_2.win_pattern().score()

    def break_tie(self):
        return self.hand_1.win_pattern().score() == self.hand_2.win_pattern().score()

    def player_one_wins(self):
        if self.player_one_has_a_better_win_pattern():
            return True
        elif self.break_tie():
            for i, rank in enumerate(self.hand_1.win_pattern().values()):
                other_guy_rank = self.hand_2.win_pattern().values()[i]
                if Card.ranks.index(rank) < Card.ranks.index(other_guy_rank):
                    return False
            return True
        return False

    def player_two_wins(self):
        return not self.player_one_wins()
    

class GameTest(unittest.TestCase):
    
    def test_pair_eight_beats_pair_five(self):
        eights = Hand(["8S", "8D"])
        fives = Hand(["5H", "5C"])
        
        game = Game(eights, fives)
        
        self.assertTrue(game.player_one_wins())
    
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
    
    def test_pair_jacks_beats_pair_tens(self):
        hand_1 = Hand(["TH", "8H", "5C", "QS", "TC"])
        hand_2 = Hand(["9H", "4D", "JC", "KS", "JS"])
         
        game = Game(hand_1, hand_2)
         
        self.assertTrue(game.player_two_wins())

    def test_three_of_a_kind_beats_two_pair(self):
        hand_1 = Hand(["2S", "2D", "2H", "3S", "4D"])
        hand_2 = Hand(["AS", "AD", "KH", "KS", "QD"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins)
                      
        
# if __name__ == "__main__":
#     with open("../../TestResources/hands.txt", 'r') as f:
#         for i in range(5):
#             cards = f.readline().split()
#             hand_1 = Hand(cards[:5])
#             hand_2 = Hand(cards[5:])
#             print(hand_1)
#             print(hand_2)
#             game = Game(hand_1, hand_2)
#         
#             print(game.player_one_wins())