#!/usr/bin/env python3
import sys
import json
import copy
sys.path.append('../../src/Game')
from character import *
from level import *
from game import *
from rulechecker import *
from gameManager import *

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

    # Input: [ (name-list), (level), (natural), (point-list), (actor-move-list-list) ] 
    
    # Get the JSON input from STDIN
    input = json.load(sys.stdin)

    # Pulling the name list
    name_list_json = input[0]
    
    # Pulling the data that we need from the input
    level_json = input[1]
    rooms = level_json["rooms"]
    hallways = level_json["hallways"]
    objects = level_json["objects"]
    key_pos = None
    exit_pos = None

    # Pulling the number of turns
    turns = input[2]

    # Pulling initial player and adversary positions
    initial_positions = input[3]

    # Pulling move list for players and adversaries
    move_list = input[4]
    move_index = 0

    # Creating the testing level
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

    # Creating the game and the game manager
    testing_game = Game([], [], [testing_level])
    testing_game_manager = GameManager(testing_game)

    # Start accepting players into the game
    for name in name_list_json:
        new_player = Player(name)
        testing_game_manager.accept_player(new_player)

    # Determine number of adversaries and create them
    num_adversaries = len(initial_positions) - len(name_list_json)
    for i in range(num_adversaries):
        new_adversary = Adversary(str(i))
        testing_game_manager.accept_adversary(new_adversary)

    # Start the game once players and adversaries have joined
    testing_game_manager.start_game()

    # Split up the positions for players and adversaries
    player_positions = initial_positions[0:len(name_list_json)]
    adversary_positions = initial_positions[len(name_list_json):]

    # Place players
    starting_point = testing_level.get_start()
    for index, position in enumerate(player_positions):
        testing_level.place_player(testing_game.players[index], position[0], position[1])

    # Place adversaries
    starting_point = testing_level.get_adversary_start()
    for index, position in enumerate(adversary_positions):
        testing_level.place_adversary(testing_game.adversaries[index], position[0], position[1])

    manager_trace = []      # one of: [(name), (player-update)], [(name), (actor-move), (result)]

    # Adding first update to manager_trace (this is after adding players to game and initial posns)
    for player in testing_game.players:
        tile_layout = testing_level.get_tile_and_actor_lists(player)[0]
        actor_position_list = testing_level.get_tile_and_actor_lists(player)[1]
        object_list = testing_level.get_tile_and_actor_lists(player)[2]

        player_update = {"type": "player-update",
                         "layout": tile_layout,
                         "position": [player.x_pos, player.y_pos],
                         "objects": object_list,
                         "actors": actor_position_list}
        manager_trace.append([player.id, player_update])  

    
    # Assign moves used per player. This is how we'll keep track of who has moves left.
    moves_used = {}
    for player in testing_game.players:
        moves_used[player.id] = 0

    stop = False
    turns_taken = 0
    # Go through moves until the level is over
    while not testing_game.is_end_of_level():
        # If the maximum number of turns has been reached, go to output message
        if turns_taken == turns:
            break
        else:
            # There are still turns left to play, go through player moves
            players_active = [player for player in testing_game.players if player not in testing_level.players_exited]
            for player in players_active:
                moves = move_list[player.turn_id - 1] 
                while moves_used[player.id] < len(moves):
                    # Go through players moves until valid move is found
                    # If there are no moves left, break out of loop
                    posn = moves[moves_used[player.id]]["to"]
                    # [(name), (actor-move), (result)]
                    key_already_found = copy.deepcopy(testing_level.exit_unlocked)
                    result = None
                    if not posn:
                        posn = (player.x_pos, player.y_pos)
                        actor_move = {"type": "move", "to": None}
                    else:
                        actor_move = {"type": "move", "to": [posn[0], posn[1]]}
                    if (testing_game_manager.accept_movement(posn, player)):
                        # Move was successful, move on to next player
                        moves_used[player.id] += 1
                        if key_already_found != testing_level.exit_unlocked:
                            # Player has picked up key after movement
                            result = "Key"
                        else:
                            if player in testing_level.players_exited and player.active:
                                result = "Exit"
                            elif player in testing_level.players_exited and not player.active:
                                result = "Eject"
                            else:
                                result = "OK"
                        manager_trace.append([player.id, actor_move, result])

                        players_active = [player for player in testing_game.players if player not in testing_level.players_exited]

                        # Issue update to each player still in the game
                        for player in players_active:
                            tile_layout = testing_level.get_tile_and_actor_lists(player)[0]
                            actor_position_list = testing_level.get_tile_and_actor_lists(player)[1]
                            object_list = testing_level.get_tile_and_actor_lists(player)[2]

                            player_update = {"type": "player-update",
                                            "layout": tile_layout,
                                            "position": [player.x_pos, player.y_pos],
                                            "objects": object_list,
                                            "actors": actor_position_list}  
                            manager_trace.append([player.id, player_update])

                        # Continue on to next player after successful move and change player turn       
                        # testing_game_manager.change_player_turn()    
                        break
                    else:
                        # Move was not successful, try next move in move list
                        moves_used[player.id] += 1
                        result = "Invalid"
                        manager_trace.append([player.id, actor_move, result])

                        # Move was not successful, we continue trying until we find a successful move 
                
                # If move input stream for a player is exhausted, and there are still turns
                # to play, break and print result
                if moves_used[player.id] == len(moves) and turns_taken < turns - 1:
                    stop = True
                    break

            # Breaking out of main while loop here because at least one player has no move moves
            # while there are still turns to player    
            if stop == True:
                break
            
            # Go through adversary moves (stationary)
            for adversary in testing_game.adversaries:
                curr_posn = (adversary.x_pos, adversary.y_pos)
                testing_game_manager.accept_movement(curr_posn, adversary)

            # Increment the number of turns taken
            turns_taken += 1

    # Creating state output 

    player_actor_list = []
    adversary_actor_list = []

    # Get the player actor-position-list
    for player in testing_game.players:
        if player not in testing_game.current_level.players_exited:
            player_actor_list.append({"type": "player",
                                    "name": player.id,
                                    "position": [player.x_pos, player.y_pos]})

    # Get the adversary actor-position-list
    for adversary in testing_game.adversaries:
        adversary_actor_list.append({"type": "adversary",
                                     "name": adversary.id,
                                     "position": [adversary.x_pos, adversary.y_pos]})

    state = {"type": "state",
             "level": level_json,
             "players": player_actor_list,
             "adversaries": adversary_actor_list,
             "exit-locked": not testing_level.exit_unlocked}

    # Remove key object from level_json if exit is unlocked
    final_objects = []
    if testing_level.exit_unlocked:
        for obj in state["level"]["objects"]:
            if obj["type"] == "key":
                continue
            elif obj["type"] == "exit":
                final_objects.append(obj)
        state["level"]["objects"] = final_objects


    # Outputting results here
    print(json.dumps([state, manager_trace]))