'''
Created on Jun 4, 2016

@author: Daniel
'''

from poker import WinPatterns

class Card:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    
    """A playing card that has rank and suit."""
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
    """An ordered collection of cards."""   
    def __init__(self, card_strings):
        self.cards = sorted([Card(string) for string in card_strings], reverse=True)
      
    def win_pattern(self):
        for pattern in WinPatterns.order:
            if pattern(self).criterion():
                return pattern(self)
            
    def score(self):
        return WinPatterns.order.index(self.win_pattern().__class__)
    
    def beats(self, other):
        return self.win_pattern().trumps(other.win_pattern())
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)
    

if __name__ == "__main__":
    import unittest
    test_suite = unittest.TestLoader().discover("tests", top_level_dir="../..")
    unittest.TextTestRunner().run(test_suite)
