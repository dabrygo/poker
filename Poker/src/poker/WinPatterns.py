'''
Created on Jun 3, 2016

@author: Daniel
'''

from poker import Deck

class WinPattern:
    """"""
    def __init__(self, hand):
        self.cards = hand.cards
        self.ranks = [card.rank for card in self.cards]
        self.suits = [card.suit for card in self.cards]
    
    def criterion(self):
        """Return true if hand matches this pattern."""
        pass
    
    # TODO: Make property?
    def values(self):
        """A list ranks of the cards involved."""
        pass
    
    # TODO Refactor to MatchingCards subclass?
    def has_n(self, card, n):
        return self.ranks.count(card.rank) == n
    
    def trumps(self, other):
        raise NotImplementedError
    

class HighCard(WinPattern):
    """The highest-ranking card in a hand."""
    def __init__(self, hand):
        super().__init__(hand)
            
    def criterion(self):
        return True
    
    def values(self):
        return self.cards[0]
    
    def trumps(self, other):
        for i, card in enumerate(self.cards):
            if card != other.cards[i]:
                return other.cards[i] < card
        raise NotImplementedError # Draw
   
          
class Pair(WinPattern):
    """A hand has two cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return len(set([card.rank for card in self.cards if self.has_n(card, 2)])) == 1 
    
    def values(self):
        for card in self.cards:
            if self.has_n(card, 2):
                return card
    
    def trumps(self, that):
        if self.values() != that.values():
            return that.values() < self.values()
        return HighCard.trumps(self, that)


class TwoPair(WinPattern):
    """A hand has two sets of two cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return len(set([card.rank for card in self.cards if self.has_n(card, 2)])) == 2 
    
    def values(self):
        return sorted(list(set([card.rank for card in self.cards if self.has_n(card, 2)])))
    
    def trumps(self, other):
        pair_ranks = self.values()
        other_pair_ranks = other.values()
        for i, rank in enumerate(pair_ranks):
            if Deck.Card.ranks.index(rank) != Deck.Card.ranks.index(other_pair_ranks[i]):
                return Deck.Card.ranks.index(other_pair_ranks[i]) < Deck.Card.ranks.index(rank) 
        return HighCard.trumps(self, other)
    
        
class ThreeOfAKind(WinPattern):
    """A hand has three cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return any([self.has_n(card, 3) for card in self.cards])
    
    def values(self):
        for card in self.cards:
            if self.has_n(card, 3):
                return card

    def trumps(self, that):
        if self.values() != that.values():
            return that.values() < self.values()
        return HighCard.trumps(self, that) 


class Straight(WinPattern):
    """A hand has five cards with consecutive ranks."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        start_index = Deck.Card.ranks.index(self.cards[0].rank)
        for i in range(5):
            if self.cards[i].rank != Deck.Card.ranks[start_index - i]:
                return False
        return True
    
    def trumps(self, other):
        return HighCard.trumps(self, other)
      

class Flush(WinPattern):
    """A hand has cards of only one suit."""
    def __init__(self, hand):
        super().__init__(hand)
        
    def criterion(self):
        return len(set(self.suits)) == 1
    
    def trumps(self, other):
        return HighCard.trumps(self, other)
    

class FullHouse(WinPattern):
    """A hand has a pair and a three-of-a-kind of different ranks."""
    def __init__(self, hand):
        super().__init__(hand)
        
    def criterion(self):
        return Pair(self).criterion() and ThreeOfAKind(self).criterion()
    
    def trumps(self, that):
        this_triplet_card = ThreeOfAKind(self).values()
        that_triplet_card = ThreeOfAKind(that).values()

        if this_triplet_card != that_triplet_card:
            return that_triplet_card < this_triplet_card 
        else:
            pair = Pair(self).values()
            other_pair = Pair(self).values()
            if pair != other_pair:
                return other_pair < pair
            raise NotImplementedError # Draw


class FourOfAKind(WinPattern):
    """A hand has four cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return any([self.has_n(card, 4) for card in self.cards])
    
    def values(self):
        for card in self.cards:
            if self.has_n(card, 4):
                return card
    
    def trumps(self, other):
        if self.values() != other.values():
            return other.values() < self.values()
        return HighCard.trumps(self, other) 


class StraightFlush(WinPattern):
    """A hand has consecutive cards of the same suit."""
    def __init__(self, hand):
        super().__init__(hand)
        
    def criterion(self):
        return Straight(self).criterion() and Flush(self).criterion()
    
    def trumps(self, other):
        return Straight(self).trumps(other)
    

class RoyalFlush(WinPattern):
    """A hand has the highest consecutive cards of the same suit."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return StraightFlush(self).criterion() and HighCard(self).values().rank == "A" 
        
    def trumps(self, other):
        raise NotImplementedError # Draw


order = [RoyalFlush, StraightFlush, FourOfAKind, FullHouse, Flush,
         Straight, ThreeOfAKind, TwoPair, Pair, HighCard]


if __name__ == "__main__":
    import unittest
    import sys
    test_suite = unittest.TestLoader().discover("tests", top_level_dir="../..")
    unittest.TextTestRunner(stream=sys.stdout).run(test_suite)