# Gomoku (Five in a Row) 🧩

A modern, feature-rich Python implementation of the classic Gomoku game (Five in a Row), offering both a sleek GUI and console mode. Play against friends or challenge advanced AI opponents powered by Minimax and Alpha-Beta algorithms! 🧠

![Gomoku Board](https://th.bing.com/th/id/OIP.bafHCcgs9k5HciPIzDO6-gHaEK?rs=1&pid=ImgDetMain)

---

## 🚀 Features

- **Multiple Game Modes:**  
  - Human vs Human  
  - Human vs AI  
  - AI vs AI (watch the bots battle!)

- **Smart AI Opponents:**  
  - Minimax algorithm  
  - Alpha-Beta pruning for faster, deeper strategy

- **Customizable Gameplay:**  
  - Choose board sizes (9x9, 13x13, 15x15, 19x19, or custom)  
  - Set player names and markers

- **User-Friendly Interface:**  
  - Modern GUI (wooden theme)  
  - Console mode for terminal fans  
  - Move history & error handling

---

## 🎮 How to Play

### GUI Mode

```powershell
python gomoku_gui.py
```

- Select board size and game mode
- Enter player names
- Choose AI algorithm (if applicable)
- Click intersections to place stones

### Console Mode

```powershell
python main.py
```

- Follow prompts for setup and moves

---

## 🧩 AI Algorithms

- **Minimax:** Explores possible moves to maximize AI’s chance of winning, considering both offensive and defensive strategies.
- **Alpha-Beta Pruning:** Optimizes Minimax by skipping unnecessary moves, allowing deeper and faster decision-making.

---

## 📁 Project Structure

- `main.py` — Console mode entry point
- `gomoku_gui.py` — GUI implementation
- `game_engine.py` — Game logic and flow
- `board.py` — Board state management
- `player.py` — Player classes
- `minimax_ai.py` — Minimax AI logic
- `alphabeta_ai.py` — Alpha-Beta AI logic
- `ai_utils.py` — Shared AI evaluation logic

---

## 🗂️ Class Overview

Below is a simple text-based class overview for the main components of this project:

```
Board
 ├─ display()
 ├─ is_valid_move(x, y)
 ├─ apply_move(x, y, mark)
 ├─ undo_move(x, y)
 ├─ is_winner(mark)
 ├─ draw()
 └─ reset()

Player
 ├─ name
 ├─ mark
 └─ get_move(game_state)

GomokuAIEvalMixin
 ├─ is_win(board, mark)
 ├─ count_open_seq(board, mark, length)
 └─ evaluate(board)

MinimaxAI (inherits Player, GomokuAIEvalMixin)
 ├─ get_move(game_state)
 └─ get_best_valid_moves(board)

AlphaBetaAI (inherits Player, GomokuAIEvalMixin)
 ├─ get_move(game_state)
 └─ get_best_valid_moves(board)
```

- `MinimaxAI` and `AlphaBetaAI` both inherit from `Player` and mix in shared AI logic from `GomokuAIEvalMixin`.
- All classes interact with the `Board` for game state and moves.

---

## ⚡ Quickstart

1. **Clone the repo:**

   ```powershell
   git clone https://github.com/username/python-ai-gomoku.git
   cd python-ai-gomoku
   ```

2. **Install dependencies:**

   ```powershell
   pip install customtkinter
   ```

3. **Run the game:**  
   - GUI: `python gomoku_gui.py`  
   - Console: `python main.py`

---

## 🤝 Contributing

Contributions, suggestions, and pull requests are welcome!

---

## 🌏 Acknowledgments

Inspired by the timeless Gomoku game and the global community of board game enthusiasts.

---
