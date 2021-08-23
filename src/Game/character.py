#!/usr/bin/env python3

import random
from enum import Enum

class Type(Enum):
    ZOMBIE = 1
    GHOST = 2

class Player():
    def __init__(self, id):
        """
        Represents a Player interface in the game of Snarl.

        Args:
            id (String): The Player's unique ID.
        """
        self.id = id
        self.turn_id = None
        self.active = True
        self.x_pos = None
        self.y_pos = None
        self.exits = 0
        self.ejects = 0
        self.keys = 0
        self.exited = False

    
class Adversary:
    def __init__(self, id):
        """
        Represents an Adversary in the game of Snarl.

        Args:
            id (String): The Adversary's unique ID.
        """
        self.id = id
        self.turn_id = None
        self.active = True
        self.x_pos = None
        self.y_pos = None
        self.type = None
        self.game_manager = None
        self.level = None

    def set_type(self, type):
        """
        Set the type of the adversary.

        Args:
            type (Type): The type of the adversary. These currently include ZOMBIE and GHOST.
        """
        self.type = type

    def set_game_manager(self, manager):
        """
        Sets the game manager for this adversary. This game manager instance will be responsible
        for communicating between the this adversary, players, and all other adversaries,
        in the game.

        Args:
            manager (GameManager): The game manager managing this adversary.
        """
        self.game_manager = manager
        self.level = manager.game.current_level

    def get_position(self):
        """
        Returns the position of the adversary as a tuple.

        Returns:
            (int, int): The position of the adversary.
        """
        return (self.x_pos, self.y_pos)

    def show_moves(self):
        """
        Queries the game manager to find the list of valid moves for this adversary.

        Returns:
            [(int, int)]: The list of valid moves for this adversary.
        """
        return self.game_manager.send_adversary_moves(self)

    def take_turn(self):
        """
        Sends a request to the game manager to move to the desired position.

        Returns:
            bool: Whether the movement taken during the turn was successful.
        """
        # First, get the adversaries valid moves
        valid_moves = self.show_moves()

        # If there are no valid moves, we send our current position (no movement / skip)
        if not valid_moves:
            return self.game_manager.accept_movement((self.x_pos, self.y_pos), self)
        # There are valid moves, determine what move to take
        else:
            # Get the positions of actors in the vicinity of the adversary
            actor_positions = self.level.get_tile_and_actor_lists(self)[1]
            # Looping through actor postions to find players
            for actor in actor_positions:
                if actor["type"] == "player":
                    # Determine closest valid movement to player and send to game manager
                    closest_move = self.find_closest_move(actor["position"], valid_moves)
                    return self.game_manager.accept_movement(closest_move, self)

            # There are no players in the vicinity, let's pick a random valid move
            rand_index = random.randint(0, len(valid_moves) - 1)
            move = valid_moves[rand_index]
            return self.game_manager.accept_movement(move, self)

    def find_closest_move(self, position, valid_moves):
        """
        Find the distance between the adversary's current position and the given position.

        Args:
            position (int, int): The position to check.
            valid_moves [position]: The adversary's valid moves.

        Returns:
            (int, int): The closest valid move to the position.
        """
        closest = None
        closest_value = 100
        for move in valid_moves:
            if closest:
                x_dist = abs(position[0] - move[0])
                y_dist = abs(position[1] - move[1])
                if x_dist + y_dist < closest_value:
                    closest = move
                    closest_value = x_dist + y_dist
            else:
                closest = move

        return closest