'''
Created on Jun 2, 2016

@author: Daniel
'''
import unittest
from poker.WinPatterns import HighCard, Pair, TwoPair, ThreeOfAKind, Straight, Flush, FullHouse, FourOfAKind, StraightFlush, RoyalFlush

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


class Hand:
    """An unordered collection of cards."""
    order = [RoyalFlush, StraightFlush, FourOfAKind, FullHouse, Flush,
             Straight, ThreeOfAKind, TwoPair, Pair, HighCard]
    
    def __init__(self, card_strings):
        self.cards = [Card(card) for card in card_strings]
    
    def sort_hand(self, highest_first=True):
        self.cards = sorted(self.cards, reverse=highest_first)
      
    def win_pattern(self):
        for pattern in Hand.order:
            if pattern(self).criterion():
                return pattern(self)
            
    def score(self):
        return Hand.order.index(self.win_pattern().__class__)
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)
    

class TestHand(unittest.TestCase):
    def test_sort_hand(self):
        hand = Hand(["5H", "5C", "6S", "7S", "KD"])
        hand.sort_hand()
        self.assertEqual("K", hand.cards[0].rank)
    
    # TODO No Magic numbers when it comes to testing score
    def test_royal_flush(self):
        hand = Hand(["JH", "KH", "TH", "AH", "QH"])
        self.assertEqual(0, hand.score())
      
    def test_straight_flush(self):
        hand = Hand(["JH", "8H", "TH", "9H", "7H"])
        self.assertEqual(1, hand.score())
        
    def test_four_of_a_kind(self):
        hand = Hand(["JH", "7H", "7D", "7C", "7S"])
        self.assertEqual(2, hand.score())

    def test_full_house(self):
        hand = Hand(["5H", "5S", "7D", "7C", "7S"])
        self.assertEqual(3, hand.score())

    def test_flush(self):
        hand = Hand(["TH", "7H", "2H", "KH", "3H"])
        self.assertEqual(4, hand.score())
        
    def test_straight(self):
        hand = Hand(["6H", "3S", "4H", "2C", "5H"])
        self.assertEqual(5, hand.score())
        
    def test_three_of_a_kind(self):
        hand = Hand(["6C", "KD", "3H", "3S", "3D"])
        self.assertEqual(6, hand.score())
        
    def test_two_pair(self):
        hand = Hand(["6C", "KD", "6H", "3S", "3D"])
        self.assertEqual(7, hand.score())
        
    def test_pair(self):
        hand = Hand(["6C", "KD", "6H", "7S", "3D"])
        self.assertEqual(8, hand.score())
        
    def test_high_card(self):
        hand = Hand(["6C", "KD", "9H", "7S", "3D"])
        self.assertEqual(9, hand.score())


class Game:
    """A set of two hands, one of which is a winner."""
    def __init__(self, hand_1, hand_2):
        hand_1.sort_hand()
        self.hand_1 = hand_1
        hand_2.sort_hand()
        self.hand_2 = hand_2
    
    def player_one_has_a_better_win_pattern(self):
        return self.hand_1.score() < self.hand_2.score()

    def break_tie(self):
        return self.hand_1.score() == self.hand_2.score()

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
    

class TestGame(unittest.TestCase):
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
                      

# TODO: More "tied" tests
class TestTie(unittest.TestCase):
    @unittest.skip("TODO: Draw conditions")
    def test_both_players_have_royal_flush(self):
        pass
    
    def test_one_player_has_smaller_straight_flush(self):
        hand_1 = Hand(["2H", "3H", "4H", "5H", "6H"])
        hand_2 = Hand(["3S", "4S", "5S", "6S", "7S"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
        
    def test_one_player_has_smaller_four_of_a_kind(self):
        hand_1 = Hand(["5H", "5S", "5C", "5D", "QH"])
        hand_2 = Hand(["KH", "KS", "KC", "KD", "2H"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
        
    @unittest.skip("Worry about multideck games later...")
    def test_both_players_have_same_four_of_a_kind(self):
        pass
    
    @unittest.skip("FIXME")
    def test_one_player_has_smaller_triplet_in_full_house(self):
        hand_1 = Hand(["2H", "2D", "4C", "4D", "4S"])
        hand_2 = Hand(["3C", "3D", "3S", "9S", "9D"])
         
        game = Game(hand_1, hand_2)
         
        self.assertTrue(game.player_one_wins())
    
    @unittest.skip("Worry about multideck games later...")
    def test_one_player_has_smaller_pair_in_full_house(self):
        hand_1 = Hand(["4C", "4D", "4S", "2H", "2D"])
        hand_2 = Hand(["4C", "4D", "4S", "9S", "9D"])
         
        game = Game(hand_1, hand_2)
         
        self.assertTrue(game.player_two_wins())
    
    @unittest.skip("TODO Multideck draw condition")
    def test_players_have_same_full_house(self):
        hand_1 = Hand(["4C", "4D", "4S", "2H", "2D"])
        hand_2 = Hand(["4C", "4D", "4S", "2S", "2C"])
        
        game = Game(hand_1, hand_2)
        
        print(game)
    
    @unittest.skip("TEMPORARY SKIP")
    def test_one_player_has_smaller_high_card_in_flush(self):
        hand_1 = Hand(["2H", "4H", "5H", "6H", "7H"]) 
        hand_2 = Hand(["2C", "4C", "5C", "6C", "8C"]) 
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
    
    @unittest.skip("TEMPORARY SKIP") 
    def test_one_player_has_smallest_card_in_flush(self):
        hand_1 = Hand(["9C", "JC", "QC", "KC", "AC"]) 
        hand_2 = Hand(["8H", "JH", "QH", "KH", "AH"])
        
        game = Game(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
        
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