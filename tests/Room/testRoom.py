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

def get_traversable_tiles(room, x, y, length, width):
    """
    Gets the traversable tiles from the point to check (x, y)

    Args:
        room (Room): The Room where we are searching for traversable tiles
        x (int): The x-coordinate of the point to check
        y (int): The y-coordinate of the point to check
        length (int): The number of rows
        width (Int): The number of columns
    """
    traversables = []
    # Checking that we are not going out of bounds
    if x > length - 1 or y > width - 1 or x < 0 or y < 0:
        return
    # Checking above
    if not (x - 1 < 0):
        if not room.tiles[x - 1][y].border:
            traversables.append([x - 1, y])
    # Checking left
    if not (y - 1 < 0):
        if not room.tiles[x][y - 1].border:
            traversables.append([x, y - 1])
    # Checking right
    if not (y + 1 > width - 1):
        if not room.tiles[x][y + 1].border:
            traversables.append([x, y + 1])
    # Checking below
    if not (x + 1 > length - 1):
        if not room.tiles[x + 1][y].border:
            traversables.append([x + 1, y])

    return traversables

if __name__ == '__main__':

    input = json.load(sys.stdin)

    room_json = input[0]
    bounds = room_json["bounds"]
    layout = room_json["layout"] 
    starting_point = (room_json["origin"][0], room_json["origin"][1])
    # Accounting for origin by subtracting starting point coordinates from the point to check
    point_to_check = (input[1][0] - starting_point[0], input[1][1] - starting_point[1])
    length = bounds["rows"]
    width = bounds["columns"]

    testing_room = Room(length, width)

    valid_starting_point = False

    traversable_tiles = []

    if point_to_check[0] in range(0, length) and point_to_check[1] in range(0, width):
        valid_starting_point = True
        for i in range(length):
            for j in range(width):
                tile_type = layout[i][j]
                if tile_type == 0:
                    testing_room.tiles[i][j] = Tile(i, j, True, False, False, False)
                elif tile_type == 1:
                    testing_room.tiles[i][j] = Tile(i, j, False, False, False, False)
                else:
                    testing_room.tiles[i][j] = Tile(i, j, False, True, False, False)

        traversable_tiles = get_traversable_tiles(testing_room, point_to_check[0], point_to_check[1], length, width)

        # Accounting for origin by adding starting point coordinates back into tile positions
        for coord in traversable_tiles:
            coord[0] += starting_point[0]
            coord[1] += starting_point[1]

    success_message = ["Success: Traversable points from ", list(point_to_check), " in room at ", list(starting_point), " are ", traversable_tiles]
    failure_message = ["Failure: Point ", list(point_to_check), " is not in room at ", list(starting_point)]

    # Checking if point to check is out of bounds - if it is, we send the failure message
    if valid_starting_point:
        print(json.dumps(success_message))
    else:
        print(json.dumps(failure_message))