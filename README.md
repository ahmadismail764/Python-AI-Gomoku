# Gomoku (Five in a Row)

A modern implementation of the classic Gomoku (Five in a Row) game with both console and GUI modes, featuring multiple AI algorithms.

![Gomoku Game](https://th.bing.com/th/id/OIP.bafHCcgs9k5HciPIzDO6-gHaEK?rs=1&pid=ImgDetMain)

## Features

- **Multiple Game Modes**:
  - Human vs Human
  - Human vs AI
  - AI vs AI (Watch and learn!)

- **Advanced AI Opponents**:
  - Minimax algorithm
  - Alpha-Beta pruning algorithm with optimized move evaluation

- **Customizable Settings**:
  - Adjustable board sizes (9x9, 13x13, 15x15, 19x19, or custom)
  - Custom player names and markers

- **User-Friendly Interface**:
  - Modern GUI with wooden theme
  - Console-based gameplay option
  - Comprehensive error handling and input validation
  - Move history highlighting

## Game Rules

Gomoku, also known as Five in a Row, is a traditional strategy board game. The rules are simple:

1. Players take turns placing stones on the board
2. The first player to form an unbroken chain of five stones (horizontally, vertically, or diagonally) wins
3. If the board fills up without a winner, the game is a draw

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - `customtkinter` (for GUI mode)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/username/python-ai-gomoku.git
   cd python-ai-gomoku
   ```

2. Install the required dependencies:
   ```bash
   pip install customtkinter
   ```

## How to Play

### GUI Mode

Run the game with the graphical user interface:

```bash
python gomoku_gui.py
```

1. Select a board size from the dropdown or enter a custom size
2. Choose a game mode (Human vs Human, Human vs AI, or AI vs AI)
3. Enter player names
4. If playing against AI, select an algorithm (Minimax or AlphaBeta)
5. Click on intersections to place your stones

### Console Mode

Run the game in console mode:

```bash
python main.py
```

1. Follow the on-screen prompts to select game mode and enter player information
2. Enter moves as coordinate pairs (row, column) when prompted

## AI Algorithms

### Minimax

The Minimax algorithm works by exploring all possible game states up to a certain depth. It assumes that both players play optimally:
- The AI maximizes its score
- The opponent minimizes the AI's score

Our implementation includes a sophisticated evaluation function that considers:
- Sequences of 2, 3, and 4 stones with open ends
- Defensive and offensive play balancing

### Alpha-Beta Pruning

The Alpha-Beta algorithm enhances Minimax by reducing the number of nodes evaluated. It maintains two values:
- Alpha: The minimum score the maximizing player is assured
- Beta: The maximum score the minimizing player is assured

This optimization allows for faster computation and deeper search depth.

## Project Structure

- `main.py` - Entry point for console mode
- `gomoku_gui.py` - GUI implementation using customtkinter
- `game_engine.py` - Core game logic and flow control
- `board.py` - Board representation and state management
- `player.py` - Base player class definition
- `minimax_ai.py` - Minimax AI implementation
- `alphabeta_ai.py` - Alpha-Beta pruning AI implementation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Special thanks to everyone who contributed to this project
- Inspired by the traditional Gomoku game and its many variants around the world
