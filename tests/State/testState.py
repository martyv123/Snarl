#!/usr/bin/env python3

import sys
import json
sys.path.append('Snarl/src/Game')
from level import *
from game import *
from character import *

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


if __name__ == '__main__':

    # Get the JSON input from STDIN
    input = json.load(sys.stdin)

    # Pulling the data that we need from the input
    state = input[0]
    name = input[1]
    point = input[2]

    level_json = state["level"]
    players_json = state["players"]
    adversaries_json = state["adversaries"]
    exit_locked = state["exit-locked"]

    rooms = level_json["rooms"]
    hallways = level_json["hallways"]
    objects = level_json["objects"]

    key_pos = None
    exit_pos = None

    if len(objects) == 2:
        key_pos = objects[0]["position"]
        exit_pos = objects[1]["position"]
    else:
        exit_pos = objects[0]["position"]

    point_to_check = (input[1][0], input[1][1])

    # Creating the testing level
    testing_level = Level(50, 50)
    
    # Adding rooms to our level
    add_rooms(testing_level, rooms)
    
    # Adding hallways to our level
    add_hallways(testing_level, hallways)

    # Set the key and exit for the level
    if key_pos:
        testing_level.set_key(key_pos[0], key_pos[1])
        testing_level.set_level_exit(exit_pos[0], exit_pos[1])
    else:
        testing_level.exit_unlocked = True
        testing_level.set_level_exit(exit_pos[0], exit_pos[1])

    # Create Testing Game State and Game Manager
    testing_game = Game([], [], [testing_level])
    testing_game_manager = GameManager(testing_game)

    # Save player being moved
    testing_player = None

    # Create players and move them to location
    for player in players_json:
        new_player = Player(player["name"])
        testing_game_manager.accept_player(new_player)
        position = (player["position"][0], player["position"][1])
        testing_level.place_player(new_player, position[0], position[1])
        if name == player["name"]:
            testing_player = new_player

    # Create adversaries and move them to location
    for adversary in adversaries_json:
        new_adversary = Adversary(adversary["name"])
        testing_game_manager.accept_adversary(new_adversary)
        position = (adversary["position"][0], adversary["position"][1])
        testing_level.place_adversary(new_adversary, position[0], position[1])


    # Result state and possible output messages
    result_state = state 
    success_no_interaction = ["Success", result_state]
    success_ejected = ["Success", "Player ", name, " was ejected.", result_state]
    success_exited = ["Success", "Player ", name, " exited.", result_state]
    failure_no_player = ["Failure", "Player ", name, " is not a part of the game."]
    failure_not_traversable = ["Failure", "The destination position ", point, " is invalid."]

    # Test result
    if testing_player:
        point_tile = testing_level.tiles[point[0]][point[1]]
        placement_result = testing_level.place_player(testing_player, point[0], point[1])
        if placement_result:
            if testing_level.level_over:
                final_players = []
                for player in state["players"]:
                    if player["name"] != name:
                        final_players.append(player)
                        result_state["players"] = final_players
                print(json.dumps(success_exited))
            elif testing_player.active:
                for player in state["players"]:
                    if player["name"] == name:
                        player["position"] = [testing_player.x_pos, testing_player.y_pos]
                if testing_level.exit_unlocked:
                    result_state["exit-locked"] = False
                    result_state["level"]["objects"] = [ {"type": "exit", "position": exit_pos} ]
                else:
                    state["exit-locked"] = True
                print(json.dumps(success_no_interaction))
            else:
                final_players = []
                for player in state["players"]:
                    if player["name"] != name:
                        final_players.append(player)
                        result_state["players"] = final_players
                print(json.dumps(success_ejected))
        else:
            print(json.dumps(failure_not_traversable))
    else:
        print(json.dumps(failure_no_player))