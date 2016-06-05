'''
Created on Jun 3, 2016

@author: Daniel
'''

import unittest

from poker.Poker import OneDeckGame
from poker.Deck import Hand


class TestTie(unittest.TestCase):
    """Players meet the same win condition, but it's not a draw."""   
    def test_player_wins_with_high_card(self):
        hand_1 = Hand(["5D", "8C", "9S", "JS", "AC"])
        hand_2 = Hand(["2C", "5C", "7D", "8S", "QH"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
        
    def test_player_wins_with_high_pair(self):
        pair_8 = Hand(["2C", "3S", "8S", "8D", "TD"])
        pair_5 = Hand(["5H", "5C", "6S", "7S", "KD"])
        
        game = OneDeckGame(pair_8, pair_5)
        
        self.assertTrue(game.player_one_wins())
        
    def test_player_wins_with_higher_first_pair_in_two_pair(self):
        pairs_6_and_8 = Hand(["3S", "6H", "6D", "8C", "8D"])
        pairs_6_and_7 = Hand(["3H", "6S", "6C", "7C", "7D"])
        
        game = OneDeckGame(pairs_6_and_8, pairs_6_and_7)
        
        self.assertTrue(game.player_one_wins())
        
    def test_player_wins_with_higher_second_pair_in_two_pair(self):
        pairs_5_and_8 = Hand(["3H", "5S", "5C", "8S", "8H"])
        pairs_6_and_8 = Hand(["3S", "6H", "6H", "8C", "8D"])
        
        game = OneDeckGame(pairs_6_and_8, pairs_5_and_8)
        
        self.assertTrue(game.player_one_wins())
    def test_player_wins_with_higher_three_of_a_kind(self):
        triple_8 = Hand(["3H", "5S", "8C", "8S", "8H"])
        triple_7 = Hand(["3S", "5H", "7H", "7C", "7D"])
        
        game = OneDeckGame(triple_8, triple_7)
        
        self.assertTrue(game.player_one_wins())
        
    @unittest.skip("Worry about multideck games later...")
    def test_player_wins_with_three_of_a_kind_and_high_card(self):
        triple_8 = Hand(["3H", "7H", "7S", "7D", "KD"])
        triple_7 = Hand(["3S", "7H", "7C", "7D", "AD"])
        
        game = OneDeckGame(triple_8, triple_7)
        
        self.assertTrue(game.player_one_wins())
        
    def test_player_wins_with_higher_straight(self):
        straight_2_6 = Hand(["2S", "3C", "4D", "5H", "6S"])
        straight_3_7 = Hand(["3S", "4C", "5D", "6H", "7S"])
        
        game = OneDeckGame(straight_3_7, straight_2_6)
        
        self.assertTrue(game.player_one_wins())

    def test_player_wins_with_higher_flush(self):
        high_flush = Hand(["AS", "KS", "QS", "JS", "9S"])
        low_flush = Hand(["8S", "7S", "6S", "5S", "3S"])
        
        game = OneDeckGame(high_flush, low_flush)
        
        self.assertTrue(game.player_one_wins())
        
    def test_player_wins_with_higher_card_in_flush(self):
        high_flush = Hand(["AS", "KS", "QS", "JS", "9S"])
        low_flush = Hand(["KH", "QH", "JH", "TH", "8H"])
        
        game = OneDeckGame(high_flush, low_flush)

        self.assertTrue(game.player_one_wins())

    def test_player_wins_with_triplet_in_full_house(self):
        triple_4 = Hand(["2H", "2D", "4C", "4D", "4S"])
        triple_3 = Hand(["3C", "3D", "3S", "9S", "9D"])
         
        game = OneDeckGame(triple_4, triple_3)
         
        self.assertTrue(game.player_one_wins())
    
    @unittest.skip("Worry about multideck games later...")
    def test_player_wins_with_pair_in_full_house(self):
        hand_1 = Hand(["4C", "4D", "4S", "2H", "2D"])
        hand_2 = Hand(["4C", "4D", "4S", "9S", "9D"])
         
        game = OneDeckGame(hand_1, hand_2)
         
        self.assertTrue(game.player_two_wins())
        
    def test_player_wins_with_higher_four_of_a_kind(self):
        hand_1 = Hand(["KH", "KS", "KC", "KD", "2H"])
        hand_2 = Hand(["5H", "5S", "5C", "5D", "QH"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
        
    def test_player_wins_with_higher_straight_flush(self):
        hand_1 = Hand(["3S", "4S", "5S", "6S", "7S"])
        hand_2 = Hand(["2H", "3H", "4H", "5H", "6H"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
    

class TestDraw(unittest.TestCase):
    """Players have effectively the same hand."""
    @unittest.skip("TODO: Draw conditions")
    def test_players_have_same_straight(self):
        pass
    
    @unittest.skip("TODO Multideck draw condition")
    def test_players_have_same_full_house(self):
        hand_1 = Hand(["4C", "4D", "4S", "2H", "2D"])
        hand_2 = Hand(["4C", "4D", "4S", "2S", "2C"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        print(game)
    
    @unittest.skip("TODO: Draw conditions")
    def test_players_have_royal_flush(self):
        pass


class TestLowCardWins(unittest.TestCase):
    """Hands are nearly identical except for lowest card."""
    def test_high_card_wins_on_low_card(self):
        hand_1 = Hand(["2S", "5H", "6D", "7C", "8C"])
        hand_2 = Hand(["3H", "5S", "6C", "7D", "8D"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
        
    def test_pair_wins_on_low_card(self):
        hand_1 = Hand(["2S", "5H", "6D", "7C", "7S"])
        hand_2 = Hand(["3H", "5S", "6C", "7D", "7H"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
        
    def test_two_pair_wins_on_low_card(self):
        hand_1 = Hand(["2S", "6H", "6D", "7C", "7S"])
        hand_2 = Hand(["3H", "6S", "6C", "7D", "7H"])
                
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
    
    @unittest.skip("Worry about multideck games later...")
    def test_three_of_a_kind_wins_on_low_card(self):
        hand_1 = Hand(["2S", "5H", "7H", "7C", "7D"])
        hand_2 = Hand(["3H", "5S", "7H", "7C", "7D"])        
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_two_wins())
        
    def test_flush_wins_on_low_card(self):
        high_flush = Hand(["AS", "KS", "QS", "JS", "9S"])
        low_flush = Hand(["AH", "KH", "QH", "JH", "8H"])
        
        game = OneDeckGame(high_flush, low_flush)

        self.assertTrue(game.player_one_wins())
    
    @unittest.skip("Worry about multideck games later...")
    def test_four_of_a_kind_wins_on_low_card(self):
        hand_1 = Hand(["KH", "KS", "KC", "KD", "QH"])
        hand_2 = Hand(["KH", "KS", "KC", "KD", "2H"])
        
        game = OneDeckGame(hand_1, hand_2)
        
        self.assertTrue(game.player_one_wins())
        