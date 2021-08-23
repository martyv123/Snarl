#!/usr/bin/env python3

from enum import Enum
from level import *
from character import *
from game import *

class RuleChecker:
    def __init__(self, game):
        """
        Initializes the rulechecker.

        Args:
            game (Game): The game to rule check.
        """
        self.game = game

    def is_valid_game_state(self):
        """
        Determines if the current game state is valid by checking the number of players
        and their active status in relation to the game state.

        Returns:
            bool: Whether the game state is valid
        """
        players_active = False
        
        # Checking number of players
        if len(self.game.players) < 1 or len(self.game.players) > 4:
            return False

        # Checking player status and players are on walkable tiles
        for player in self.game.players:
            if player.active:
                players_active = True
            player_pos = (player.x_pos, player.y_pos)
            try:
                if self.game.current_level.tiles[player_pos[0]][player_pos[1]].border:
                    return False
            except:
                return False
        
        # Checking adversaries are on walkable tiles
        for adversary in self.game.adversaries:
            adversary_pos = (adversary.x_pos, adversary.y_pos)
            try:
                if self.game.current_level.tiles[adversary_pos[0]][adversary_pos[1]].border:
                    return False
            except:
                return False

        # Checking that player status aligns with game state
        if players_active and self.game.state == State.OVER:
            return False
        if not players_active and self.game.state == State.IN_PROGRESS:
            return False

        return True

    def is_valid_level(self, level):
        """
        Determines if the given level is valid by checking for key, exit, 
        and no overlapping rooms and hallways.

        Args:
            level (Level): The level to check validity for. 

        Returns:
            bool: Whether the level is valid
        """

        # Checking that the level has a key
        if not level.key:
            return False

        # Checking that the level has an exit
        if not level.level_exit:
            return False

        # Checking that hallways and rooms do not overlap
        for row in level.tiles:
            for tile in row:
                if isinstance(tile, Tile) and tile.in_room and tile.in_hallway:
                    return False

        return True

    def is_valid_movement(self, character, destination):
        """
        Determines if the movement for the character is valid by Snarl game rules.

        Args:
            character (Player or Adversary): The player or adversary to check.
            destination (int, int): The destination movement to check.

        Returns:
            bool: Whether the movement is valid
        """
        curr = (character.x_pos, character.y_pos)
        abs_distance = (abs(destination[0] - curr[0]), abs(destination[1] - curr[1]))

        # Check if the destination tile contains another actor:
        # 1. Players cannot move onto other players
        # 2. Adversaries cannot move onto other adversaries

        # Check for an existing tile first
        dst_tile = self.game.current_level.tiles[destination[0]][destination[1]]

        if not isinstance(dst_tile, Tile):
            return False

        # Check if player is active
        if not character.active:
            return False

        # Check if destination for the player or character is valid by Snarl rules
        if isinstance(character, Player):
            # Check if the destination tile contains another actor:
            # 1. Players cannot move onto other players
            if dst_tile.characters:
                for c in dst_tile.characters:
                    if isinstance(c, Player) and c.id != character.id:
                        return False

            if abs_distance[0] == 0 and abs_distance[1] == 0 and not dst_tile.border:
                pass
            elif abs_distance[0] + abs_distance[1] <= 2 and not dst_tile.border:
                pass
            else:
                return False
        elif isinstance(character, Adversary):
            # Check if the destination tile contains another actor:
            # 2. Adversaries cannot move onto other adversaries
            if dst_tile.characters:
                for c in dst_tile.characters:
                    if isinstance(c, Adversary) and c.id != character.id:
                        return False
            if abs_distance[0] == 0 and abs_distance[1] == 0:
                pass
            elif abs_distance[0] + abs_distance[1] <= 1:
                pass
            else:
                return False

        # Check if the destination tile is traversable only for non ghosts
        if isinstance(character, Adversary):
            if character.type == Type.GHOST:
                return True
            elif character.type == Type.ZOMBIE:
                try:
                    if isinstance(dst_tile, Tile):
                        if not dst_tile.border:
                            # For zombies, check for invalid moves into a hallway
                            if self.game.current_level.tiles[destination[0]][destination[1]].in_hallway:
                                return False
                            else:
                                return True
                    # Not reached unless tile is a border tile
                    return False
                except:
                    # Not a tile so return false
                    return False
        else:
            try:
                destination_tile = self.game.current_level.tiles[destination[0]][destination[1]]
                if isinstance(dst_tile, Tile):
                    if not destination_tile.border:
                        return True
                return False
            except:
                return False