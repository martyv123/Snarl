#!/usr/bin/env python3
import sys
sys.path.append('../Common')

from player import IPlayer

class Client(IPlayer):
    """
    Represents a client that controls a player in the game of Snarl.

    Args:
        IPlayer (IPlayer): Super class for a Player.
    """
    def show_moves(self):
        """
        Queries the game manager to find the list of valid moves for this player.

        Returns:
            [(int, int)]: The list of valid moves for this player.
        """
        return self.game_manager.send_player_moves(self.player)

    def take_turn(self, position):
        """
        Sends a request to the game manager to move to the desired position.

        Args:
            position (int, int): A tuple of x and y coordinates.

        Returns:
            bool: Whether the movement taken during the turn was successful.
        """
        return self.game_manager.accept_movement(position, self.player)

    def get_position(self):
        """
        Gets the current position of this player.

        Returns:
            (int, int): A tuple of x and y coordinates.
        """
        return (self.player.x_pos, self.player.y_pos)

    def get_status(self):
        """
        Gets the status of this player.

        Returns:
            bool: Whether the player is active.
        """
        return self.player.active

    def set_game_manager(self, manager):
        """
        Sets the game manager for this player. This game manager instance will be responsible
        for communicating between the this player, the other players, and all other adversaries
        in the game.

        Args:
            manager (GameManager): The game manager managing this player.
        """
        self.game_manager = manager

    def render_view(self):
        """
        Renders the player's view by printing the view to the console.
        """
        player_view = self.game_manager.send_player_view(self.player)
        print(player_view)

