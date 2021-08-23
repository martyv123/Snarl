#!/usr/bin/env python3

import sys
import argparse
import json
import math
import random

sys.path.append('../src/Player')
sys.path.append('../src/Game')
sys.path.append('../src/Common')

from character import *
from level import *
from game import *
from gameManager import *
from localPlayer import *


def test_args():
    # Testing that the args work
    print("Printing args:")
    if args.levels:
        print("\nThis is the levels file: " + str(args.levels))

    if args.players:
        print("\nThis is the number of players: " + str(args.players))

    if args.start:
        print("\nThis is the level to start on: " + str(args.start))

    if args.observe:
        print("\nThe user has indicated they want to observe the game.")


def init_tiles(room, layout):
    """
    Initializes the tiles for the room.

    Args:
        room (Room): The room to initialize tiles for.
        layout ([JSON]): The layout for the room.
    """
    for i in range(room.length):
        for j in range(room.width):
            tile_type = layout[i][j]
            if tile_type == 0:
                new_tile = Tile(i, j, True, False, False, False)
                new_tile.in_room = True
                room.tiles[i][j] = new_tile
            elif tile_type == 1:
                new_tile = Tile(i, j, False, False, False, False)
                new_tile.in_room = True
                room.tiles[i][j] = new_tile
            else:
                new_tile = Tile(i, j, False, True, False, False)
                new_tile.in_room = True
                room.tiles[i][j] = new_tile


def add_rooms(level, rooms):
    """
    Adds the JSON input of rooms to the instantiated level.

    Args:
        level ([type]): The instantiated level.
        rooms ([JSON]): The JSON input of rooms.
    """
    for room in rooms:
        origin = room["origin"]
        bounds = room["bounds"]
        layout = room["layout"]
        new_room = Room(bounds["rows"], bounds["columns"])
        init_tiles(new_room, layout)
        level.add_room(origin[0], origin[1], new_room)


def add_hallways(level, hallways):
    """
    Adds hallways to the level.

    Args:
        level (Level): The level to add hallways to.
        hallways ([JSON]): The JSON input of hallways.
    """
    for hallway in hallways:
        from_ = hallway["from"]
        to = hallway["to"]
        waypoints = hallway["waypoints"]
        waypoints_t = []
        for w in waypoints:
            waypoints_t.append((w[0], w[1]))
        room1 = None
        room2 = None
        for room in level.rooms:
            for t in room.tiles:
                for a in t:
                    if a.x_pos == from_[0] and a.y_pos == from_[1]:
                        room1 = room

        for room in level.rooms:
            for t in room.tiles:
                for a in t:
                    if a.x_pos == to[0] and a.y_pos == to[1]:
                        room2 = room
        level.add_hallway(from_[0], from_[1], to[0], to[1], waypoints_t, room1, room2)


def create_zombies(number):
    """
    Create the given number of zombies.

    Args:
        number: The number of zombies.

    Returns:
        [Adversary]: A list of the zombie adversaries.
    """
    zombies = []
    for i in range(number):
        id = "Z" + str(i)
        new_zombie = Adversary(id)
        new_zombie.set_type(Type.ZOMBIE)
        zombies.append(new_zombie)

    return zombies


def create_ghosts(number):
    """
    Create the given number of ghosts.

    Args:
        number: The number of ghosts.

    Returns:
        [Adversary]: A list of the ghosts adversaries.
    """
    ghosts = []
    for i in range(number):
        id = "G" + str(i)
        new_ghost = Adversary(id)
        new_ghost.set_type(Type.GHOST)
        ghosts.append(new_ghost)

    return ghosts


def get_random_starting_position(level):
    """
    Pick a random starting position for a traversable tile in a room.
    The tile cannot be occupied by another actor or object.

    Args:
        level (Level): The level to find a random starting position for.

    Returns:
        (int, int): The starting position
    """
    length = level.length
    width = level.width

    for i in range(length):
        for j in range(width):
            rand_x_pos = random.randint(0, length - 1)
            rand_y_pos = random.randint(0, width - 1)
            dst_tile = level.tiles[rand_x_pos][rand_y_pos]
            if isinstance(dst_tile, Tile) and dst_tile.in_room and not dst_tile.border:
                if not dst_tile.level_exit and not dst_tile.key and not dst_tile.characters:
                    return (rand_x_pos, rand_y_pos)


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description="Welcome to Snarl!")

    # Adding CL arguments
    parser.add_argument('--levels', help="FILENAME containing JSON level specifications.",
                        default='snarl.levels')
    parser.add_argument('--players', type=int, help="The number of players (1-4).", default=1)
    parser.add_argument('--start', type=int, help="The level number to start from.", default=1)
    parser.add_argument('--observe', help="Switch to an observer view.", action='store_true')

    # Creating the args list
    args = parser.parse_args()

    # Testing args
    # test_args()

    # Pulling information from args
    levels_file = args.levels
    num_players = args.players
    starting_level = args.start
    observer_view = True if args.observe else False

    num_levels = 0
    json_levels = []

    # Now pulling information from JSON levels file
    # print("We are reading from this file: " + str(levels_file))
    with open (levels_file, mode='r') as input_file:
        curr_json_level = ""
        counter = 0
        for line in input_file.readlines():
            # print(line)
            if counter == 0:
                num_levels = int(line.strip())
            else:
                if line == "\n" and counter != 1:
                    json_levels.append(curr_json_level.strip('\n'))
                    curr_json_level = ""
                else:
                    curr_json_level += line
            counter += 1

        # Append the last JSON level to the json_levels list
        json_levels.append(curr_json_level.strip('\n'))

    # Convert str json levels into json objects
    parsed_levels = []
    for json_level in json_levels:
        parsed_levels.append(json.loads(json_level))

    # Create our rooms, hallways, and level to add to the game
    levels = []
    for index, json_level in enumerate(parsed_levels):
        if index < starting_level - 1:
            continue
        else:
            rooms = json_level["rooms"]
            hallways = json_level["hallways"]
            objects = json_level["objects"]
            key_pos = None
            exit_pos = None

            testing_level = Level(20, 20)

            # Adding rooms to our level
            add_rooms(testing_level, rooms)

            # Adding hallways to our level
            add_hallways(testing_level, hallways)

            # Set the key and exit for the level
            for obj in objects:
                if obj["type"] == "exit":
                    exit_pos = obj["position"]
                    testing_level.set_level_exit(exit_pos[0], exit_pos[1])
                elif obj["type"] == "key":
                    key_pos = obj["position"]
                    testing_level.set_key(key_pos[0], key_pos[1])

            levels.append(testing_level)


    # Create the game and the game manager
    demo_game = Game([], [], levels)
    demo_game_manager = GameManager(demo_game)

    # Limiting implementation to 1 player as stated in assignment description
    # Register the player(s)
    print("\nWelcome to Snarl!")
    print("Please choose a unique name to register for the game.")
    player_name = input("Enter your name below: \n")
    print("\n\nGAME")

    player_1 = Player(player_name)

    # Creating the client that controls the player
    client = Client(player_1)

    # Accept the player into the game via the game manager
    demo_game_manager.accept_player(player_1)

    # Add the game manager to the client
    client.set_game_manager(demo_game_manager)

    # Create the initial number of adversaries
    # Number of zombies = math.floor(l / 2)  + 1 where l is the level number
    # Number of ghosts = math.floor((l - 1) / 2) where l is the level number
    num_zombies = math.floor(starting_level / 2) + 1
    num_ghosts = math.floor((starting_level - 1) / 2)

    zombies = create_zombies(num_zombies)
    ghosts = create_ghosts(num_ghosts)
    adversaries = zombies + ghosts

    # Accept the adversaries into the game via the game manager
    for adversary in adversaries:
        demo_game_manager.accept_adversary(adversary)

    # Initially place the players and adversaries in random locations
    # Must be on a traversable room tile, not on another player/adversary, and not on a key/exit
    player_starting_pos = get_random_starting_position(demo_game_manager.game.current_level)
    demo_game_manager.game.current_level.place_player(player_1,
                                                      player_starting_pos[0], player_starting_pos[1])

    for adversary in adversaries:
        adversary_starting_pos = get_random_starting_position(demo_game_manager.game.current_level)
        demo_game_manager.game.current_level.place_adversary(adversary,
                                                          adversary_starting_pos[0],
                                                          adversary_starting_pos[1])

    # Start the game at the requested level (current level)
    demo_game_manager.start_game()

    game_won = True
    exited = 0
    keys = 0
    curr_level_key_found = 0

    # Looping through actions for the game
    while demo_game_manager.game.state == State.IN_PROGRESS:
        # The current level
        curr_level = demo_game_manager.game.current_level
        # Player's turn
        if demo_game_manager.whose_turn == Turn.PLAYER:
            # Print the player's view or the observer's view
            if observer_view:
                print("<===============player================>")
                for row in curr_level.print_level():
                    print(row)
                print("<===============player================>\n")
            else:
                print("<===============player================>")
                for row in demo_game_manager.send_player_view(player_1):
                    print(row)
                print("<===============player================>\n")
            demo_game_manager.send_player_turn_notification(player_1)
            successful_move = False
            while not successful_move:
                player_move_x_coord = input("Enter the x_coordinate of your move below: \n")
                player_move_y_coord = input("Enter the y_coordinate of your move below: \n")
                try:
                    x_coord = int(player_move_x_coord)
                    y_coord = int(player_move_y_coord)
                    if demo_game_manager.accept_movement((x_coord, y_coord), player_1):
                        successful_move = True
                    else:
                        print("That move was not successful. Please try again.\n")
                        continue
                except:
                    if not player_1.active:
                        demo_game_manager.end_game()
                        game_won = False
                        successful_move = True
                    else:
                        print("Please enter integers for your move coordinates.\n")
                    continue
            if curr_level.exit_unlocked and curr_level_key_found == 0:
                keys += 1
                curr_level_key_found += 1
        # Adversaries' turn
        if demo_game_manager.whose_turn == Turn.ADVERSARY:
            for adversary in demo_game_manager.game.adversaries:
                successful_move = False
                while not successful_move:
                    successful_move = adversary.take_turn()
                if observer_view:
                    print("<=============adversary===============>")
                    for row in curr_level.print_level():
                        print(row)
                    print("<=============adversary===============>\n")
                else:
                    print("<=============adversary===============>")
                    for row in demo_game_manager.send_player_view(player_1):
                        print(row)
                    print("<=============adversary===============>\n")

        # Handle leveling up if player successfully finds exit
        if player_1.active and player_1 in curr_level.players_exited:
            demo_game_manager.game.level_up()
            exited += 1
            curr_level_key_found = 0
            demo_game_manager.game.adversaries = []

            # Number of zombies = math.floor(l / 2)  + 1 where l is the level number
            # Number of ghosts = math.floor((l - 1) / 2) where l is the level number
            num_zombies = math.floor(starting_level / 2) + 1
            num_ghosts = math.floor((starting_level - 1) / 2)

            zombies = create_zombies(num_zombies)
            ghosts = create_ghosts(num_ghosts)
            adversaries = zombies + ghosts

            # Accept the adversaries into the game via the game manager
            for adversary in adversaries:
                demo_game_manager.accept_adversary(adversary)

            # Initially place the players and adversaries in random locations
            # Must be on a traversable room tile, not on another player/adversary, and not on a key/exit
            player_starting_pos = get_random_starting_position(demo_game_manager.game.current_level)
            demo_game_manager.game.current_level.place_player(player_1,
                                                              player_starting_pos[0], player_starting_pos[1])

            for adversary in adversaries:
                adversary_starting_pos = get_random_starting_position(demo_game_manager.game.current_level)
                demo_game_manager.game.current_level.place_adversary(adversary,
                                                                     adversary_starting_pos[0],
                                                                     adversary_starting_pos[1])

            print("You are now on the next level.")

        # Handle ending the game if player gets eliminated
        if not player_1.active:
            demo_game_manager.end_game()
            game_won = False

    if game_won:
        print("You won the game.\n")
    else:
        print("You lost the game.\n")
    print("You successfully found " + str(keys) + " keys.\n")
    print("You successfully exited " + str(exited) + " times.\n")
