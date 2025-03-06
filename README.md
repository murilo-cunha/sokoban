# Sokoban Game with Pyxel

A simple implementation of the classic Sokoban puzzle game using [Pyxel](https://github.com/kitao/pyxel), a retro game engine for Python.

## About Sokoban

Sokoban (倉庫番, "warehouse keeper") is a puzzle game where the player pushes boxes around a warehouse, trying to get them to designated storage locations.

## Game Rules

- Use arrow keys to move the player character
- Push boxes onto target spots
- You cannot pull boxes, only push them
- Complete the level by placing all boxes on target spots
- Press 'R' to restart the current level
- After completing a level, press 'N' to move to the next level

## Setup and Running

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the game:
   ```
   python sokoban.py
   ```

## Game Controls

- **Arrow Keys**: Move the player
- **R**: Restart the current level
- **N**: Go to next level (after completion)

## Game Elements

- Blue squares: Walls
- Green circles: Target spots
- Red squares: Boxes
- Light blue squares: Boxes on target spots
- Yellow square: Player

## Adding More Levels

You can add more levels by extending the `levels` list in the `Sokoban` class. 
Use these values to define your custom levels:
- 0: Empty space
- 1: Wall
- 2: Player starting position
- 3: Box
- 4: Target
- 5: Box on target (initial state)
