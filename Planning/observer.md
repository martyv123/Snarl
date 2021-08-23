# Observer

## Interface

DisplayLevel() - None -> String
- Displays the current level in ASCII format.

Update() - None -> None
- Receives updates from game state and updates the observer's views accordingly.
  
GetPlayers() - None -> List[Player]
- Returns all players and player names in the game.

GetAdversaries() - None -> List[Adversaries]
- Returns all adversaries in the game.

GetLevels() - None -> List[Level]
- Returns all the levels in the game.

GetCurrentLevel() - None -> Level
- Returns the current level that the players are playing.

GetGameState() - None -> Status
- Returns the current game status which is either IN_PROGRESS or OVER.


## Example View

Here is an observer's view of the game at initialization. There is one player and one adversary in this game. Traversable tiles are marked by "." and "/", with "/" representing doorways into or out of hallways. "+" will represent the key to the level exit, and "o" will represent the level exit. "X" marks untraversable tiles.

```
XXXXXXXXXXXX
XP../...XXXX 
X...XXX.XXXX 
X...XXX.XXXX 
XXXXXXX.XXXX 
XXXXXXX.XXXX 
XXXXXXX/XXXX 
XXXXXXX+..XX 
XXXXXXXo..XX 
XXXXXXX..AXX 
XXXXXXXXXXXX 
XXXXXXXXXXXX 
```

The observer's view will change upon events happening in the game. These events mean player or adversary movement, player or adversary interactions, and the completion of a level or the game. The view below depicts a player moving two tiles to the left during their turn.

```
XXXXXXXXXXXX 
X..P/...XXXX 
X...XXX.XXXX 
X...XXX.XXXX 
XXXXXXX.XXXX 
XXXXXXX.XXXX 
XXXXXXX/XXXX 
XXXXXXX+..XX 
XXXXXXXo..XX 
XXXXXXX..AXX 
XXXXXXXXXXXX 
XXXXXXXXXXXX 
```

The observer's view below depicts an adversary moving one tile up during their turn.

```
XXXXXXXXXXXX  
X..P/...XXXX  
X...XXX.XXXX  
X...XXX.XXXX  
XXXXXXX.XXXX 
XXXXXXX.XXXX  
XXXXXXX/XXXX  
XXXXXXX+..XX  
XXXXXXXo.AXX  
XXXXXXX...XX 
XXXXXXXXXXXX 
XXXXXXXXXXXX 
```

...

The observer's view below depicts the player finding the key to the level exit. The key will no longer be displayed in the observer's view. If a player moves from the tile containing the key after it was picked up, that tile will appear as a walkable tile.

```
XXXXXXXXXXXX  
X.../...XXXX  
X...XXX.XXXX  
X...XXX.XXXX  
XXXXXXX.XXXX 
XXXXXXX.XXXX  
XXXXXXX/XXXX  
XXXXXXXP..XX  
XXXXXXXo.AXX  
XXXXXXX...XX 
XXXXXXXXXXXX 
XXXXXXXXXXXX 
```

The observer's view below depicts the player finding the level exit. Once the game state updates, the observer will be notified that the level has been completed. 

```
XXXXXXXXXXXX  
X.../...XXXX  
X...XXX.XXXX  
X...XXX.XXXX  
XXXXXXX.XXXX 
XXXXXXX.XXXX  
XXXXXXX/XXXX  
XXXXXXX...XX  
XXXXXXXP.AXX  
XXXXXXX...XX 
XXXXXXXXXXXX 
XXXXXXXXXXXX
``` 

Once the level has been completed, the observer will receive a notification that the level is over.

```
This level has been completed!
```

If the game has been completed, the observer will also receive a notification with information about how the game has ended.

Message 1
```
The game is over! All players have successfully escaped all adversaries.
```

Message 2
```
The game is over! All players have been eliminated by the adversaries.
```
