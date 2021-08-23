# Snarl: How to Play

# Requirements:
- Python 3.6+
- Terminal or CLI (Command Line Interface)

# Setting Up:
1. Clone the repository at https://github.com/martyv123/Snarl/
2. Open the directory at Olindond/Snarl/local.
3. Run the executable in a terminal with the command ```./localSnarl --help```.
4. Run the executable again with your desired flags. <br>
Example: ```./localSnarl --levels exampleLevels.levels --players 1```

# How to Play:
- The game will initially display a player view upon starting the game.
- The game will prompt the player for moves by asking for an x-coordinate, and then a y-coordinate. Moves are in the form of ```(x_coordinate, y_coordinate)```
- If an incorrect move is detected, the game will prompt you for a new move.
- The game view will be updated after each player or adversary move.
- Updates will be sent to the view after every interaction. Interactions include finding the key, finding the exit, and being eliminated.
- Once the game is over, the player will be notified of their achievements.
