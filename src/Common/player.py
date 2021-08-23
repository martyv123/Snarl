#!/usr/bin/env python3

from abc import ABC, abstractmethod

class IPlayer(ABC):
    def __init__(self, player):
        """
        Represents a Player interface in the game of Snarl.

        Args:
            player (Player): The Player's that the client controls.
        """
        self.player = player
        self.game_manager = None
        super().__init__()

    @abstractmethod
    def show_moves(self):
        """
        Queries the game manager to find the list of valid moves for this player.

        Returns:
            [(int, int)]: The list of valid moves for this player.
        """
        pass

    @abstractmethod
    def take_turn(self, position):
        """
        Sends a request to the game manager to move to the desired position.

        Args:
            position (int, int): A tuple of x and y coordinates.

        Returns:
            bool: Whether the movement taken during the turn was successful.
        """
        pass

    @abstractmethod
    def get_position(self):
        """
        Gets the current position of this player.

        Returns:
            (int, int): A tuple of x and y coordinates.
        """
        pass

    @abstractmethod
    def get_status(self):
        """
        Gets the status of this player.

        Returns:
            bool: Whether the player is active.
        """
        pass

    @abstractmethod
    def set_game_manager(self, manager):
        """
        Sets the game manager for this player. This game manager instance will be responsible
        for communicating between the this player, the other players, and all other adversaries
        in the game.

        Args:
            manager (GameManager): The game manager managing this player.
        """
        pass

    @abstractmethod
    def render_view(self):
        """
        Renders the player's view by printing the view to the console.
        """