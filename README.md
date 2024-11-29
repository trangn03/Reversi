# Reversi Game

A two-player deterministic board game where players compete to capture the opponent's discs by strategically placing their own on a grid.

## Features

- **Single-player mode:** Compete against a challenging AI opponent powered by the Minimax algorithm with alpha-beta pruning.
- **Two-player mode:** Play against a friend locally.
- **Dynamic gameplay:** The AI evaluates game states recursively to maximize its chances of winning while minimizing the opponent's, ensuring competitive and engaging gameplay.

## Gameplay Rules

1. Players take turns placing their discs (black or white) on the board.
2. A move is valid if it captures one or more of the opponent's discs by enclosing them in a straight line (horizontally, vertically, or diagonally).
3. Captured discs are flipped to the player's color.
4. The game ends when neither player can make a valid move.
5. The player with the most discs of their color on the board wins.

## Technology

- **Language:** Python
- **AI Algorithm:** Minimax algorithm with alpha-beta pruning for optimal AI decision-making.

## Installation
1. Ensure you have Python installed on your system (version 3.x or above).
2. Clone this repository:
   ```bash
   git clone https://github.com/trangn03/Reversi.git
3. Navigate to the project directory:
    ```bash
    cd Reversi
4. Run the game
    ```bash
    cd python reversi.py
