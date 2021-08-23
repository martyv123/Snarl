# Milestone 6 - Refactoring Report

**Team members:**
John Hassan and Marty Vo

**Github team/repo:**
https://github.ccs.neu.edu/CS4500-S21/Olindond

## Plan

For refactoring, our group is focusing on fixing some discrepancies between the JSON input for a game representation and our internal game representation, our placement of adversaries and players, and fully moving the rulechecker and game manager interfaces into their seperate modules. Currently, the rulechecker and the game manager have codependencies in our game module that we will be removing during this refactoring stage.

## Changes

- GameManager and RuleChecker
  - Both the GameManager and RuleChecker interfaces were seperated from the Game module and now exist as their own seperate modules. No codependencies exist between the modules now, and both the GameManager and RuleChecker are instantiated as their own instances.

- place_players and place_adversaries
  - These functions have been deprecated and are only to be used for testing purposes. The reason for this is that actors (players and adversaries) cannot occupy tiles that are currently occupied by another actor.


## Future Work

In the future, if time allows, we plan to abstract classes and data representations that share the same common functionality into parent classes and use inheritance to specify different behavior across different data representations. This will allow for easier addition of different actors and game features.


## Conclusion

There is more we could have refactored, but we decided to use this week as a breather because we both have other courses that are requiring a significant amount of our time as well. We appreciate the ability to look back and reflect on our code, and will make use of this refactoring to produce a cleaner code base.