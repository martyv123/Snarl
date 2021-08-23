#!/usr/bin/env python3

import sys
import unittest

sys.path.append('../../src/Game')
from character import *
from level import *
from game import *
from gameManager import *
from ruleChecker import *


class TestRuleChecker(unittest.TestCase):
    def test_is_valid_game_state(self):
        # A correct game state in progress
        p1 = Player("p1")
        a1 = Adversary("a1")
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

        example_game = Game([p1], [a1], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)
        example_rulechecker = example_manager.rulechecker
        example_manager.start_game()

        self.assertEqual(example_rulechecker.is_valid_game_state(), True)

        # A correct game state that has ended
        p1.active = False
        example_manager.end_game()
        self.assertEqual(example_rulechecker.is_valid_game_state(), True)

        # An incorrect game state with 0 players
        bad_game_1 = Game([], [], [example_level, example_level2])
        rc1 = RuleChecker(bad_game_1)
        self.assertEqual(rc1.is_valid_game_state(), False)

        # An incorrect game state with 5 players
        bad_game_2 = Game([p1, p1, p1, p1, p1], [], [example_level, example_level2])
        rc2 = RuleChecker(bad_game_2)
        self.assertEqual(rc2.is_valid_game_state(), False)

        # An incorrect game state with no active players but the game is not over
        p1.active = False
        example_manager.start_game()
        self.assertEqual(rc2.is_valid_game_state(), False)

        # An incorrect game state with active player but the game is over
        p1.active = True
        example_manager.end_game()
        self.assertEqual(rc2.is_valid_game_state(), False)

    def test_is_valid_level(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)

        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.add_hallway(1, 4, 6, 7, [(1, 7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([p1], [a1], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)
        example_rulechecker = example_manager.rulechecker
        example_manager.start_game()

        # No key or exit in level
        self.assertEqual(example_rulechecker.is_valid_level(example_level), False)

        # No key in level
        example_level.set_level_exit(8, 7)
        self.assertEqual(example_rulechecker.is_valid_level(example_level), False)

        # Key and exit in level
        example_level.set_key(7, 7)
        self.assertEqual(example_rulechecker.is_valid_level(example_level), True)

    def test_is_valid_movement(self):
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

        example_game = Game([p1], [a1], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        example_manager = GameManager(example_game)
        example_rulechecker = example_manager.rulechecker
        example_manager.start_game()

        # Player stays put on current tile
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (p1.x_pos, p1.y_pos)), True)

        # Adversary stays put on current tile
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (a1.x_pos, a1.y_pos)), True)

        # Player moves one tile in a valid direction
        example_level.place_player(p1, 2, 2)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (2, 1)), True)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (2, 3)), True)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (1, 2)), True)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (3, 2)), True)

        # Player moves two tiles in a valid direction
        example_level.place_player(p1, 1, 2)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (3, 2)), True)
        example_level.place_player(p1, 3, 2)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (1, 2)), True)
        example_level.place_player(p1, 1, 1)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (1, 3)), True)
        example_level.place_player(p1, 1, 3)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (1, 1)), True)

        # Player tries to move more than two tiles
        example_level.place_player(p1, 1, 1)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (1, 4)), False)

        # Player tries to move onto wall tile
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (1, 0)), False)

        # Player tries to move onto non tile
        example_level.place_player(p1, 2, 3)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (2, 4)), False)

        # Player tries to move onto another player
        example_level.place_player(p2, 2, 1)
        self.assertEqual(example_rulechecker.is_valid_movement(p1, (2, 1)), False)

        # Adversary moves one tile in a valid direction
        example_level.place_adversary(a1, 2, 2)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (2, 1)), True)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (2, 3)), True)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (1, 2)), True)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (3, 2)), True)

        # Adversary tries to move more than one tile
        example_level.place_adversary(a1, 1, 1)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (1, 3)), False)

        # Adversary tries to move onto wall tile
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (1, 0)), False)

        # Zombie tries to move onto void tile
        example_level.place_adversary(a1, 2, 3)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (2, 4)), False)

        # Adversary tries to move onto another adversary
        example_level.place_adversary(a2, 3, 3)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (3, 3)), False)

        # Zombie tries to move into hallway
        example_level.place_adversary(a1, 1, 4)
        self.assertEqual(example_rulechecker.is_valid_movement(a1, (1, 5)), False)

        # Ghost tries to move into hallway
        example_level.place_adversary(a2, 6, 7)
        self.assertEqual(example_rulechecker.is_valid_movement(a2, (6, 6)), True)

        # Ghost tries to move onto wall tile
        example_level.place_adversary(a2, 1, 1)
        self.assertEqual(example_rulechecker.is_valid_movement(a2, (1, 0)), True)


if __name__ == '__main__':
    unittest.main()
