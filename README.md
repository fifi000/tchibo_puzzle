# tchibo_puzzle
The game is based on a physical one bought in Tchibo store. The original one is a wooden board with a set of colorful marble balls.

## Rules
The pieces move like in Checkers, so you can jump over another piece only if the field behind is free to take.
The overall goal is to end with a single ball on the center.

## Modes
* Basic 🔄 - you start with 32 balls and solve it such that you end with only a one piece 
* Rush Mode 🔥- here you start on level 2 (2 balls) and you go to the next level when you end with one ball, if you fail you have to manually reset the game
* Puzzle Mode 🧩 - in this mode you can specifie the number of balls you start with and play just like in normal mode

In both rush and puzzle mode you are guarantied that the board is solvable due to the algorithim which sets the balls.
The algorithim starts with a single ball in the center and makes reverse moves such that it moves a piece 2 fields away and adds a ball between fields. 
Here is example with moving ball 2 units to the right 'O - -' --> '- O O'

## Game Control
* undo/ redo
  * you can use either triangles on the screen or use keyboard arrows or A/D keys respectively
  * note: they will neither work during rush mode nor puzzle mode
* Basic 🔄
  * since nothing will happen when you end your attempt you can use either the restart button on the screen or press N (N - new game) to start a new classic game
* Rush Mode 🔥
  * use either the fire icon on the upper menu or press R
* Puzzle Mode 🧩
  * use either the puzzle icon on the upper menu or press P
* Help Message Box
  * to display a menu with keyboard shortcuts press H
* Loading game
  * when playing in normal mode the game will be saved in a folder `saved_games` when you end with small enough number of balls
  * after pressing L you can choose a file with saved game, then with undo/ redo buttons you can reconstruct your game
  * note: only positions of balls are saved so colors will statistically match once every 2^64 times

## Installation
