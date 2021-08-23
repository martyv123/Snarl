#!/usr/bin/env python3

import sys
import json
sys.path.append('../../src/Game')
from level import *

# Input comes in the form of [(room), (point)]

# Room:
#   { "type" : "room",
#     "origin" : (point),
#     "bounds" : (boundary-data),
#     "layout" : (tile-layout)
#    }

# Boundary:
#    { "rows" : Integer,
#      "columns" : Integer
#    } 

# Tile Layout:
#   [[Integer]] - where 0 = wall, 1 = traversable, 2 = door

# Point:
#    [Integer, Integer]

# The input JSON is of the following format

# [(level), (point)]
# where the following data definitions apply.

# A (level) is a JSON object with the following shape:

# { 
#   "rooms": (room-list),
#   "hallways": (hall-list),
#   "objects": [ { "type": "key", "position": (point) }, 
#                { "type": "exit", "position": (point) } ]
# }

# A (room-list) is a JSON array of (room) as defined in Milestone 3
# A (hall-list) is a JSON array of (hall)

# A (hall) is a JSON object with the following shape:

# { 
#   "from": (point),
#   "to": (point),
#   "waypoints": (point-list)
# }
# A (point) and (point-list) are as defined in Milestone 3.

# For this task, assume that the given level is valid and that it always contains exactly one key and one exit object.

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

def check_traversable(level, point_to_check):
    """
    Checks if the point-to-check tile is traversable.

    Args:
        level (Level): The level to check in if the tile is traversable.
        point_to_check (int, int): The (x, y) coordinate of the tile.

    Returns:
        bool: Whether the tile is traversable.
    """
    try:
        if isinstance(level.tiles[point_to_check[0]][point_to_check[1]], Tile) and not level.tiles[point_to_check[0]][point_to_check[1]].border:
            return True
        else:
            return False
    except:
        return False

def check_object(level, point_to_check):
    """
    Checks if the point-to-check tile contains an object.

    Args:
        level (Level): The level to check in if the tile holds an object.
        point_to_check (int, int): The (x, y) coordinate of the tile

    Returns:
        bool: Whether the tile contains an object.
    """
    obj = None
    try:
        tile = level.tiles[point_to_check[0]][point_to_check[1]]
        if isinstance(tile, Tile):
            if tile.key:
                obj = "key"
            elif tile.level_exit or tile.exit:
                obj = "exit"
    except:
        tile = None

    return obj

def check_location_and_reachable(level, point_to_check, reachable):
    """
    Checks where the point-to-check tile resides and the reachable rooms

    Args:
        level (Level): The level to check in where the tile resides and the reachables.
        point_to_check (int, int): The (x, y) coordinate of the tile.
        reachable ([Room]): The list of rooms reachable from the tile.

    Returns:
        str: The location of the room.
    """
    type_ = "void"

    try:
        tile = level.tiles[point_to_check[0]][point_to_check[1]]
    except:
        tile = None

    if isinstance(tile, Tile):
        if tile.in_room:
            type_ = "room"
            for room in testing_level.rooms:
                for t in room.tiles:
                    for a in t:
                        if a.x_pos == point_to_check[0] and a.y_pos == point_to_check[1]:
                            for hallway in (testing_level.hallways):
                                c1 = hallway.connecting_rooms[0]
                                c1_coords = [c1.origin_x, c1.origin_y]
                                c2 = hallway.connecting_rooms[1]
                                c2_coords = [c2.origin_x, c2.origin_y]
                                # print("room coords")
                                # print(c1_coords)
                                # print(c2_coords)
                                if room == c1 and c2_coords not in reachable:
                                    # print("appending [1]")
                                    reachable.append(c2_coords)
                                if room == c2 and c1_coords not in reachable:
                                    # print("appending [0]")
                                    reachable.append(c1_coords)
        elif tile.in_hallway:
            type_ = "hallway"
            for hallway in testing_level.hallways:
                for t in hallway.tiles:
                    if t.x_pos == point_to_check[0] and t.y_pos == point_to_check[1]:
                        for r in hallway.connecting_rooms:
                            r_coords = [r.origin_x, r.origin_y]
                            # print("hallway coords")
                            # print(r_coords)
                            if r_coords not in reachable:
                                reachable.append(r_coords) 

    return type_

if __name__ == '__main__':

    # Get the JSON input from STDIN
    input = json.load(sys.stdin)

    # Pulling the data that we need from the input
    level_json = input[0]
    rooms = level_json["rooms"]
    hallways = level_json["hallways"]
    objects = level_json["objects"]
    key_pos = objects[0]["position"]
    exit_pos = objects[1]["position"]
    point_to_check = (input[1][0], input[1][1])

    # Creating the testing level
    testing_level = Level(50, 50)
    
    # Adding rooms to our level
    add_rooms(testing_level, rooms)
    
    # Adding hallways to our level
    add_hallways(testing_level, hallways)

    # Set the key and exit for the level
    testing_level.set_key(key_pos[0], key_pos[1])
    testing_level.set_level_exit(exit_pos[0], exit_pos[1])

    # Testing if the point-to-check is traversable
    traversable = check_traversable(testing_level, point_to_check)

    # Testing if the point-to-check is an object
    obj = check_object(testing_level, point_to_check)
    
    # Testing where the point-to-check resides and the reachable rooms and hallways
    reachable = []
    type_ = check_location_and_reachable(testing_level, point_to_check, reachable)

    # layout = testing_level.print_level()
    # for row in layout:
    #     print(row)

    # Test result
    output_message = {
            "traversable": traversable,
            "object": obj,
            "type": type_,
            "reachable": reachable
            }

    # Printing output JSON string 
    print(json.dumps(output_message))