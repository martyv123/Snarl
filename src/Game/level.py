#!/usr/bin/env python3

import copy
import random
from character import *

class Tile:
    def __init__(self, x_pos, y_pos, border, exit, level_exit, key):
        """
        Represents a tile in a room. This tile may have a key or exit.

        Args:
            x_pos (int): The x-coordinate of the tile
            y_pos (int): The y-coordinate of the tile
            border (bool): Whether the tile is a border
            exit (bool): Whether the tile is an exit
            key (bool): Whether the tile contains a key
            characters ([Character]): The Characters present on the Tile
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.border = border
        self.exit = exit
        self.key = key
        self.level_exit = level_exit
        self.characters = []
        self.in_hallway = False
        self.in_room = False

class Room:
    def __init__(self, length, width):
        """
        Represents a room inside a level.
        Examples of rooms can be found in Game/level_tests.py in the TestRoomGeneration Class

        Args:
            length (int): The length of the room
            width (int): The width of the room
        """
        self.length = length
        self.width = width
        self.level_exit = None
        self.tiles = [[0 for x in range(width)] for y in range(length)]
        self.origin_x = None
        self.origin_y = None
        self.generate_room()
        
    def generate_room(self):
        """ Generates the room by creating a length by width grid of tiles.
        """
        for i in range(self.length):
            for j in range(self.width):
                border = False
                if i == 0 or j == 0 or i == self.length - 1 or j == self.width - 1:
                    border = True
                this_tile = Tile(i, j, border, False, False, False)
                this_tile.in_room = True
                self.tiles[i][j] = this_tile
    
    def set_exit(self, x_pos, y_pos):
        """
        Sets an exit for a room which must be on a border tile. This will lead into a hallway.

        Args:
            x_pos (int): The x-coordinate of the exit
            y_pos ([type]): The y-coordinate of the exit

        Returns:
            (bool): Whether setting the exit at the specified location succeeded
        """
        if x_pos < self.length and y_pos < self.width and self.tiles[x_pos][y_pos].border:
            # Check four corners, exit should be on a reachable border tile
            if (x_pos == 0 and y_pos == 0) or (x_pos == 0 and y_pos == self.width - 1):
                return False
            if (x_pos == self.length - 1 and y_pos == 0) or (x_pos == self.length - 1 and y_pos == self.width - 1):
                return False
                
            self.tiles[x_pos][y_pos].exit = True
            return True
        else:
            return False

class Hallway:
    def __init__(self, tiles, waypoints, room1, room2):
        """
        Represents a hallway that connects two rooms.

        Args:
            tiles ([Tile]): The hallway's tiles
            waypoints ([(int, int)]): The hallway's waypoints represented as a tuple of x/y coords
            room1 (Room): The first room that the hallway is connected to
            room2 (Room): The second room that the hallway is connected to
        """
        self.tiles = tiles
        self.waypoints = waypoints
        self.connecting_rooms = [room1, room2]       

class Level:
    def __init__(self, length, width):
        """
        A dungeon level. It is composed of Rooms and Hallways.

        Examples of levels can be found in level_tests.py in TestLevelGeneration
        Args:
            length (int): The tile length of the level
            width (int): The tile width of the level
        """
        self.length = length
        self.width = width
        self.rooms = []
        self.hallways = []
        self.tiles = [[0 for x in range(width)] for y in range(length)]
        self.key = None
        self.level_exit = None
        self.exit_unlocked = False
        self.level_over = False
        self.players_exited = []
        self.start = (self.length, self.width)
        self.adversary_start = (0, 0)
        self.interaction_log = ""
        self.end_level_message = { "type": "end-level",
                                   "key": "",
                                   "exits": [],
                                   "ejects": []}

    def add_room(self, x_pos, y_pos, room):
        """
        Adds a room to the level if it does not overlap with any other rooms/hallways.

        Args:
            x_pos (int): The starting x-coordinate of the room
            y_cos (int): The starting y-coordinate of the room
            room (Room): The room to be added
        
        Returns:
            result (bool): Whether the room was successfully added
        """
        # Checking that the room can fit in the level
        if room.length + x_pos > self.length or room.width + y_pos > self.width:
            return False

        # Checking that the room must have at least one walkable tile
        if room.length < 3 or room.width < 3:
            return False
        
        new_tiles = copy.deepcopy(self.tiles)
        for i in range(room.length):
            for j in range(room.width):
                if isinstance(new_tiles[x_pos + i][y_pos + j], Tile):
                    return False
                new_tiles[x_pos + i][y_pos + j] = room.tiles[i][j]
                room.tiles[i][j].x_pos = x_pos + i
                room.tiles[i][j].y_pos = y_pos + j

        if x_pos < self.start[0] and y_pos < self.start[1]:
            self.start = (x_pos + 1, y_pos + 1)

        if x_pos + room.length > self.adversary_start[0] and y_pos + room.width > self.adversary_start[1]:
            self.adversary_start = (x_pos + room.length - 2, y_pos + room.width - 2)

        self.tiles = copy.deepcopy(new_tiles)
        room.origin_x = x_pos
        room.origin_y = y_pos
        self.rooms.append(room)
        

        return True

    def add_hallway(self, entrance_x, entrance_y, end_x, end_y, waypoints, room1, room2):
        """
        Add a hallway that connects two rooms.

        Args:
            entrance_x (int): The entrance tile's x-coordinate
            entrance_y (int): The entrance tile's y-coordinate
            end_x (int): The end tile's x-coordinate
            end_y (int): The end tile's y-coordinate
            waypoints ([(int, int)]): The hallway's waypoints
            room1 (Room): The first room that the hallway is connected to
            room2 (Room): The second room that the hallway is connected to

        Returns:
            bool: Whether the hallway was added
        """
        new_tiles = copy.deepcopy(self.tiles)
        # Checking for out of bounds entrances and exits
        if entrance_x > self.length or entrance_y > self.width:
            return False
        # Checking whether or not the entrance and exit is a tile
        if not isinstance(new_tiles[entrance_x][entrance_y], Tile) or not isinstance(new_tiles[end_x][end_y], Tile):
            return False
        
        # Changing entrance/end tiles to no longer be border tiles and to be exit tiles
        new_tiles[entrance_x][entrance_y].border = False
        new_tiles[entrance_x][entrance_y].exit = True
        new_tiles[end_x][end_y].border = False
        new_tiles[end_x][end_y].exit = True

        curr_x = entrance_x
        curr_y = entrance_y
        hallway = Hallway([], waypoints, room1, room2)
        for w in waypoints:
            try:
                move = self.travel(new_tiles, curr_x, curr_y, w[0], w[1])
                for t in move[1]:
                    hallway.tiles.append(t)
                new_tiles = move[0]
                curr_x = w[0]
                curr_y = w[1]
            except:
                return False
            if isinstance(new_tiles[w[0]][w[1]], Tile):
                return False
            else:
                new_tile = Tile(w[0], w[1], False, False, False, False)
                new_tile.in_hallway = True
                new_tiles[w[0]][w[1]] = new_tile
                hallway.tiles.append(new_tile)
        
        try:
            move = self.travel(new_tiles, curr_x, curr_y, end_x, end_y)
            for t in move[1]:
                hallway.tiles.append(t)
            self.tiles = move[0]
        except:
            return False
        self.hallways.append(hallway)
        return True

    def travel(self, new_tiles, entrance_x, entrance_y, end_x, end_y):
        """
        Creates hallway between rooms and/or waypoints.

        Args:
            new_tiles ([[Tile]]): Current level state
            entrance_x (int): The x-coordinate of the starting point
            entrance_y (int): The y-coordinate of the starting point
            end_x (int): The x-coordinate of the end point
            end_y (int): The y-coordinate of the end point
        """
        x_distance = end_x - entrance_x
        x_direction = "up" if x_distance > 0 else "down"
        y_distance = end_y - entrance_y
        y_direction = "right" if y_distance > 0 else "left"

        # Checking that movement is 1-dimensional
        if x_distance != 0 and y_distance != 0:
            return False

        # Checking for out of bounds entrances and exits
        if entrance_x > self.length or entrance_y > self.width:
            return False

        # Assign the current x/y coordinates
        curr_x = entrance_x
        curr_y = entrance_y

        hallway_tiles = []

        for i in range(abs(y_distance) - 1):
            if y_direction == "left":
                curr_y -= 1
            if y_direction == "right":
                curr_y += 1
            if isinstance(new_tiles[curr_x][curr_y], Tile):
                return False
            hallway_tile = Tile(curr_x, curr_y, False, False, False, False)
            hallway_tile.in_hallway = True
            hallway_tiles.append(hallway_tile)
            new_tiles[curr_x][curr_y] = hallway_tile

        for i in range(abs(x_distance) - 1):
            if x_direction == "down":
                curr_x -= 1
            if x_direction == "up":
                curr_x += 1
            if isinstance(new_tiles[curr_x][curr_y], Tile):
                return False
            hallway_tile = Tile(curr_x, curr_y, False, False, False, False)
            hallway_tile.in_hallway = True
            hallway_tiles.append(hallway_tile)
            new_tiles[curr_x][curr_y] = hallway_tile
        
        return (new_tiles, hallway_tiles)

    def set_key(self, x_pos, y_pos):
        """
        Sets the key for a level in a room

        Args:
            x_pos (int): The x-coordinate of the key
            y_pos (int): They y-coordinate of the key
        """
        # Checking that the coordinates are in bounds
        if x_pos > self.length - 1 or y_pos > self.width - 1:
            return False
        elif isinstance(self.tiles[x_pos][y_pos], Tile) and not self.tiles[x_pos][y_pos].in_hallway:
            if self.tiles[x_pos][y_pos].border or self.tiles[x_pos][y_pos].exit:
                return False
            else:
                self.tiles[x_pos][y_pos].key = True
                self.key = self.tiles[x_pos][y_pos]
                return True
        else:
            return False

    def set_level_exit(self, x_pos, y_pos):
        """
        Sets the exit for a level within a walkable tile

        Args:
            x_pos (int): The x-coordinate of the level exit
            y_pos (int): The y-coordinate of the level exit
        """
        # Checking that the coordinates are in bounds
        if x_pos > self.length - 1 or y_pos > self.width - 1:
            return False
        elif isinstance(self.tiles[x_pos][y_pos], Tile) and not self.tiles[x_pos][y_pos].in_hallway:
            if self.tiles[x_pos][y_pos].border:
                return False
            elif self.tiles[x_pos][y_pos].exit:
                return False
            else:
                self.tiles[x_pos][y_pos].level_exit = True
                self.level_exit = self.tiles[x_pos][y_pos] 
                return True
        else:
            return False

    def place_adversary(self, character, x_pos, y_pos):
        """
        Place the Adversary at the x and y pos of the Level.

        Args:
            x_pos (int): The x-coordinate
            y_pos (int): The y-coordinate

        Return:
            (bool): If the placement was successful
        """
        try:
            curr = self.tiles[x_pos][y_pos]
            if isinstance(curr, Tile):
                if not curr.border:
                    # Not border tile, we are a Zombie
                    for c in curr.characters:
                        if isinstance(c, Player) and c not in self.players_exited:
                            self.eliminate_interaction(c)
                        if isinstance(c, Adversary) and c.id != character.id:
                            return False
                    if character.x_pos and character.y_pos and self.tiles[character.x_pos][character.y_pos].characters:
                        self.tiles[character.x_pos][character.y_pos].characters.remove(character)
                    character.x_pos = x_pos
                    character.y_pos = y_pos
                    curr.characters.append(character)
                else:
                    # Border tile, we are a Ghost
                    # Picking a random tile within a random room
                    for i in range(self.length):
                        for j in range(self.width):
                            rand_x_pos = random.randint(0, self.length - 1)
                            rand_y_pos = random.randint(0, self.width - 1)
                            dst_tile = self.tiles[rand_x_pos][rand_y_pos]
                            if isinstance(dst_tile, Tile) and dst_tile.in_room and not dst_tile.border:
                                for c in dst_tile.characters:
                                    if isinstance(c, Player):
                                        self.eliminate_interaction(c)
                                    if isinstance(c, Adversary) and c.id != character.id:
                                        return False
                                if character.x_pos and character.y_pos and self.tiles[character.x_pos][character.y_pos].characters:
                                    self.tiles[character.x_pos][character.y_pos].characters.remove(character)
                                character.x_pos = x_pos
                                character.y_pos = y_pos
                                dst_tile.characters.append(character)
                return True
            else:
                return False
        except IndexError as e:
            return False

    def place_player(self, character, x_pos, y_pos):
        """
        Place the Character at the x and y pos of the Level.

        Args:
            x_pos (int): The x-coordinate
            y_pos (int): The y-coordinate

        Return:
            (bool): If the placement was successful
        """
        self.interaction_log = ""

        try:
            curr = self.tiles[x_pos][y_pos]
            if isinstance(curr, Tile) and not curr.border:
                for c in curr.characters:
                    if isinstance(c, Adversary):
                        self.eliminate_interaction(character)
                        return False
                    if isinstance(c, Player) and c.id != character.id:
                        return False
                if curr.key:
                    self.key_interaction(character)
                    curr.key = False
                if curr.level_exit:
                    self.exit_interaction(character)               
                if character.x_pos and character.y_pos and self.tiles[character.x_pos][character.y_pos].characters:
                    if character in self.tiles[character.x_pos][character.y_pos].characters:
                        self.tiles[character.x_pos][character.y_pos].characters.remove(character)
                character.x_pos = x_pos
                character.y_pos = y_pos
                curr.characters.append(character)
                return True
            else:
                return False
        except IndexError as e:
            print(e)
            return False

    def key_interaction(self, player):
        """ Key interaction when a Player walks on a tile with a key.

        Args:
            player (Player): The player who found the key.
        """
        self.exit_unlocked = True
        self.interaction_log = str(str(player.id) + " found the key")
        player.keys += 1
        self.end_level_message["key"] = player.id

    def exit_interaction(self, character):
        """ 
        Exit interaction when a Player walks on a tile with the Level exit. 
        Only sets the Level to over if the key has been previously found.

        Args:
            character (Player): The player who exited.
        """
        if self.exit_unlocked:
            self.level_over = True
            self.players_exited.append(character)
            self.interaction_log = str(str(character.id) + " exited")
            character.exits += 1
            character.exited = True
            self.end_level_message["exits"].append(character.id)

            # Remove player from tile
            # self.tiles[character.x_pos][character.y_pos].characters = []
            # character.x_pos = None
            # character.y_pos = None

    def eliminate_interaction(self, character):
        """
        Eliminates a Player from the Game.

        Args:
            character (Player): The player to be eliminated.
        """
        if not self.level_over and not character.exited:
            self.remove_character(character)
            self.players_exited.append(character)
            self.interaction_log =  str(str(character.id) + " was expelled")
            character.ejects += 1
            self.end_level_message["ejects"].append(character.id)

    def remove_character(self, character):
        """
        Remove the Character at the x and y pos of the Level.

        Args:
            character (Character): The Character to be removed
        """
        x_coord = character.x_pos
        y_coord = character.y_pos
        curr = self.tiles[x_coord][y_coord]
        character.active = False
        curr.characters = []

    def get_start(self):
        """ 
        Get this Level's starting point for Players

        Returns:
            (int, int): A tuple of the starting x and y coordinates
        """
        return (self.start[0], self.start[1])

    def get_adversary_start(self):
        """ 
        Get this Level's starting point for Adversaries

        Returns:
            (int, int): A tuple of the starting x and y coordinates
        """
        return (self.adversary_start[0], self.adversary_start[1])

    def print_level(self):
        """ Get ASCII representation of the level

        Returns:
            ([str]): String representation of the level layout
        """
        layout = []
        for i in range (self.length):
            row = ''
            for j in range (self.width):
                try:
                    this_tile = self.tiles[i][j]
                    if this_tile.characters:
                        if isinstance(this_tile.characters[0], Player):
                            if this_tile.characters[0].turn_id:
                                row += str(this_tile.characters[0].turn_id)
                            else:
                                row += 'P'
                        elif isinstance(this_tile.characters[0], Adversary):
                            if this_tile.characters[0].type == Type.ZOMBIE:
                                row += 'Z'
                            elif this_tile.characters[0].type == Type.GHOST:
                                row += 'G'
                    elif this_tile.level_exit:
                        row += 'o'
                    elif this_tile.exit:
                        row += '/'
                    elif this_tile.border:
                        row += 'X'
                    elif this_tile.key:
                        row += '+'
                    else:
                        row += '.'
                except AttributeError as e:
                    # Not a tile, so we can just print some representation
                    row += "X"
            layout.append(row)

        return layout

    def get_player_view(self, player):
        """ Get ASCII representation for a player's view of the level.

        Args:
            player (Player): The player to get the view for.

        Returns:
            (player): The player to generate the view for.
        """
        # Get position information and boundaries of view
        x_pos = player.x_pos
        y_pos = player.y_pos
        x_bounds = (x_pos - 2, x_pos + 2)
        y_bounds = (y_pos - 2, y_pos + 2)

        # Check for invalid bounds, and redetermine the bounds
        if (x_bounds[0] < 0):
            x_bounds = (0, x_bounds[1])
        if (y_bounds[0] < 0):
            y_bounds = (0, y_bounds[1])
        
        if (x_bounds[1] > self.length - 1):
            x_bounds = (x_bounds[0], self.length - 1)
        if (y_bounds[1] > self.width - 1):
            y_bounds = (y_bounds[0], self.width - 1)

        layout = []
        for i in range (x_bounds[0], x_bounds[1] + 1):
            row = ''
            for j in range (y_bounds[0], y_bounds[1] + 1):
                try:
                    this_tile = self.tiles[i][j]
                    if this_tile.characters:
                        if isinstance(this_tile.characters[0], Player):
                            if this_tile.characters[0].turn_id:
                                row += str(this_tile.characters[0].turn_id)
                            else:
                                row += 'P'
                        elif isinstance(this_tile.characters[0], Adversary):
                            if this_tile.characters[0].type == Type.ZOMBIE:
                                row += 'Z'
                            elif this_tile.characters[0].type == Type.GHOST:
                                row += 'G'
                    elif this_tile.level_exit:
                        row += 'o'
                    elif this_tile.exit:
                        row += '/'
                    elif this_tile.border:
                        row += 'X'
                    elif this_tile.key:
                        row += '+'
                    else:
                        row += '.'
                except AttributeError as e:
                    # Not a tile, so we can just print some representation
                    row += "X"
            layout.append(row)

        return layout

    def get_tile_and_actor_lists(self, player):
        """ 
        Get the integer representation of a player's view of the level.
        Get the actor position list.
        Void tiles are padded into the view and represented as 0.

        Args:
            player (Player): The player to get the view for.

        Returns:
            ( [[int]], [JSON] ): A tuple containing the integer representation of a player's view
            and the JSON representation of the actor-position-list.
        """
        # Get position information and boundaries of view
        x_pos = player.x_pos
        y_pos = player.y_pos
        x_bounds = (x_pos - 2, x_pos + 2)
        y_bounds = (y_pos - 2, y_pos + 2)

        tile_layout = []
        actor_position_list = []
        object_list = []
        actor_type = None
        actor_name = None
        actor_posn = None
        
        for i in range (x_bounds[0], x_bounds[1] + 1):
            row = []
            for j in range (y_bounds[0], y_bounds[1] + 1):
                try:
                    this_tile = self.tiles[i][j]
                    if this_tile.characters:
                        if isinstance(this_tile.characters[0], Player) and player.id != this_tile.characters[0].id:
                            actor_type = "player"
                            actor_name = this_tile.characters[0].id
                            actor_posn = (this_tile.x_pos, this_tile.y_pos)
                            actor_position_list.append({"type": actor_type, "name": actor_name, "position": actor_posn})
                        elif player.id != this_tile.characters[0].id:
                            actor_type = ""
                            if player.type == Type.ZOMBIE:
                                actor_type = "zombie"
                            elif player.type == Type.GHOST:
                                actor_type = "ghost"
                            actor_name = this_tile.characters[0].id
                            actor_posn = (this_tile.x_pos, this_tile.y_pos)
                            actor_position_list.append({"type": actor_type, "name": actor_name, "position": actor_posn})
                    if this_tile.exit:
                        row.append(2)
                    elif this_tile.border:
                        row.append(0)
                    elif this_tile.key and not self.exit_unlocked:
                        object_list.append({"type": "key", "position": [this_tile.x_pos, this_tile.y_pos]})
                        row.append(1)
                    elif this_tile.level_exit:
                        object_list.append({"type": "exit", "position": [this_tile.x_pos, this_tile.y_pos]})
                        row.append(1)
                    else:
                        row.append(1)
                except AttributeError as e:
                    # It's a void tile or out of bounds, so we append a 0.
                    row.append(0)
            tile_layout.append(row)

        return (tile_layout, actor_position_list, object_list)