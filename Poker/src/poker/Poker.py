'''
Created on Jun 2, 2016

@author: Daniel
'''

from poker import WinPatterns
from poker.WinPatterns import HighCard, Pair

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
        

class Hand:
    """An unordered collection of cards."""   
    def __init__(self, card_strings):
        self.cards = [Card(card) for card in card_strings]
    
    def sort_hand(self, highest_first=True):
        self.cards = sorted(self.cards, reverse=highest_first)
      
    def win_pattern(self):
        for pattern in WinPatterns.order:
            if pattern(self).criterion():
                return pattern(self)
            
    def score(self):
        return WinPatterns.order.index(self.win_pattern().__class__)
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)
    

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
            if type(self.hand_1.win_pattern()) in [HighCard, Pair]:
                return self.hand_1.win_pattern().trumps(self.hand_2.win_pattern())
            else:
                for i, rank in enumerate(self.hand_1.win_pattern().values()):
                    other_guy_rank = self.hand_2.win_pattern().values()[i]
                    if Card.ranks.index(rank) < Card.ranks.index(other_guy_rank):
                        return False
                return True
        return False

    def player_two_wins(self):
        return not self.player_one_wins()

      
if __name__ == "__main__":
    import unittest
    test_suite = unittest.TestLoader().discover("tests", top_level_dir="../..")
    unittest.TextTestRunner().run(test_suite)
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