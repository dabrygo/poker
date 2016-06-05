'''
Created on Jun 2, 2016

@author: Daniel
'''


class OneDeckTwoPlayerGame:
    """A set of two hands, one of which is a winner."""
    def __init__(self, hand_1, hand_2):
        self.hand_1 = hand_1
        self.hand_2 = hand_2
    
    def player_one_has_a_better_win_pattern(self):
        return self.hand_1.score() < self.hand_2.score()

    def break_tie(self):
        return self.hand_1.score() == self.hand_2.score()

    def player_one_wins(self):
        if self.break_tie():
            return self.hand_1.beats(self.hand_2)
        return self.player_one_has_a_better_win_pattern()

    def player_two_wins(self):
        return not self.player_one_wins()

      
if __name__ == "__main__":
    import unittest
    import sys
    from poker.Deck import Hand
    test_suite = unittest.TestLoader().discover("tests", top_level_dir="../..")
    unittest.TextTestRunner(stream=sys.stdout).run(test_suite)
    with open("../../TestResources/10_hands.txt", 'r') as f:
        for i in range(10):
            cards = f.readline().split()
            hand_1 = Hand(cards[:5])
            hand_2 = Hand(cards[5:])
            game = OneDeckTwoPlayerGame(hand_1, hand_2)
         
            print("Game " + str(i+1))
            
            print(" 1. " + str(hand_1))
            print(" 2. " + str(hand_2))
            print(" Player 1 " + ("wins" if game.player_one_wins() else "loses"))
            print()
            