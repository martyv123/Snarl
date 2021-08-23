#!/usr/bin/env python3

import sys
import socket
import json
import time
import math
import random
import argparse

sys.path.append('../Player')
sys.path.append('../Game')
sys.path.append('../Common')

from character import *
from level import *
from game import *
from gameManager import *
from localPlayer import *


class Remote:
    def __init__(self):
        """
        Initialize the remote server for a game of Snarl with default configurations. 
        These fields can be modified to desired configurations.
        """
        self.levels_file = "snarl.levels"
        self.num_clients = 4
        self.wait = 60
        self.observer_view = False
        self.address = "127.0.0.1"
        self.port = 45678
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.num_connections = 0
        self.connections = []
        self.clients = []
        self.adversaries = []
        self.levels = None
        self.game = None
        self.game_manager = None

    def init_tiles(self, room, layout):
        """
        Initializes the tiles for the room.

        Args:
            room (Room): The room to initialize tiles for.
            layout ([JSON]): The layout for the room.
        """
        for i in range(room.length):
            for j in range(room.width):
                tile_type = layout[i][j]
                if tile_type == 0:
                    new_tile = Tile(i, j, True, False, False, False)
                    new_tile.in_room = True
                    room.tiles[i][j] = new_tile
                elif tile_type == 1:
                    new_tile = Tile(i, j, False, False, False, False)
                    new_tile.in_room = True
                    room.tiles[i][j] = new_tile
                else:
                    new_tile = Tile(i, j, False, True, False, False)
                    new_tile.in_room = True
                    room.tiles[i][j] = new_tile

    def add_rooms(self, level, rooms):
        """
        Adds the JSON input of rooms to the instantiated level.

        Args:
            level ([type]): The instantiated level.
            rooms ([JSON]): The JSON input of rooms.
        """
        for room in rooms:
            origin = room["origin"]
            bounds = room["bounds"]
            layout = room["layout"]
            new_room = Room(bounds["rows"], bounds["columns"])
            self.init_tiles(new_room, layout)
            level.add_room(origin[0], origin[1], new_room)

    def add_hallways(self, level, hallways):
        """
        Adds hallways to the level.

        Args:
            level (Level): The level to add hallways to.
            hallways ([JSON]): The JSON input of hallways.
        """
        for hallway in hallways:
            from_ = hallway["from"]
            to = hallway["to"]
            waypoints = hallway["waypoints"]
            waypoints_t = []
            for w in waypoints:
                waypoints_t.append((w[0], w[1]))
            room1 = None
            room2 = None
            for room in level.rooms:
                for t in room.tiles:
                    for a in t:
                        if a.x_pos == from_[0] and a.y_pos == from_[1]:
                            room1 = room

            for room in level.rooms:
                for t in room.tiles:
                    for a in t:
                        if a.x_pos == to[0] and a.y_pos == to[1]:
                            room2 = room
            level.add_hallway(from_[0], from_[1], to[0], to[1], waypoints_t, room1, room2)

    def parse_levels_file(self):
        """
        Parse the levels file to create levels for our Snarl game.
        We will add the levels to our Game, which will then be added to our Game Manager.
        """
        levels_file = self.levels_file
        num_levels = 0
        json_levels = []

        # Pulling data from snarl.levels file
        with open (levels_file, mode='r') as input_file:
            curr_json_level = ""
            counter = 0
            for line in input_file.readlines():
                # print(line)
                if counter == 0:
                    num_levels = int(line.strip())
                else:
                    if line == "\n" and counter != 1:
                        json_levels.append(curr_json_level.strip('\n'))
                        curr_json_level = ""
                    else:
                        curr_json_level += line
                counter += 1

            # Append the last JSON level to the json_levels list
            json_levels.append(curr_json_level.strip('\n'))

            # Convert str json levels into json objects
            parsed_levels = []
            for json_level in json_levels:
                parsed_levels.append(json.loads(json_level))

            # Create our rooms, hallways, and level to add to the game
            # We will start at level 0
            starting_level = 0
            levels = []
            for index, json_level in enumerate(parsed_levels):
                if index < starting_level - 1:
                    continue
                else:
                    rooms = json_level["rooms"]
                    hallways = json_level["hallways"]
                    objects = json_level["objects"]
                    key_pos = None
                    exit_pos = None

                    testing_level = Level(20, 20)

                    # Adding rooms to our level
                    self.add_rooms(testing_level, rooms)

                    # Adding hallways to our level
                    self.add_hallways(testing_level, hallways)

                    # Set the key and exit for the level
                    for obj in objects:
                        if obj["type"] == "exit":
                            exit_pos = obj["position"]
                            testing_level.set_level_exit(exit_pos[0], exit_pos[1])
                        elif obj["type"] == "key":
                            key_pos = obj["position"]
                            testing_level.set_key(key_pos[0], key_pos[1])

                    levels.append(testing_level)

        self.levels = levels

    def init_server(self):
        """
        Initialize the TCP connection for clients to connect on.
        """
        # Listening on the server socket
        self.server.bind((self.address, self.port))
        self.server.settimeout(self.wait)
        print('Server socket created on ' + self.address + ':' + str(self.port))

        # Listening for connections until all clients request or timeout
        while self.num_connections < self.num_clients:
            try:
                self.server.listen()
                conn, addr = self.server.accept()
                print("Connected to " + addr[0] + ":" + str(addr[1]))
                self.num_connections += 1
                self.connections.append(conn)

                # Send the server welcome message
                welcome_message = {"type": "welcome", "info": "Olindond"}
                conn.send(json.dumps(welcome_message).encode())

            except:
                self.close_server()
                break

        # Initializing the Game and the Game Manager
        self.parse_levels_file()
        self.game = Game([], [], self.levels)
        self.game_manager = GameManager(self.game)

        time.sleep(1)

        # All client connections have occured, check to see if we have received the names
        while len(self.game.players) != self.num_clients:
            self.get_player_names(len(self.game.players))
    
    def get_player_names(self, num_players):
        """
        Recieve player names from the client connections. Each name should be unique.

        Args:
            num_players (int): The number of valid names already registered.
        """
        try:
            conn_to_listen_to = self.connections[num_players]
            # Send the request for name
            conn_to_listen_to.send("name".encode())

            encoded_name = conn_to_listen_to.recv(4096)
            name = encoded_name.decode('utf-8')
            print("Client sent for name: " + str(name))

            # Now we create the player avatar and append it to our list of players
            player = Player(name)
            accepted_player = self.game_manager.accept_player(player)

            # Check if name is unique. If name is not unique, request another name.
            if not accepted_player:
                print("Player name was not accepted. Retrying...")
                self.get_player_names(num_players)

        except:
            # No data received from the client connection, assume they disconnected
            # Game will not start
            self.close_server()

    def create_zombies(self, number):
        """
        Create the given number of zombies.

        Args:
            number: The number of zombies.

        Returns:
            [Adversary]: A list of the zombie adversaries.
        """
        zombies = []
        for i in range(number):
            id = "Z" + str(i)
            new_zombie = Adversary(id)
            new_zombie.set_type(Type.ZOMBIE)
            zombies.append(new_zombie)

        return zombies

    def create_ghosts(self, number):
        """
        Create the given number of ghosts.

        Args:
            number: The number of ghosts.

        Returns:
            [Adversary]: A list of the ghosts adversaries.
        """
        ghosts = []
        for i in range(number):
            id = "G" + str(i)
            new_ghost = Adversary(id)
            new_ghost.set_type(Type.GHOST)
            ghosts.append(new_ghost)

        return ghosts

    def setup_adversaries(self):
        """
        Set-up the Zombie and Ghost adversaries according to the level number.
        """
        current_level_num = self.game.levels.index(self.game.current_level)
        num_zombies = math.floor(current_level_num / 2) + 1
        num_ghosts = math.floor((current_level_num - 1) / 2)

        zombies = self.create_zombies(num_zombies)
        ghosts = self.create_ghosts(num_ghosts)
        adversaries = zombies + ghosts

        # Accept the adversaries into the game via the game manager
        for adversary in adversaries:
            self.game_manager.accept_adversary(adversary)

    def get_random_starting_position(self, level):
        """
        Pick a random starting position for a traversable tile in a room.
        The tile cannot be occupied by another actor or object.

        Args:
            level (Level): The level to find a random starting position for.

        Returns:
            (int, int): The starting position
        """
        length = level.length
        width = level.width

        for i in range(length):
            for j in range(width):
                rand_x_pos = random.randint(0, length - 1)
                rand_y_pos = random.randint(0, width - 1)
                dst_tile = level.tiles[rand_x_pos][rand_y_pos]
                if isinstance(dst_tile, Tile) and dst_tile.in_room and not dst_tile.border:
                    if not dst_tile.level_exit and not dst_tile.key and not dst_tile.characters:
                        return (rand_x_pos, rand_y_pos)

    def place_at_initial_positions(self):
        """
        Place Players and Adversaries at their initial positions.
        """
        # Initially place the players and adversaries in random locations
        # Must be on a traversable room tile, not on another player/adversary, and not on a key/exit

        for player in self.game.players:
            player_starting_pos = self.get_random_starting_position(self.game.current_level)
            if self.game.current_level.place_player(player, player_starting_pos[0], player_starting_pos[1]):
                # print("Successfully placed player " + player.id)
                pass
            else:
                pass
                # print("Could not place player " + player.id)

        for adversary in self.game.adversaries:
            adversary_starting_pos = self.get_random_starting_position(self.game.current_level)
            if self.game.current_level.place_adversary(adversary, adversary_starting_pos[0], adversary_starting_pos[1]):
                # print("Successfully placed adversary " + adversary.id)
                pass
            else:
                # print("Could not place adversary " + adversary.id)
                pass

    def start_level(self):
        """
        Start the level and send the level-start message.
        """
        # Sending the start-level JSON message to client connections.
        name_list = []
        current_level_num = self.game.levels.index(self.game.current_level)
        for player in self.game.players:
            name_list.append(player.id)
        start_level = {"type": "start-level", "level": current_level_num, 
                        "players": name_list}
        time.sleep(2)
        for conn in self.connections:
            conn.send(json.dumps(start_level).encode())

        self.game_manager.start_game()

    def send_player_updates(self):
        """
        Send initial player updates to all players before starting the level.
        """
        time.sleep(2)
        for index, player in enumerate(self.game.players):
            # print("Sending player update and player view to player: " + str(index + 1))
            tile_layout = self.game.current_level.get_tile_and_actor_lists(player)[0]
            actor_position_list = self.game.current_level.get_tile_and_actor_lists(player)[1]
            object_list = self.game.current_level.get_tile_and_actor_lists(player)[2]
            message = self.game.current_level.interaction_log

            player_update = {"type": "player-update",
                            "layout": tile_layout,
                            "position": [player.x_pos, player.y_pos],
                            "objects": object_list,
                            "actors": actor_position_list,
                            "message": message}

            # Sending the player update messages to clients
            conn_to_send_to = self.connections[index]
            conn_to_send_to.send(json.dumps(player_update).encode())

            # Sending player view
            player_view = self.game_manager.send_player_view(player)
            player_view_message = {"type": "view", "view": player_view}
            conn_to_send_to.send(json.dumps(player_view_message).encode())

            if self.observer_view:
                observer_view = self.game.current_level.print_level()
                print("\n<===================>")
                for row in observer_view:
                    print(row)
                print("<===================>\n")

    def send_move_result(self, conn, result):
        """
        Send the move result.

        Args:
            conn (socket): The connection of the player to send to.

            result (string): "OK", "Key", "Exit", "Eject", "Invalid"
        """
        time.sleep(2)
        conn.send(result.encode())

    def play_round(self):
        """
        Plays a single round for a level. Requests moves from each player and plays them.
        """
        all_moved = False

        time.sleep(2)
        print("Start of round begins")

        while not all_moved:
            if self.game.is_end_of_level() or self.game.is_end_of_game():
                self.game.levels_completed -= 1
                break
            if self.game_manager.whose_turn == Turn.PLAYER:
                successful_move = False

                curr_player_turn = self.game_manager.player_turn
                conn_to_send_to = self.connections[curr_player_turn - 1]
                curr_player = self.game.players[curr_player_turn - 1]

                move = b''
                unsuccesful_moves = 0

                while not successful_move:
                    try:
                        # Wait for move request - we'll only allow 3 tries per player
                        # Skip their turn after 3 unsuccessful tries

                        if unsuccesful_moves == 3:
                            print("Player has had 3 unsuccessful moves, we are skipping their turn")

                            curr_player_posn = (curr_player.x_pos, curr_player.y_pos)
                            prev_keys = curr_player.keys
                            prev_exits = curr_player.exits
                            prev_ejects = curr_player.ejects

                            self.game_manager.accept_movement(curr_player_posn, curr_player)

                            # Sending result and player updates
                            if curr_player.keys > prev_keys:
                                self.send_move_result(conn_to_send_to, "Key")
                                self.send_player_updates()
                            elif curr_player.exits > prev_exits:
                                self.send_move_result(conn_to_send_to, "Exit")
                                self.send_player_updates()
                            elif curr_player.ejects > prev_ejects:
                                self.send_move_result(conn_to_send_to, "Eject")
                                self.send_player_updates()
                            else:
                                self.send_move_result(conn_to_send_to, "OK")
                                self.send_player_updates()

                            break

                        # Send the move request
                        time.sleep(2)
                        conn_to_send_to.send("move".encode())

                        # Wait for move from player
                        move += conn_to_send_to.recv(4096)
                        decoded_move = json.loads(move.decode('utf-8'))

                        if decoded_move["type"] == "move":
                            posn_to_move_to = decoded_move["to"]
                            # print("We received the requested move to " + str(posn_to_move_to[0]) + ", " + str(posn_to_move_to[1]))
                            # Here we can start moving the player
                            prev_keys = curr_player.keys
                            prev_exits = curr_player.exits
                            prev_ejects = curr_player.ejects
                            print(curr_player.id + " is attempting to move...")
                            if self.game_manager.accept_movement((posn_to_move_to[0], posn_to_move_to[1]), curr_player):
                                print(str(curr_player.id) +  " entered a successful move")
                                successful_move = True
                                
                                # Sending result and player updates
                                if curr_player.keys > prev_keys:
                                    print("Key was found by player " + str(curr_player_turn))
                                    self.send_move_result(conn_to_send_to, "Key")
                                    self.send_player_updates()
                                elif curr_player.exits > prev_exits:
                                    print("Exit was found by player " + str(curr_player_turn))
                                    self.send_move_result(conn_to_send_to, "Exit")
                                    self.send_player_updates()
                                elif curr_player.ejects > prev_ejects:
                                    print("Player " + str(curr_player_turn) + " was expelled")
                                    self.send_move_result(conn_to_send_to, "Eject")
                                    self.send_player_updates()
                                else:
                                    self.send_move_result(conn_to_send_to, "OK")
                                    self.send_player_updates()

                                move = b''
                            else:
                                print(str(curr_player.id) + " did not enter a successful move, retrying")
                                unsuccesful_moves += 1
                                move = b''
                                self.send_move_result(conn_to_send_to, "Invalid")
                    except Exception as e:
                        # We should enter the while loop again
                        print("Move was not a valid JSON or not all data received by socket")
                        print("This was what was recieved: " + str(move))
                        move = b''     
                        print("This is the error: ")
                        print(e)

            elif self.game_manager.whose_turn == Turn.ADVERSARY:
                for adversary in self.game.adversaries:
                    successful_move = False
                    while not successful_move:
                        successful_move = adversary.take_turn()
                    self.send_player_updates()
                    
                print("Adversaries have moved.")

                # This should end the round
                all_moved = True

    def level_init(self):
        """
        Initialize the beginning of a level.
        """
        print("Level is initializing")
        self.setup_adversaries()
        self.place_at_initial_positions()
        self.start_level()
        # This is the initial update
        self.send_player_updates()

    def send_end_level(self):
        """
        Send the end of level statistics.
        """
        time.sleep(2)
        for conn in self.connections:
            end_level_message = self.game.current_level.end_level_message
            conn.send(json.dumps(end_level_message).encode())

    def send_end_game(self):
        """
        Send the end of game statistics.
        """
        time.sleep(2)
        self.game.get_game_scores()
        for conn in self.connections:
            end_game_message = self.game.end_game_message
            conn.send(json.dumps(end_game_message).encode())

    def close_server(self):
        """
        Tear down the server socket connection.
        """
        self.server.close()

    def start_server(self):
        """
        Start the server and the game.
        """
        # Argument parser
        parser = argparse.ArgumentParser(description="Welcome to Snarl!")

        # Adding CL arguments
        parser.add_argument('--levels', help="FILENAME containing JSON level specifications.",
                            default='snarl.levels')
        parser.add_argument('--clients', type=int, help="The number of clients (1-4).", default=4)
        parser.add_argument('--wait', type=int, help="The number of seconds to wait for the next client to connect.", default=60)
        parser.add_argument('--observe', help="Switch to an observer view.", action='store_true')
        parser.add_argument('--address', type=str, help="The IP address on which the server should listen for connections", default="127.0.0.1")
        parser.add_argument('--port', type=int, help="The port number the server will listen on", default=45678)

        # Creating the args list
        args = parser.parse_args()

        # Pulling information from command line args
        self.levels_file = args.levels
        self.num_clients = args.clients
        self.wait = args.wait
        self.observer_view = True if args.observe else False
        self.address = args.address
        self.port = args.port

        # Initialize the server after all setup is complete
        self.init_server()

        # Initialize the first level
        self.level_init()

        # We are now playing the game
        while not self.game.is_end_of_game():
            if self.game.is_end_of_level():
                # Send end of level statistics
                print("**********End of level reached**********")
                print(str(self.game.levels_completed) + " levels completed")
                if self.game.is_end_of_game():
                    print("**********End of game reached**********")
                    break
                else:
                    self.send_end_level()
                    self.game.level_up()
                    time.sleep(2)
                    self.level_init()
            
            # This plays a round
            self.play_round() 

        # Send end of game statistics
        self.send_end_game()

        print("The game has ended.")

        self.close_server()
