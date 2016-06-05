'''
Created on Jun 3, 2016

@author: dbgod
'''

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class WinPattern:
    """"""
    def __init__(self, hand):
        self.cards = hand.cards
        self.ranks = [card.rank for card in self.cards]
    
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
        sort_by_rank = sorted(self.cards, reverse=True)
        return sort_by_rank[0].rank
    
    def trumps(self, other):
        sort_by_rank = sorted(self.cards, reverse=True)
        other_sort_by_rank = sorted(other.cards, reverse=True)
        for i, card in enumerate(sort_by_rank):
            if card < other_sort_by_rank[i]:
                return False
            elif card == other_sort_by_rank[i]:
                continue
            else:
                return True
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
            if ranks.index(rank) == ranks.index(other_pair_ranks[i]):
                continue
            if ranks.index(rank) > ranks.index(other_pair_ranks[i]):
                return True
            if ranks.index(rank) < ranks.index(other_pair_ranks[i]):
                return False
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
    # TODO Move ranks to someplace accessible to poker.Poker.Card
    #      and here
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        self.cards = sorted(self.cards, reverse=False)
        start_index = ranks.index(self.cards[0].rank)
        for i in range(5):
            if self.cards[i].rank != ranks[start_index + i]:
                return False
        return True
    
    def trumps(self, other):
        return HighCard.trumps(self, other)
      

class Flush(WinPattern):
    """A hand has cards of only one suit."""
    def __init__(self, hand):
        super().__init__(hand)
        
    def criterion(self):
        return len(set([card.suit for card in self.cards])) == 1
    
    def trumps(self, other):
        return HighCard.trumps(self, other)
    

class FullHouse(WinPattern):
    """A hand has a pair of one rank and a three of a kind of another."""
    def __init__(self, hand):
        super().__init__(hand)
        
    def criterion(self):
        return Pair(self).criterion() and ThreeOfAKind(self).criterion()
    
    def trumps(self, that):
        this_triplet_card = ThreeOfAKind(self).values()
        that_triplet_card = ThreeOfAKind(that).values()

        if this_triplet_card != that_triplet_card:
            return this_triplet_card > that_triplet_card
        else:
            pair = Pair(self).values()[0]
            other_pair = Pair(self).values()[0]
            if ranks.index(pair) < ranks.index(other_pair):
                return False
            elif ranks.index(pair) > ranks.index(other_pair):
                return True
            else:
                raise NotImplementedError # Draw


class FourOfAKind(WinPattern):
    """A hand has four cards of the same rank."""
    def __init__(self, hand):
        super().__init__(hand)
    
    def criterion(self):
        return any([self.has_n(card, 4) for card in self.cards])
    
    def values(self):
        return sorted(set([card.rank for card in self.cards if self.has_n(card, 4)]))
    
    def trumps(self, other):
        quartet = self.values()[0]
        other_quartet = other.values()[0]
        if ranks.index(quartet) < ranks.index(other_quartet):
            return False
        elif ranks.index(quartet) > ranks.index(other_quartet):
            return True
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
        return StraightFlush(self).criterion() and HighCard(self).values()[0] == "A" 
        
    def trumps(self, other):
        raise NotImplementedError # Draw


order = [RoyalFlush, StraightFlush, FourOfAKind, FullHouse, Flush,
         Straight, ThreeOfAKind, TwoPair, Pair, HighCard]


if __name__ == "__main__":
    import unittest
    test_suite = unittest.TestLoader().discover("tests", top_level_dir="../..")
    unittest.TextTestRunner().run(test_suite)