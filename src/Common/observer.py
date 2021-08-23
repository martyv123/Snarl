#!/usr/bin/env python3

from abc import ABC, abstractmethod

class IObserver(ABC):
    def __init__(self, game_manager):
        """
        Represents an observer interface for the game of Snarl. The observer has the ability
        to view the game in progress and has access to all of the player's and adversaries
        locations, as well as a full view and knowledge of the current level.

        Args:
            player (Player): The Player's that the client controls.
        """
        self.game_manager = game_manager
        super().__init__()

    @abstractmethod
    def display_level(self):
        """
        Displays the full level (players, adversaries, keys, exits, doors, etc) by printing to
        the console.
        """

    @abstractmethod
    def get_players(self):
        """
        Gets the list of players from the game manager and prints out their names and turns.
        """

    @abstractmethod
    def get_adversaries(self):
        """
        Gets the list of adversaries from the game manager and prints out their names and turns.
        """

    @abstractmethod
    def get_levels(self):
        """
        Gets the list of levels from the game manager and prints out their layouts.
        """

    @abstractmethod
    def get_current_level(self):
        """
        Gets the current level in progress from the game manager and prints out its layout.
        """

    @abstractmethod
    def get_game_state(self):
        """
        Gets the current status of the game state from the game manager and prints it out.
        """