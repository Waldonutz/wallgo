# WallGo - Strategic Board Game

## Overview
WallGo is a two-player abstract strategy game played on a 7x7 grid. Each player controls two pieces (Red vs Blue) and strategically moves them around the board, placing walls to block movement. The objective is to isolate all four pieces from each other by walling off their respective areas.

![WallGo Game](game_screenshot.png)

## Game Rules

### Setup
- Each player starts with 2 pieces placed on the board
- Players can choose initial positions or use the "Randomize" button
- No walls are placed at the start
- The outer edges of the board are considered permanent walls

### Gameplay

1. **Players:**  
   Two players (Red and Blue) alternate turns.

2. **Moving Pieces:**  
   On a player's turn, they must move one of their pieces:  
   - The piece can move 1 or 2 squares **orthogonally** (up, down, left, or right)
   - The piece can move in an **L-shape** (one step in one direction, then one step perpendicular)
   - The piece can **stay in place** (after a 2-second delay to prevent misclicks)
   - Diagonal moves are **not** allowed
   - Pieces cannot move through walls or off the board

3. **Placing Walls:**  
   After moving, the player must place a single wall on one of the grid lines adjacent to the moved piece's new position:  
   - Walls are placed along grid lines between two adjacent squares
   - Walls cannot be placed where a wall already exists
   - Walls block movement between adjacent squares

4. **Restrictions:**  
   - Players cannot move pieces through walls
   - The outer edges of the board act as permanent walls
   - Pieces that are completely isolated (in a 1x1 square) cannot be moved

### Winning Condition

- The game ends when **all four pieces** are each isolated from each other
- This means:
  - Red piece 1 cannot reach Red piece 2
  - Blue piece 1 cannot reach Blue piece 2
  - No red piece can reach any blue piece
- The player with the highest total of squares in their walled-off sections is declared the winner

## How to Run the Game

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/wallgo.git
   cd wallgo
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv wallgo_env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     wallgo_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source wallgo_env/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the game:
   ```
   python wallgo.py
   ```

## Game Controls

- **Setup Phase:**
  - Click on the board to place your pieces
  - Use the "Randomize Pieces" button for random placement

- **During Play:**
  - Click on one of your pieces to select it
  - Click on a highlighted cell to move the selected piece
  - After a 2-second delay, you can click on your current position to stay in place
  - After moving, click on a highlighted grid line to place a wall

- **General Controls:**
  - Click the "Restart Game" button to start a new game
  - Press F key to toggle FPS display

## Creating a Standalone Executable

You can create a standalone executable using PyInstaller:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Create the executable:
   ```
   pyinstaller --onefile --windowed --add-data "*.py:." wallgo.py
   ```

3. The executable will be created in the `dist` directory

## Features

- Intuitive graphical interface with visual feedback
- Automatic detection of valid moves and wall placements
- Visual indicators for isolated pieces
- Game state tracking and win condition detection
- Randomized piece placement option
- Restart game functionality

## Development

### Project Structure
- `wallgo.py` - Main game file and entry point
- `game_logic.py` - Game state and logic
- `renderer.py` - Visualization and rendering
- `requirements.txt` - Required Python packages

### Technologies Used
- Python 3
- Pygame for graphics and input handling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by classic abstract strategy games
- Developed as a programming exercise
