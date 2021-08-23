# Game Manager Interface

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

The Game Manager will represent an interface that allows for communication between the Player and the Game State. This communication involves moving the Player, interactions involving the Player, and other functions necessary to facilitate progress

Game Manager
- AcceptPlayer(Player): Player -> Game State
  - Accepts a player into the game given that their name is unique and there are less than 4 players currently in the game.
- AcceptMovement(Position, Player): Position, Player -> Game State
  - Accepts an movement taken by a Player on their turn and moves the player if the move is valid.
- AcceptInteraction(Player): Player -> Game State
  - Accepts an interaction by the Player at their current position. An interaction could be a player interacting with an adversary, key, or exit.
- StartGame(): None -> Game State
  - Begins the game at the first Level.
- CurrentPlayerTurn(): Game State -> Game State
  - Retrieve which Player’s turn it is. The Game Manager will not accept movements or interactions during the turn of another Player other than the current Player’s turn.
- PlayerTurnNotification(Player): Player -> Game State
  - Send a notification to the Player indicating that it is their turn to move.
- SendPlayerMoves(Player): Player -> Position
  - Send the list of valid moves for the Player back to the Player
