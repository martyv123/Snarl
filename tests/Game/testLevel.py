#!/usr/bin/env python3

import sys
import unittest
sys.path.append('../../src/Game')
from level import *
from character import *

# Unit Testing for implementation of levels within a Snarl Game 
# Modules being tested: level.py

class TestRoomGeneration(unittest.TestCase):
    def test_room_borders(self):
        """Testing that the room's borders are set correctly
        """
        example_room = Room(6, 7)
        # Borders should be exits
        for i in range(example_room.length):
            self.assertEqual(example_room.tiles[i][0].border, True)
        for i in range(example_room.width):
            self.assertEqual(example_room.tiles[0][i].border, True)
        for i in range(example_room.width):
            self.assertEqual(example_room.tiles[example_room.length - 1][i].border, True)
        for i in range(example_room.length):
            self.assertEqual(example_room.tiles[i][example_room.width - 1].border, True)

    def test_room_exits(self):
        """Testing that the room's exits are initialized correctly
        """
        example_room = Room(6, 7)
        # Testing initial generation, no exit should be found
        for i in range(example_room.length):
            self.assertEqual(example_room.tiles[i][0].exit, False)
        for i in range(example_room.width):
            self.assertEqual(example_room.tiles[0][i].exit, False)
        for i in range(example_room.width):
            self.assertEqual(example_room.tiles[example_room.length - 1][i].exit, False)
        for i in range(example_room.length):
            self.assertEqual(example_room.tiles[i][example_room.width - 1].exit, False)

    def test_room_keys(self):
        """Testing that the room's tiles are initialized correctly
        """
        example_room = Room(6, 7)
        # Testing initial generation, no exit should be found
        for i in range(example_room.length):
            self.assertEqual(example_room.tiles[i][0].exit, False)
        for i in range(example_room.width):
            self.assertEqual(example_room.tiles[0][i].exit, False)
        for i in range(example_room.width):
            self.assertEqual(example_room.tiles[example_room.length - 1][i].exit, False)
        for i in range(example_room.length):
            self.assertEqual(example_room.tiles[i][example_room.width - 1].exit, False)

    def test_set_exit(self):
        """Testing that we can set a room's exit after generation
        """
        example_room = Room(6, 7)
        
        # Set exit on non border
        self.assertEqual(example_room.set_exit(3, 3), False)
        # Set exit out of bounds
        self.assertEqual(example_room.set_exit(6, 6), False)
        # Set exit on border but unreachable tile
        self.assertEqual(example_room.set_exit(0, 0), False)
        self.assertEqual(example_room.set_exit(0, 6), False)
        self.assertEqual(example_room.set_exit(5, 0), False)
        self.assertEqual(example_room.set_exit(5, 6), False)
        # Set exit on correct tile
        self.assertEqual(example_room.set_exit(5, 5), True)
        self.assertEqual(example_room.set_exit(0, 1), True)

class TestLevelGeneration(unittest.TestCase):
    def test_add_room(self):
        """ Testing that we can add a room to the level
        """
        example_room = Room(4, 5)
        example_level = Level(12, 12)
        example_level.add_room(0, 0, example_room)
        # Checking adding a room that is out of bounds
        self.assertEqual(example_level.add_room(0, 0, Room(20, 20)), False)
        # Checking adding a room that has no walkable tiles
        self.assertEqual(example_level.add_room(0, 0, Room(2, 3)), False)
        # Checking adding an overlapping room
        self.assertEqual(example_level.add_room(0, 0, Room(3, 4)), False)
        # Checking for adding a room that is valid
        self.assertEqual(example_level.rooms[0], example_room)
        
    def test_add_hallway(self):
        room1 = Room(5, 5)
        room2 = Room(4, 4)
        example_level = Level(12, 12)

        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)

        # Adding hallway that is out of bounds
        self.assertEqual(example_level.add_hallway(13, 13, 14, 14, [], room1, room2), False)

        # Adding hallway with entrance and exit that is not a tile
        self.assertEqual(example_level.add_hallway(10, 10, 8, 8, [], room1, room2), False)

        # Adding an overlapping hallway
        self.assertEqual(example_level.add_hallway(1, 3, 3, 4, [], room1, room2), False)

        # Adding a valid hallway
        self.assertEqual(example_level.add_hallway(4, 1, 8, 6, [(8, 1)], room1, room2), True)
        self.assertEqual(len(example_level.hallways), 1)

        # Adding a valid hallway with mutliple waypoints
        self.assertEqual(example_level.add_hallway(1, 4, 6, 7, [(1,9), (3,9), (3,7)], room1, room2), True)
        self.assertEqual(len(example_level.hallways), 2)

    def test_travel(self):
        room1 = Room(5, 5)
        room2 = Room(4, 4)
        example_level = Level(12, 12)

        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)

        # Traveling in multiple directions
        self.assertEqual(example_level.travel(example_level.tiles, 1, 4, 6, 7), False)

        # Traveling with entrance and exit that is not a tile
        self.assertEqual(example_level.travel(example_level.tiles, 10, 10, 8, 8), False)

        # Travel over existing tiles
        self.assertEqual(example_level.travel(example_level.tiles, 1, 3, 3, 4), False)
 
    def test_set_key(self):
        """ Testing that we can set the key for the exit to the level
        """
        example_room1 = Room(4, 5)
        example_room2 = Room(4, 4)
        example_level = Level(12, 12)
        
        example_level.add_room(0, 0, example_room1)
        example_level.add_room(6, 6, example_room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], example_room1, example_room2)

        # Setting the key out of bounds
        self.assertEqual(example_level.set_key(13, 13), False)
        # Setting the key on a border tile
        self.assertEqual(example_level.set_key(3, 4), False)
        # Setting the key on a door
        self.assertEqual(example_level.set_key(1, 4), False)
        # Setting the key on a valid tile
        self.assertEqual(example_level.set_key(2, 3), True)

    def test_set_level_exit(self):
        """ Testing that we can set the level exit in a room after generation
        """
        example_room = Room(4, 5)
        example_room.set_exit(0, 2)
        example_level = Level(12, 12)
        example_level.add_room(0, 0, example_room)
        # Setting the levle exit out of bounds
        self.assertEqual(example_level.set_level_exit(12, 12), False)
        # Setting the level exit on a border tile
        self.assertEqual(example_level.set_level_exit(3, 4), False)
        # Setting the level exit on a door
        self.assertEqual(example_level.set_level_exit(0, 2), False)
        # Setting the level exit on a valid tile
        self.assertEqual(example_level.set_level_exit(2, 3), True)

    def test_get_start(self):
        """ Testing the starting point of a room where we can place Players.
        """
        example_room = Room(4, 5)
        example_level = Level(14, 14)
        example_level.add_room(0, 0, example_room)
        example_level.add_room(6, 6, example_room)
        self.assertEqual(example_level.get_start(), (1, 1))
    
    def test_place_actor(self):
        player1 = Player(1)
        player2 = Player(2)
        player3 = Player(3)
        adversary1 = Adversary(1)
        adversary2 = Adversary(2)
        adversary3 = Adversary(3)
        adversary1.set_type(Type.ZOMBIE)
        adversary2.set_type(Type.ZOMBIE)
        adversary3.set_type(Type.ZOMBIE)

        room1 = Room(5, 5)
        room1.set_exit(1, 4)
        room2 = Room(4, 4)
        room2.set_exit(0, 1)
        example_level = Level(12, 12)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        starting_point = example_level.get_start()
        a_starting_point = example_level.get_adversary_start()

        # Testing placing character at start point
        example_level.place_player(player1, starting_point[0], starting_point[1])
        # Testing placing character at a different point than start point
        example_level.place_player(player2, 2, 2)
        # Testing placing an adversary at start point
        example_level.place_adversary(adversary1, a_starting_point[0], a_starting_point[1])
        # Testing placing adversary at a different point than start point
        example_level.place_adversary(adversary2, 2, 3)

        layout = ["XXXXXXXXXXXX", 
                  "XP../...XXXX", 
                  "X.PZXXX.XXXX",
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+.XXX", 
                  "XXXXXXXoZXXX",
                  "XXXXXXXXXXXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]

        # Testing the Level layout after placing characters
        self.assertEqual(example_level.print_level(), layout)
        # Testing placing a character out of bounds 
        self.assertEqual(example_level.place_player(player1, 12, 12), False)
        # Testing placing a character on a non tile in the Level layout
        self.assertEqual(example_level.place_player(player1, 11, 11), False)
        # Testing placing a character on a border tile
        self.assertEqual(example_level.place_player(player1, 0, 0), False)
        # Testing placing an adversary on the same tile as another adversary
        self.assertEqual(example_level.place_adversary(adversary3, 2, 3), False)
        
        # Testing placing character on same tile as adversary
        example_level.place_player(player2, 2, 3)
        self.assertEqual(player2.active, False)

        layout2 = ["XXXXXXXXXXXX", 
                  "XP../...XXXX", 
                  "X..ZXXX.XXXX",
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+.XXX", 
                  "XXXXXXXoZXXX",
                  "XXXXXXXXXXXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout2)

        # Testing placing a character on a tile with the exit (locked)
        example_level.place_player(player3, 8, 7)
        self.assertEqual(example_level.exit_unlocked, False)

        # Testing placing a character on a tile with the key
        example_level.place_player(player3, 7, 7)
        self.assertEqual(example_level.exit_unlocked, True)

        # Testing placing a character on a tile with the exit (unlocked)
        example_level.place_player(player3, 8, 7)
        self.assertEqual(example_level.level_over, True)

    def test_remove_character(self):
        player1 = Player(1)
        player2 = Player(2)
        adversary1 = Adversary(1)

        room1 = Room(5, 5)
        room2 = Room(4, 4)
        example_level = Level(12, 12)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        starting_point = example_level.get_start()

        # Testing placing character at start point
        example_level.place_player(player1, starting_point[0], starting_point[1])
        # Testing placing character at a different point than start point
        example_level.place_player(player2, 2, 2)
        # Testing placing an adversary
        example_level.place_adversary(adversary1, 2, 3)

        # Removing all placed players
        example_level.remove_character(player1)
        example_level.remove_character(player2)

        layout = ["XXXXXXXXXXXX", 
                  "X.../...XXXX", 
                  "X..AXXX.XXXX", 
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+.XXX", 
                  "XXXXXXXo.XXX", 
                  "XXXXXXXXXXXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]

    def test_print_level_one_room(self):
        """Testing generating a level with one room
        """
        room1 = Room(5, 5)
        example_level = Level(6, 6)
        example_level.add_room(0, 0, room1)

        layout = ['XXXXXX', 'X...XX', 'X...XX', 'X...XX', 'XXXXXX', 'XXXXXX']

        self.assertEqual(example_level.print_level(), layout)

    def test_print_level_two_rooms_one_hallway(self):
        """ Testing generating a level with two rooms and a hallway
        """
        room1 = Room(5, 5)
        room1.set_exit(1, 4)
        room2 = Room(4, 4)
        room2.set_exit(0, 1)
        example_level = Level(12, 12)
        
        example_level.add_room(0, 0, room1)
        example_level.add_room(6, 6, room2)
        example_level.set_key(7, 7)
        example_level.set_level_exit(8, 7)
        example_level.add_hallway(1, 4, 6, 7, [(1,7)], room1, room2)

        layout = ["XXXXXXXXXXXX", 
                  "X.../...XXXX", 
                  "X...XXX.XXXX", 
                  "X...XXX.XXXX", 
                  "XXXXXXX.XXXX",
                  "XXXXXXX.XXXX", 
                  "XXXXXXX/XXXX", 
                  "XXXXXXX+.XXX", 
                  "XXXXXXXo.XXX", 
                  "XXXXXXXXXXXX",
                  "XXXXXXXXXXXX", 
                  "XXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout)

    def test_print_level_three_rooms_two_hallways(self):
        """ Testing generating a level with two rooms and a hallway
        """
        room1 = Room(5, 5)
        room1.set_exit(4, 1)
        room2 = Room(5, 5)
        room2.set_exit(0, 1)
        room2.set_exit(3, 0)
        room3 = Room(5, 5)
        room3.set_exit(0, 1)
        example_level = Level(20, 20)

        example_level.add_room(0, 0, room1)
        example_level.add_room(10, 10, room2)
        example_level.add_room(15, 0, room3)
        example_level.set_key(1, 0)
        example_level.set_level_exit(19, 0)
        example_level.add_hallway(4, 1, 10, 11, [(6, 1), (6, 11)], room1, room2)
        example_level.add_hallway(13, 10, 15, 1, [(13, 1)], room2, room3)

        layout = ["XXXXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X...........XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX/XXXXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "X........./...XXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "XXXXXXXXXXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout)

    def test_get_player_view(self):
        """ Testing generating a player's view within a level with two rooms and a hallway
        """
        # Setting up rooms and doors
        room1 = Room(5, 5)
        room1.set_exit(4, 1)
        room2 = Room(5, 5)
        room2.set_exit(0, 1)
        room2.set_exit(3, 0)
        room3 = Room(5, 5)
        room3.set_exit(0, 1)
        example_level = Level(20, 20)

        # Adding rooms, hallways, keys and exit
        example_level.add_room(0, 0, room1)
        example_level.add_room(10, 10, room2)
        example_level.add_room(15, 0, room3)
        example_level.set_key(1, 0)
        example_level.set_level_exit(19, 0)
        example_level.add_hallway(4, 1, 10, 11, [(6, 1), (6, 11)], room1, room2)
        example_level.add_hallway(13, 10, 15, 1, [(13, 1)], room2, room3)

        # Adding the player
        p1 = Player("p1")
        p1.turn_id = 1
        example_level.place_player(p1, 1, 1)

        layout = ["XXXXXXXXXXXXXXXXXXXX",
                  "X1..XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X...........XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX/XXXXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "X........./...XXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "XXXXXXXXXXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout)

        example_level.place_player(p1, 2, 2)
        layout = ["XXXXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X.1.XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X...........XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX/XXXXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "X........./...XXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "XXXXXXXXXXXXXXXXXXXX"]
        
        self.assertEqual(example_level.print_level(), layout)

        example_level.place_player(p1, 18, 1)
        layout = ["XXXXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X...........XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX/XXXXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "X........./...XXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X1..XXXXXXXXXXXXXXXX",
                  "XXXXXXXXXXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout)

        example_level.place_player(p1, 8, 11)
        layout = ["XXXXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X...........XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX1XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX/XXXXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "X........./...XXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "XXXXXXXXXXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout)

        example_level.place_player(p1, 6, 4)
        layout = ["XXXXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X...1.......XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX.XXXXXXXX",
                  "XXXXXXXXXXX/XXXXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "XXXXXXXXXXX...XXXXXX",
                  "X........./...XXXXXX",
                  "X.XXXXXXXXXXXXXXXXXX",
                  "X/XXXXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "X...XXXXXXXXXXXXXXXX",
                  "XXXXXXXXXXXXXXXXXXXX"]

        self.assertEqual(example_level.print_level(), layout)


if __name__ == '__main__':
    unittest.main()
