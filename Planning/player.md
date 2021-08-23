# Player Interface

## Data Definitions

A Position is a:
- (int, int) <br>

A Character is one of:
- Player
- Adversary <br>

A Game Space is one of:
- Level
- Room
- Hallway <br>

A Game State is one of:
- In Progress
- Over <br>

## Interface

A Player is an object containing at least a name (string), position (Position), and status (boolean). The status determines whether a Player is still active in the current Level. 

Player
- ShowMoves(Position): Position -> [Position]
  - Query the Game Manager for the list of valid next moves.
- TakeTurn(Position): Position -> Game State
  - Player takes their turn and decides to move or not to move.
  - Players can choose not to move, in which case their Position does not change.
  - This information is sent to the Game Manager.
- GetPosition(): Player -> Position
  - Get the Player’s current position.
- GetStatus(): Player -> Boolean
  - Returns a boolean determining whether or not the Player is currently active in the game’s current level.
