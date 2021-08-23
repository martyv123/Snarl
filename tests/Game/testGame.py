#!/usr/bin/env python3

import sys
import unittest
sys.path.append('../../src/Game')
from game import *
from level import *

class TestGame(unittest.TestCase):
    def test_start_game(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        room1 = Room(5, 5)
        example_level = Level(6, 6)
        example_level.add_room(0, 0, room1)
        example_game = Game([p1], [a1], [example_level])
        
        # Testing that the Game state on initialization
        self.assertEqual(example_game.get_game_state(), State.OVER)

    def test_place_players(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        room1 = Room(5, 5)
        example_level = Level(15, 15)
        example_level.add_room(2, 3, room1)
        example_level.add_room(8, 8, room1)
        example_game = Game([p1], [a1], [example_level])

        # Testing that Players are placed in the top-left most room
        example_game.place_players()
        current_level = example_game.current_level
        self.assertEqual(current_level.tiles[3][4].characters[0], p1)
    
    def test_place_adversaries(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        room1 = Room(5, 5)
        example_level = Level(15, 15)
        example_level.add_room(2, 3, room1)
        example_level.add_room(8, 8, room1)
        example_game = Game([p1], [a1], [example_level])

        # Testing that Adversaries are placed in the bottom-right most room
        example_game.place_adversaries()
        current_level = example_game.current_level
        self.assertEqual(current_level.tiles[11][11].characters[0], a1)

    def test_level_up(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        room1 = Room(5, 5)
        example_level = Level(6, 6)
        example_level2 = Level(6, 6)
        example_level.add_room(0, 0, room1)
        example_level2.add_room(0, 0, room1)
        example_game = Game([p1], [a1], [example_level, example_level2])
        
        # Testing that we can't level up unless the level is over
        example_game.level_up()
        self.assertEqual(example_game.current_level, example_game.current_level)

        # Testing that we can level up into a next Level
        example_game.current_level.players_exited.append(p1)
        example_game.current_level.level_over = True
        example_game.level_up()
        self.assertEqual(example_game.current_level, example_level2)

    def test_game_state(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        room1 = Room(5, 5)
        example_level = Level(6, 6)
        example_level.add_room(0, 0, room1)
        example_game = Game([p1], [a1], [example_level])

        # Testing that we can get the Game state
        example_game.end_game()
        self.assertEqual(example_game.get_game_state(), State.OVER)

    def test_render_level(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        a1.set_type(Type.ZOMBIE)
        room1 = Room(5, 5)
        room2 = Room(4, 4)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        example_level2.add_room(4, 5, room1)

        example_game = Game([p1], [a1], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        layout = ["XXXXXXXXXXXX", 
                  "XP../...XXXX", 
                  "X...XXX.XXXX", 
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+.XXX", 
                  "XXXXXXXoZXXX",
                  "XXXXXXXXXXXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]

        self.assertEqual(example_game.render_current_level(), layout)

    def test_initial_game(self):
        p1 = Player("p1")
        a1 = Adversary("p2")
        a1.set_type(Type.ZOMBIE)
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

        example_game = Game([p1], [a1], [example_level, example_level2])
        example_game.place_players()
        example_game.place_adversaries()

        # Testing initial rendering
        layout = ["XXXXXXXXXXXX", 
                  "XP../...XXXX", 
                  "X...XXX.XXXX", 
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+..XX", 
                  "XXXXXXXo..XX", 
                  "XXXXXXX..ZXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]
        self.assertEqual(example_game.render_current_level(), layout)

        # Testing placing character and re-rendering
        example_game.current_level.place_player(p1, 1, 3)
        layout = ["XXXXXXXXXXXX", 
                  "X..P/...XXXX", 
                  "X...XXX.XXXX", 
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+..XX", 
                  "XXXXXXXo..XX", 
                  "XXXXXXX..ZXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]
        self.assertEqual(example_game.render_current_level(), layout)

        # Testing placing adversary and re-rendering
        example_game.current_level.place_adversary(a1, 8, 9)
        layout = ["XXXXXXXXXXXX", 
                  "X..P/...XXXX", 
                  "X...XXX.XXXX", 
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+..XX", 
                  "XXXXXXXo.ZXX",
                  "XXXXXXX...XX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]
        self.assertEqual(example_game.render_current_level(), layout)

    def test_intermediate_game(self):
        p1 = Player("p1")
        a1 = Adversary("a1")
        a1.set_type(Type.ZOMBIE)
        room1 = Room(5, 5)
        room2 = Room(5, 5)
        example_level = Level(12, 12)
        example_level2 = Level(10, 10)
        example_level3 = Level(11, 11)
        example_level4 = Level(11, 11)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 6)
        example_level.set_level_exit(7, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        example_level2.add_room(4, 5, room1)
        example_level2.set_key(7, 6)
        example_level2.set_level_exit(7, 7)

        example_game = Game([p1], [a1], [example_level4, example_level3, example_level, example_level2])

        # Intermediate game - let's start at level 4

        # Level up to level 2
        example_game.current_level.players_exited.append(p1)
        example_game.current_level.level_over = True
        example_game.level_up()
        self.assertEqual(example_game.current_level, example_level3)

        # Level up to level 3
        example_game.current_level.players_exited.append(p1)
        example_game.current_level.level_over = True
        example_game.level_up()
        self.assertEqual(example_game.current_level, example_level)

        # Level up to level 4 - reusing example_level2 so no need to have players exit
        example_game.current_level.players_exited.append(p1)
        example_game.level_up()
        self.assertEqual(example_game.current_level, example_level2)

        layout = ["XXXXXXXXXX", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX",
                  "XXXXXX...X", 
                  "XXXXXX...X", 
                  "XXXXXX+o.X", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX"]
        self.assertEqual(example_game.render_current_level(), layout)

        # Place a player and adversary
        example_game.current_level.place_player(p1, 5, 7)
        example_game.current_level.place_adversary(a1, 7, 8)

        layout = ["XXXXXXXXXX", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX",
                  "XXXXXX.P.X", 
                  "XXXXXX...X", 
                  "XXXXXX+oZX",
                  "XXXXXXXXXX", 
                  "XXXXXXXXXX"]
        self.assertEqual(example_game.render_current_level(), layout)

if __name__ == '__main__':
    unittest.main()