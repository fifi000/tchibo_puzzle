# tchibo_puzzle
The game is based on a physical one bought in Tchibo store. The original puzzle consists of a wooden board with a set of colorful marble balls.

## Screenshots
![](/readme_img/game_overview.png)
![](/readme_img/puzzle_mode.png)

## Rules
The pieces move according to the rules of Checkers, where you can jump over another piece only if the space behind it is free. The main goal is to end up with a single ball in the center.

## Modes
* Basic 🔄 - you start with 32 balls and the gole is to end with only one ball remaining.
* Rush Mode 🔥- here you start at level 2 (2 balls) and progress to the next level by ending with one ball. If you fail, you have to manually reset the game.
* Puzzle Mode 🧩 - This mode allows you to specify the number of balls you start with and play similarly to the normal mode.

In both Rush Mode 🔥 and Puzzle Mode 🧩 you are guaranteed that the board is solvable thanks to the algorithim that sets the balls. The algorithim starts with a single ball in the center and makes reverse moves, moving a piece 2 fields away and adding a ball between the fields. Here is an example of moving a ball 2 units to the right: 'O - -' --> '- O O'
Since the algorithim makes random moves when creating the board (in special modes) there is no guarantee that e.g. at the level 30 during Rush Mode 🔥 there will be 30 balls because there may not be any valid move to put more balls using the decribed above rule.

## Game Control
* Undo/Redo
  * you can use either triangles on the screen or use keyboard arrows or A/D keys respectively
  * note: Undo/redo actions are disabled in Rush Mode 🔥 and Puzzle Mode 🧩
* Basic Mode 🔄
  * since nothing will happen when you end your attempt, you can either use the restart button on the screen or press 'N' (N - new game) to start a new classic game
* Rush Mode 🔥
  * use either the fire icon on the upper menu or press 'R'
* Puzzle Mode 🧩
  * use either the puzzle icon on the upper menu or press 'P'
* Help Message Box
  * to display a menu with keyboard shortcuts, press 'H'
* Loading game
  * when playing in Basic Mode 🔄 the game will be saved in a folder `saved_games` when you end with a small enough number of balls
  * after pressing 'L' you can choose a file with a saved game, then using undo/ redo buttons you can reconstruct your game
  * note: only positions of balls are saved, so colors will statistically match once every 2^64 times

## Installation
After cloning the git repo and optionally creating venv
1. install dependencies
```bash
pip install -r requirements.txt
```
2. run game
```bash
python main.py
```
