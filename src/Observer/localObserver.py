#!/usr/bin/env python3
import sys
sys.path.append('../Common')

from observer import IObserver

class Observer(IObserver):
    """
    Represents a local observer that implements the IObserver interface.
    """
    def display_level(self):
        """
        Displays the full level (players, adversaries, keys, exits, doors, etc) by printing to
        the console.
        """
        self.get_game_state()
        full_layout = self.game_manager.game.render_current_level()
        print(full_layout)
        self.get_players()

    def get_players(self):
        """
        Gets the list of players from the game manager and prints out their names and turns.
        """
        players = self.game_manager.game.players
        for player in players:
            print("Player ID: " + player.id + ", Turn order: " + player.turn_id + ", Status: " +
                   player.active + "\n")

    def get_adversaries(self):
        """
        Gets the list of adversaries from the game manager and prints out their names and turns.
        """
        adversaries = self.game_manager.game.adversaries
        for adversary in adversaries:
            print("Adversary ID: " + adversary.id + ", Turn order: " + adversary.turn_id + "\n")

    def get_levels(self):
        """
        Gets the list of levels from the game manager and prints out their layouts.
        """
        levels = self.game_mangager.game.levels
        for id, level in enumerate(levels):
            print("Level #: " + str(id) + "\n")
            print(level.print_level())

    def get_current_level(self):
        """
        Gets the current level in progress from the game manager and prints out its layout.
        """
        current_level = self.game_manager.game.current_level
        print(current_level.print_level())

    def get_game_state(self):
        """
        Gets the current status of the game state from the game manager and prints it out.
        """
        state = self.game_manger.game.state
        printable_state = ""

        if state == State.IN_PROGRESS:
            printable_state = "In Progress"
        else:
            printable_state  ="Over"
        print("The current progress of the game is: " + printable_state + "\n")