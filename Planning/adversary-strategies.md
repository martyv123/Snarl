# Adversary Strategies

Adversaries in the game of Snarl will have automated moves that are determined by an algorithm. Currently, there are two adversary types: zombies and ghosts. Zombies are confined to the room that they are intially placed in. They can only move one tile in either cardinal direction (assuming that the destination is a valid tile) and cannot move onto wall tiles or into hallways. Zombies will react to a player in their vicinity by moving closer to the player. If there are multiple players within the vicinity of a zombie, the zombie will move closer to the closest player. Ghosts will follow the same movement patterns in either cardin direction, but can enter wall tiles and hallways. If a ghost lands on a wall tile, they will be moved to a random room onto a random tile.


## Example Situations & Outcomes

1. No players within the vicinity of any adversary
    - Both zombie and ghost types will randomly select a move from its list of valid moves. 

2. One player is within the vicinity of a zombie type adversary
    - The zombie will choose the move from its list of valid moves that puts it closest to the player. This includes moving onto the same tile as the player and therefore eliminating them.

3. Multiple players are within the vicinity of a zombie type adversary
    - The zombie will choose the move from its list of valid moves that puts it closest to the closest player. This includes moving onto the same tile as the player and therefore eliminating them.

4. One player is within the vicinity of a ghost type adversary
    - The ghost will choose the move from its list of valid moves that puts it closest to the player. This includes moving onto the same tile as the player and therefore eliminating them. If the closest move will place the ghost onto a wall tile, then the ghost will be transported to a random room onto a random tile. 

5. Multiple players are within the vicinity of a ghost type adversary
    - The ghost will choose the move from its list of valid moves that puts it closest to the closest player. This includes moving onto the same tile as the player and therefore eliminating them. If the closest move will place the ghost onto a wall tile, then the ghost will be transported to a random room onto a random tile. 