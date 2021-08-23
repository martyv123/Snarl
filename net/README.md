# MEMORANDUM

### DATE: 4/16/2021
### TO: Instructors / TAs
### FROM: John Hassan & Marty Vo
### SUBJECT: Snarl Client and Server
------------------------------------------------------------------------------

# Snarl Server
The ```snarlServer``` executable starts the server. It should take the following optional command line arguments: <br>

- ```--levels FILE```, where FILE is the path and name of a file containing a JSON level specifications. The default is snarl.levels which resides in the current directory). <br>

- ```--clients N```, where 1 ≤ N ≤ 4 is the maximum number of clients the server will for before starting the game. The default is 4. <br>

- ```--wait N```, where N is the number of seconds to wait for the next client to connect. The default is 60. <br>

- ```--observe```, when this option is given, the server will start a local observer to display the progress of the game.

- ```--address IP```, where IP is an IP address on which the server should listen for connections. The default is 127.0.0.1. <br>

- ```--port NUM```, where NUM is the port number the server will listen on. The default is 45678. <br>

# Snarl Client
The ```snarlClient``` executable starts the client. It should take the following optional command line arguments: <br>

- ```--address IP```, where IP is an IP address the client should connect to. The default is 127.0.0.1. <br>

- ```--port NUM```, where NUM is the port number the client should connect to. The default is 45678. <br>

# How to Play
1. Clone the repository which can be found [here](https://github.ccs.neu.edu/CS4500-S21/Olindond).
2. Enter the directory path: ```Olindond/Snarl/src/net``` which will contain the ```snarlServer``` and ```snarlClient``` executables.
3. Start the ```snarlServer``` executable with your desired command line arguments.
4. Start the ```snarlClient``` executable with your desigred command line arguments.
5. The client program will prompt you with further instructions.
6. The observer that is available via ```snarlServer``` can be used in a terminal.
7. Instructions on how Snarl is played can be found [here](https://course.ccs.neu.edu/cs4500sp21/plan.html): 
8. Have fun! 