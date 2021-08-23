# Rule Checker

## Data Definitions
A Character is one of:
- Player
- Adversary

A Game Space is one of:
- Room
- Hallway

State is one of:
- In Progress
- Over

## Interface
valid_game_state(Game) -> Boolean
- Checks that there are no more than 4 Players in a Game at once, and that there are active Players if the Game is not over, or if there are no active Players that the Game is over. Players and adversaries must be on walkable tiles.
  
valid_level(Level) -> Boolean
- Checks if the given level is valid by checking if there exists a key and an exit for the Level and if the no hallways and rooms overlap.

valid_movement(Character, Destination) -> Boolean
- Checks the validity of a move for a Character, returns True or False depending on if the move is valid

valid_interaction(Character) -> Boolean
- Checks if the Player's interaction at their location is valid. The interaction is valid if the object is a key, unlocked exit, or Adversary. Invalid objects are other Players. 

check_end_of_level() -> Boolean
- Checks if the end of the Level has been reached (key and exit found) and returns True or False

check_end_of_game() -> Boolean
- Checks if the end of the Game has occured when all Players are eliminated in a Level or if the last Level of the Game has been completed. When end_of_game() returns True, end_of_level() will return True as well. 