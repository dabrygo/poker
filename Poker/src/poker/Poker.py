'''
Created on Jun 2, 2016

@author: Daniel
'''


class OneDeckGame:
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
    test_suite = unittest.TestLoader().discover("tests", top_level_dir="../..")
    unittest.TextTestRunner().run(test_suite)
#     with open("../../TestResources/hands.txt", 'r') as f:
#         for i in range(5):
#             cards = f.readline().split()
#             hand_1 = Hand(cards[:5])
#             hand_2 = Hand(cards[5:])
#             print(hand_1)
#             print(hand_2)
#             game = OneDeckGame(hand_1, hand_2)
#         
#             print(game.player_one_wins())