#!/usr/bin/env python3

from enum import Enum
from level import *
from character import *

class Turn(Enum):
    PLAYER = 1
    ADVERSARY = 2

class State(Enum):
    OVER = 1
    IN_PROGRESS = 2

class Game:
    def __init__(self, players, adversaries, levels):
        """
        Initializes the Game.
        Args:
            players ([Player]): The list of Players in the Game
            adversaries ([Adversary]): The list of Adversaries in the Game
            levels ([Level]): The list of Levels in the Game

        """
        self.players = players
        self.adversaries = adversaries
        self.levels = levels
        self.levels_completed = 0
        self.state = State.OVER
        self.current_level = self.levels[0]
        self.end_game_message = {"type": "end-game",
                                 "scores": []}

    def get_game_scores(self):
        """
        Populates the end-game JSON message sent to all players at the end of the game.
        """
        for player in self.players:
            player_score = {"type": "player-score",
                            "name": player.id,
                            "exits": player.exits,
                            "ejects": player.ejects,
                            "keys": player.keys}
            self.end_game_message["scores"].append(player_score)

    def is_end_of_level(self):
        """
        Determines whether the current level is over, either by players finding both the key and
        the exit, or by adversaries eliminating all players. All players must have exited as well.

        Returns:
            bool: Whether the current level is over.
        """
        
        if self.current_level.level_over or len(self.players) == len(self.current_level.players_exited):
            self.levels_completed += 1
            return True

    def is_end_of_game(self):
        """
        Determines whether the game is over, either by players finding both the key and
        the exit for the last level, or by adversaries eliminating all players.

        Returns:
            bool: Whether the game is over.
        """

        if self.levels_completed == len(self.levels):
            return True
        else:
            return False

        # Check if we have any active players left
        # self.state == State.OVER

        # for player in self.players:
        #     if player.active:
        #         self.state = State.IN_PROGRESS

        # # If we do have active players, check if the last level has been won
        # last_level = self.levels[len(self.levels) - 1]
        # if last_level == self.current_level and self.is_end_of_level():
        #     self.state == State.OVER

        # # Return whether the game is over or still ongoing
        # if self.state == State.IN_PROGRESS:
        #     return False
        # elif self.state == State.OVER:
        #     return True

    def level_up(self):
        """ Advance to the Game's next Level and resets the players' statuses.
        """
        if self.levels[len(self.levels) - 1] == self.current_level:
            for player in self.players:
                player.active = False
        elif len(self.current_level.players_exited) == len(self.players):
            self.current_level = self.levels[self.levels.index(self.current_level) + 1]
            for player in self.players:
                player.active = True
                player.exited = False

        self.adversaries = []

    def place_players(self):
        """ 
        Place all Players on the starting tile of the top-left most Room in the current Level.
        This is used when starting a Snarl Game from the beginning.
        For creating intermediate Game states, place players via the place_character method in a level.
        """

        """
        Note: Players can't be on same tile, so if there is more than one player only the first
        player will be placed on the starting tile. This function is mainly used for testing purposes.
        """
        starting_point = self.current_level.get_start()
        for player in self.players:
            self.current_level.place_player(player, starting_point[0], starting_point[1])

    def place_adversaries(self):
        """ 
        Place all Adversaries on the starting tile of the bottom-right most Room in the current Level.
        This is used when starting a Snarl Game from the beginning.
        For creating intermediate Game states, place players via the place_character method in a level.
        """

        """
        Note: Adversaries can't be on same tile, so if there is more than one player only the first
        player will be placed on the starting tile. This function is mainly used for testing purposes.
        """
        starting_point = self.current_level.get_adversary_start()
        for adversary in self.adversaries:
            self.current_level.place_adversary(adversary, starting_point[0], starting_point[1])

    def get_game_state(self):
        """ Returns the current Game state.
        """
        return self.state

    def end_game(self):
        """ Ends the game by setting the state to be OVER.
        """
        self.state = State.OVER

    def render_current_level(self):
        """ Render the current Level of the game.
        """
        layout = self.current_level.print_level()
        return layout