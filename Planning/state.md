# MEMORANDUM

### DATE: 2/5/2021
### TO: Instructors / TAs
### FROM: John Hassan & Marty Vo
### SUBJECT: Outsourced traveller-client module
------------------------------------------------------------------------------
## Snarl Data Definitions

A Character is one of:
- Player
- Adversary

A Game Space is one of:
- Room
- Hallway

State is one of:
- In Progress
- Over
* Variables:
    * Rooms (List)
    * Hallways (List)
    * Players (List)
    * Adversaries (List)
    * Levels (List)
    * State
        - Enumurated value or 'In Progress', 'Win' or 'Lose'
------------------------------------------------------------------------------
## Game State

The Game State will be updated/maintained by the following methods:

* CreateLevel ([Game Space]) -> Level
  - Creates a new level for the current game state
* LevelUp () -> Game State
  - Goes to next level after player has found exit
* Start () -> Game State
  - Game begins, Game is now In 'Progress'
* Restart () -> Game State
  - Game starts over at first level
* EndGame() -> Game State
  - When all players are eliminated or they have completed final level, update the State with 'Win' or 'Lose'
* ExitGame () -> Game State
  - Players exit game and it ends, State is now 'Win' or 'Lose'


* AddCharacter (Character, Destination) -> Game State
  * Adds a Character (Player or Adversary) to the Game State at the Destination
* Movement (Character, Destination) -> Game State
  - Moves a player to a given destination and updates game state
* ValidMove(Character, Destination) -> Boolean
  - Checks the validity of a move
* AcceptInteraction (Character, Tile) -> Game State
  - Responds to a movement by a Character
  - Includes finding key, player-adversary interactions
  - If there is another character in the tile, interaction takes place between them and given character
* ChangeTurn() -> Game State
  - Changes turn to next character