#!/usr/bin/env python3

import socket
import json
import argparse


class Client:
    def __init__(self):
        self.address = "127.0.0.1"
        self.port = 45678
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wait = 30

    def init_connection(self):
        # Setting up the connection to server
        self.conn.connect((self.address, self.port))
        self.conn.settimeout(self.wait)
        print('Connected on ' + self.address + ':' + str(self.port))

        # Receiving initial requests from server here
        init_done = False
        while not init_done:
            data = None
            try:
                data = self.conn.recv(4096)
                decoded_data = json.loads(data.decode('utf-8'))
                if decoded_data["type"] == "welcome":
                    print("Welcome to the Snarl server! Waiting for players to connect...")
            except Exception as e:
                # Message was not a JSON, so it's probably the server requesting our name
                # This can also be triggered if the server is not sending anything back
                decoded_data = data.decode('utf-8')
                print("We are requesting your player name.")
                init_done = True

    def send_name(self):
        """
        Send the client's specified name to the server.
        """
        player_name = input("Enter your name below: \n")
        self.conn.sendall(player_name.encode())

        # Waiting for server to confirm player name - we'll see a start level message
        start_level = False
        while not start_level:
            data = None
            try:
                data = self.conn.recv(4096)
                decoded_data = json.loads(data.decode('utf-8'))
                if decoded_data["type"] == "start-level":
                    print("The level will start shortly.")
                    start_level = True
            except Exception as e:
                # Message was not a JSON, so it's probably the server requesting our name
                # The name we gave initially was probably not unique
                # This can also be triggered if the server is not sending anything back
                decoded_data = data.decode('utf-8')
                print("Another player has taken that name, please register with a different one.")
                start_level = True
                self.send_name()

    def enter_game(self):
        """
        Game is starting so we enter the phase of player updates, playing rounds, 
        ending levels, and ending the game.
        """
        data = b''

        print("You are now entering the game.")
        while True:
            try:
                data += self.conn.recv(4096)
                decoded_data = json.loads(data.decode('utf-8'))
                if decoded_data["type"] == "player-update":
                    print("\nPlayer update:")
                    if decoded_data["position"][0]:
                        print("Your position is: (" + str(decoded_data["position"][0]) + ", " + str(decoded_data["position"][1]) + ")")
                    if not decoded_data["position"][0]:
                        print("You have already left the level")
                    if decoded_data["message"] != "":
                        print(decoded_data["message"])
                elif decoded_data["type"] == "view":
                    print("\n\nPlayer view:")
                    print("<===>")
                    for row in decoded_data["view"]:
                        print(row)
                    print("<===>\n\n")
                elif decoded_data["type"] == "end-level":
                    print("\nThe level has ended. Here are the level statistics:")
                    if decoded_data["key"]:
                        print("Player who found the key: " + str(decoded_data["key"]))
                    if not decoded_data["key"]:
                        print("No player found the key")
                    if decoded_data["exits"]:
                        print("Players who exited the level: " + str(decoded_data["exits"]))
                    if not decoded_data["exits"]:
                        print("No players exited")
                    if decoded_data["ejects"]:
                        print("Players who were ejected from the level: " + str(decoded_data["ejects"]))
                    if not decoded_data["ejects"]:
                        print("No players ejected")
                elif decoded_data["type"] == "end-game":
                    print("\nThe game has ended. Here are the game statistics:")
                    for player_score in decoded_data["scores"]:
                        print("++++++++++++++++++++")
                        print("Player: " + player_score["name"])
                        print("Exits: " + str(player_score["exits"]))
                        print("Ejects: " + str(player_score["ejects"]))
                        print("Keys: " + str(player_score["keys"]))
                        print("++++++++++++++++++++")
                    print("\n Goodbye!")
                    break
                data = b'' # Reset data
            except:
                decoded_data = data.decode('utf-8')
                # print("test: " + decoded_data)
                # Check if the data was "move"
                if decoded_data == "move":
                    print("\nThe server is requesting your next move")
                    player_move_x_coord = input("Enter the x_coordinate of your move below (integer format): \n")
                    player_move_y_coord = input("Enter the y_coordinate of your move below (integer format): \n")
                    player_move = {"type": "move", "to": [int(player_move_x_coord), int(player_move_y_coord)]}
                    self.conn.sendall(json.dumps(player_move).encode())
                    data = b''
                elif decoded_data == "OK":
                    print("\nYour move was accepted.")
                    data = b''
                elif decoded_data == "Key":
                    print("\nYou found the key.")
                    data = b''
                elif decoded_data == "Exit":
                    print("\nYou found the exit.")
                    data = b''
                elif decoded_data == "Eject":
                    print("\nYou have been ejected.")
                    data = b''
                elif decoded_data == "Invalid":
                    print("\nYour move was invalid.")
                    data = b''
                else:
                    # Malformed JSON, going to call recv again
                    print("Error: Client received: " + str(data.decode()))
                    data = b''

    def close_connection(self):
        """
        Tear down the client socket connection.
        """
        self.conn.close()

    def start_client(self):
        """
        Start the client and connect to the server to play Snarl.
        """
        # Argument parser
        parser = argparse.ArgumentParser(description="Welcome to Snarl!")

        # Adding CL arguments

        parser.add_argument('--address', type=str, help="The IP address on which the server should listen for connections", default="127.0.0.1")
        parser.add_argument('--port', type=int, help="The port number the server will listen on", default=45678)

        # Creating the args list
        args = parser.parse_args()


        self.address = args.address
        self.port = args.port

        self.init_connection()
        self.send_name()

        self.enter_game()