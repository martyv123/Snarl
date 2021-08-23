#!/usr/bin/env python3

import sys
import unittest
sys.path.append('../../src/Game')
from level import *
from game import *
from gameManager import *

class TestGameManager(unittest.TestCase):
    def test_accept_player(self):
        p1 = Player("p1")
        p2 = Player("p2")
        p3 = Player("p3")
        p4 = Player("p4")
        p5 = Player("p5")
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([], [], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)

        # Adding a player with the same ID
        self.assertEqual(example_manager.accept_player(p1), True)
        self.assertEqual(example_manager.accept_player(p1), False)

        # Adding up to and no more than 4 players
        self.assertEqual(example_manager.accept_player(p2), True)
        self.assertEqual(example_manager.accept_player(p3), True)
        self.assertEqual(example_manager.accept_player(p4), True)
        self.assertEqual(example_manager.accept_player(p5), False)

    def test_accept_adversary(self):
        a1 = Adversary("a1")
        a2 = Adversary("a2")
        a3 = Adversary("a3")
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([], [], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)

        # Adding an adversary with the same ID
        self.assertEqual(example_manager.accept_adversary(a1), True)
        self.assertEqual(example_manager.accept_adversary(a1), False)

        # Adding some adversaries - no limit here
        self.assertEqual(example_manager.accept_adversary(a2), True)
        self.assertEqual(example_manager.accept_adversary(a3), True)

    def test_accept_movement(self):
        p1 = Player("p1")
        p2 = Player("p2")
        a1 = Adversary("a1")
        a2 = Adversary("a2")
        a1.set_type(Type.ZOMBIE)
        a2.set_type(Type.ZOMBIE)
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([], [], [example_level, example_level2])
        # example_game.place_players()
        # example_game.place_adversaries()

        example_manager = GameManager(example_game)
        example_manager.accept_player(p1)
        example_manager.accept_player(p2)
        example_manager.accept_adversary(a1)
        example_manager.accept_adversary(a2)

        example_manager.start_game()
        example_manager.game.place_players()
        # example_manager.game.place_adversaries()
        
        # Need this because players/adversaries can't be on the same tile
        curr_level = example_manager.game.current_level
        curr_level.place_player(p2, 1, 2)
        curr_level.place_adversary(a1, 9, 7)
        curr_level.place_adversary(a2, 9, 8)

        # Accepting an invalid movement from a player
        self.assertEqual(example_manager.accept_movement((1,4), p1), False)

        # Accepting an invalid movement from an adversary
        self.assertEqual(example_manager.accept_movement((9,7), a1), False)

        # Accepting a valid movement from an adversary not on their turn
        self.assertEqual(example_manager.accept_movement((9, 8), a1), False)

        # Accepting a valid movement from a player not on their turn
        self.assertEqual(example_manager.accept_movement((1, 3), p2), False)

        # Accepting a valid movement from a player on their turn
        self.assertEqual(example_manager.accept_movement((1, 3), p1), True)

        # Accepting a valid movement from a player on their turn - now it's adversaries turn  
        self.assertEqual(example_manager.accept_movement((1, 4), p2), True)

        # Accepting a valid movement from an adversary on their turn  
        self.assertEqual(example_manager.accept_movement((8, 7), a1), True)

        # Accepting a valid movement from an adversary on their turn - now it's players turn
        self.assertEqual(example_manager.accept_movement((8, 8), a2), True)

    def test_send_player_moves(self):
        p1 = Player("p1")
        p2 = Player("p2")
        a1 = Adversary("a1")
        a2 = Adversary("a2")
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([], [], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)
        example_manager.accept_player(p1)
        example_manager.accept_player(p2)
        example_manager.accept_adversary(a1)
        example_manager.accept_adversary(a2)

        example_manager.start_game()
        example_manager.game.place_players()
        
        # Let's move the second player here for convenience
        curr_level = example_manager.game.current_level
        curr_level.place_player(p2, 3, 1)

        p1_valid_moves = example_manager.send_player_moves(p1)
        expected_p1_valid_moves = [(1, 1), (1, 2), (1, 3), (2, 1)]
        p2_valid_moves = example_manager.send_player_moves(p2)
        expected_p2_valid_moves = [(3, 1), (3, 2), (3, 3), (2, 1)]

        # Valid moves should match
        self.assertEqual(p1_valid_moves, expected_p1_valid_moves)
        self.assertEqual(p2_valid_moves, expected_p2_valid_moves)

    def test_send_adversary_moves(self):
        p1 = Player("p1")
        p2 = Player("p2")
        a1 = Adversary("a1")
        a2 = Adversary("a2")
        a1.set_type(Type.ZOMBIE)
        a2.set_type(Type.GHOST)
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)

        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1, 7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([], [], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)
        example_manager.accept_player(p1)
        example_manager.accept_player(p2)
        example_manager.accept_adversary(a1)
        example_manager.accept_adversary(a2)

        example_manager.start_game()
        example_manager.game.place_players()

        # Placing the adversaries
        curr_level = example_manager.game.current_level
        curr_level.place_adversary(a1, 1, 1)
        curr_level.place_adversary(a2, 3, 1)

        a1_valid_moves = example_manager.send_adversary_moves(a1)
        expected_a1_valid_moves = [(1, 1), (1, 2), (2, 1)]
        a2_valid_moves = example_manager.send_adversary_moves(a2)
        expected_a2_valid_moves = [(3, 1), (3, 0), (3, 2), (2, 1), (4, 1)]

        # Valid moves should match
        self.assertEqual(a1_valid_moves, expected_a1_valid_moves)
        self.assertEqual(a2_valid_moves, expected_a2_valid_moves)

if __name__ == '__main__':
    unittest.main()