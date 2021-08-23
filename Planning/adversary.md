# Adversary Interface

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

A Adversary is an object containing at least a unique name (string), a position (Position), and a reference to the level in which it exists.

Adversary
- ShowMoves(Position): Position -> [Position]
  - Queries the Game Manager for the list of its valid moves.
- TakeTurn(Position): Position -> Game State
  - Adversaries will receive the list of player locations via RecievePlayerLocations() from the Game Manager.
  - Adversaries takes their turn and decides whether to move or not to move.
  - Adversaries can choose not to move, in which case their position does not change.
- GetPosition(): Adversary -> Position
  - Gets the Adversary’s current position.
- RecieveLevelUpdates():
  - Receives information from the Game Manager for updated information about the current level. 
- ReceivePlayerLocations():
  - Receives information from the Game Manager for updated information about player locations.
  - The Game Manager will only send player locations to the adversary when it's about to make a turn.
