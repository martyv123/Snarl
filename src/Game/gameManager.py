#!/usr/bin/env python3

from enum import Enum
from level import *
from character import *
from game import *
from ruleChecker import *

class GameManager:
    def __init__(self, game):
        """
        Represents the game manager for a game of Snarl. The game manager handles communication
        between the Player and the Game state. This communication involves moving the Player, 
        interactions involving the Player, and other functions necessary to facilitate the game.

        Args:
            game (Game): The game to be managed.
        """
        self.game = game
        self.whose_turn = None
        self.player_turn = 1
        self.adversary_turn = 1
        self.rulechecker = RuleChecker(game)
    
    def accept_player(self, player):
        """
        Accepts a player into the game of Snarl given that they contain a unique ID and that
        there are less than 4 players currently in the game.

        Args:
            player (Player): The player to be added.

        Returns:
            bool: Whether the player was accepted into the game.
        """

        # Checking for maximum number of players in the game
        if len(self.game.players) == 4:
            return False

        # Checking that the player contains a unique ID
        for current_player in self.game.players:
            if current_player.id == player.id:
                return False
        
        # Adding player to the game and setting their turn ID
        player.turn_id = len(self.game.players) + 1
        self.game.players.append(player)

        return True

    def accept_adversary(self, adversary):
        """
        Accepts an adversary into the game of Snarl given that they contain a unique ID.

        Args:
            adversary (Adversary): The adversary to be added.

        Returns:
            bool: Whether the adversary was accepted into the game.
        """

        # Checking that the adversary contains a unique ID
        for current_adversary in self.game.adversaries:
            if current_adversary.id == adversary.id:
                return False
        
        # Adding player to the game and determining move order
        adversary.turn_id = len(self.game.adversaries) + 1
        self.game.adversaries.append(adversary)
        adversary.set_game_manager(self)
        
        return True

    def accept_movement(self, position, character):
        """
        Accepts a movement taken by a character on their turn and moves the character if
        the move is valid. Accepting a movement changes the turn to the next player or
        adversary. If the character is the last player or adversary to move, the
        game turn ends for players or adversaries.

        Args:
            position (int, int): The position to move the character to.
            character (Character): The character to move.

        Returns:
            bool: Whether the movement was accepted and the player was moved.
        """
        turn = self.whose_turn
        player_turn= self.get_current_player_turn()
        adversary_turn = self.get_current_adversary_turn()
        curr_player = None
        curr_adversary = None

        for player in self.game.players:
            if player.turn_id == player_turn:
                curr_player = player

        for adversary in self.game.adversaries:
            if adversary.turn_id == adversary_turn:
                curr_adversary = adversary

        if self.rulechecker.is_valid_movement(character, position):
            curr_level = self.game.current_level
            if isinstance(character, Player) and turn == Turn.PLAYER and curr_player == character:
                curr_level.place_player(character, position[0], position[1])
                self.change_player_turn()
                return True
            elif isinstance(character, Adversary) and turn == Turn.ADVERSARY and curr_adversary == character:
                curr_level.place_adversary(character, position[0], position[1])
                self.change_adversary_turn()
                return True
            else:
                return False
        else:
            return False

    def start_game(self):
        """
        Begins the game at the first level.
        """
        self.game.state = State.IN_PROGRESS
        self.whose_turn = Turn.PLAYER

    def end_game(self):
        """
        Ends the game.
        """
        self.game.state = State.OVER        

    def get_current_player_turn(self):
        """
        Gets the current player's turn.

        Returns:
            (int): The index of the current player's turn
        """
        return self.player_turn

    def get_current_adversary_turn(self):
        """
        Gets the current adversary's turn.

        Returns:
            (int): The index of the current adversary's turn
        """
        return self.adversary_turn

    def change_player_turn(self):
        """
        Changes the player's turn to the next player.
        """
        curr_level = self.game.current_level
        if curr_level.level_over:
            self.player_turn = 1
        else:
            players_exited = curr_level.players_exited
            players_in = []

            # Find out who is left in the level
            for player in self.game.players:
                if player not in players_exited:
                    players_in.append(player)
            
            # Last player turn
            last_player_turn = players_in[len(players_in) - 1].turn_id

            # Change turn based on who is left in the level
            if self.player_turn == last_player_turn:
                self.player_turn = players_in[0].turn_id
                self.change_game_turn()
            else:
                if self.player_turn > last_player_turn:
                    self.player_turn = players_in[0].turn_id
                    self.change_game_turn()
                else:
                    for p in players_in:
                        if p.turn_id > self.player_turn:
                            self.player_turn = p.turn_id

    def change_adversary_turn(self):
        """
        Changes the adversary's turn to the next player.
        """

        # Last adversary turn
        last_adversary_turn = self.game.adversaries[len(self.game.adversaries) - 1].turn_id

        if self.adversary_turn == last_adversary_turn:
            self.adversary_turn = 1
            self.change_game_turn()
        else:
            self.adversary_turn += 1

    def change_game_turn(self):
        """
        Changes the game's turn from either Players -> Adversaries or Adversaries -> Players
        """
        if self.whose_turn == Turn.PLAYER:
            self.whose_turn = Turn.ADVERSARY
        else:
            self.whose_turn = Turn.PLAYER

    def send_player_turn_notification(self, player):
        """
        Sends a notification to the player indicating that it is their turn to move.

        Args:
            player (Player): The player to send a notification to.
        """

        # Get and print player view first
        # player_view = self.send_player_view(player)
        # for row in player_view:
        #     print(row)

        # Prompt the player for input
        print("Player " + str(player.turn_id) + " it is your turn to move!\n")
        print("Your position on the board is (" + str(player.x_pos) + ", "
              + str(player.y_pos) + ")" + "\n")
        print("Where would you like to go next?\n")

    def send_player_moves(self, player):
        """
        Sends the list of valid moves for the player back to the player.

        Args:
            player (Player): The player receiving its list of valid moves.

        Returns:
            [(int, int)]: The list of valid moves.
        """
        valid_moves = []
        curr_pos = (player.x_pos, player.y_pos)

        # Checking no movement
        if self.rulechecker.is_valid_movement(player, curr_pos):
            valid_moves.append(curr_pos)

        # Checking up
        if self.rulechecker.is_valid_movement(player, (curr_pos[0], curr_pos[1] - 1)):
            valid_moves.append((curr_pos[0], curr_pos[1] - 1))
        if self.rulechecker.is_valid_movement(player, (curr_pos[0], curr_pos[1] - 2)):
            valid_moves.append((curr_pos[0], curr_pos[1] - 2))

        # Checking down
        if self.rulechecker.is_valid_movement(player, (curr_pos[0], curr_pos[1] + 1)):
            valid_moves.append((curr_pos[0], curr_pos[1] + 1))
        if self.rulechecker.is_valid_movement(player, (curr_pos[0], curr_pos[1] + 2)):
            valid_moves.append((curr_pos[0], curr_pos[1] + 2))

        # Checking left
        if self.rulechecker.is_valid_movement(player, (curr_pos[0] - 1, curr_pos[1])):
            valid_moves.append((curr_pos[0] - 1, curr_pos[1]))
        if self.rulechecker.is_valid_movement(player, (curr_pos[0] - 2, curr_pos[1])):
            valid_moves.append((curr_pos[0] - 2, curr_pos[1]))

        # Checking right
        if self.rulechecker.is_valid_movement(player, (curr_pos[0] + 1, curr_pos[1])):
            valid_moves.append((curr_pos[0] + 1, curr_pos[1]))
        if self.rulechecker.is_valid_movement(player, (curr_pos[0] + 2, curr_pos[1])):
            valid_moves.append((curr_pos[0] + 2, curr_pos[1]))

        return list(set(valid_moves))

    def send_player_view(self, player):
        """
        Sends the player view to the player.

        Args:
            player (Player): Player who is requesting the view.

        Returns:
            [str]: The player's view.
        """
        player_view = self.game.current_level.get_player_view(player)

        return player_view

    def send_adversary_moves(self, adversary):
        """
        Sends the list of valid moves for the adversary back to the adversary.

        Args:
            adversary (Adversary): The adversary receiving its list of valid moves.

        Returns:
            [(int, int)]: The list of valid moves.
        """
        valid_moves = []
        curr_pos = (adversary.x_pos, adversary.y_pos)

        # Checking no movement
        if self.rulechecker.is_valid_movement(adversary, curr_pos):
            valid_moves.append(curr_pos)

        # Checking up
        if self.rulechecker.is_valid_movement(adversary, (curr_pos[0], curr_pos[1] - 1)):
            valid_moves.append((curr_pos[0], curr_pos[1] - 1))

        # Checking down
        if self.rulechecker.is_valid_movement(adversary, (curr_pos[0], curr_pos[1] + 1)):
            valid_moves.append((curr_pos[0], curr_pos[1] + 1))

        # Checking left
        if self.rulechecker.is_valid_movement(adversary, (curr_pos[0] - 1, curr_pos[1])):
            valid_moves.append((curr_pos[0] - 1, curr_pos[1]))

        # Checking right
        if self.rulechecker.is_valid_movement(adversary, (curr_pos[0] + 1, curr_pos[1])):
            valid_moves.append((curr_pos[0] + 1, curr_pos[1]))

        return valid_moves