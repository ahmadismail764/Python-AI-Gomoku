from board import Board


class Player:
    def __init__(self, name: str, mark: str):
        self.name = name
        self.mark = mark

    def get_move(self, game_state: Board = None):
        """Prompt the user for a move and validate input."""
        while True:
            try:
                move_str = input(f"{self.name}, enter your move (row, column): ")
                parts = move_str.replace(",", " ").split()
                if len(parts) != 2:
                    raise ValueError
                x, y = int(parts[0]), int(parts[1])
                if not game_state or game_state.is_valid_move(x, y):
                    return (x, y)
                else:
                    print(f"Cell ({x}, {y}) is not available. Try again.")
            except Exception:
                print(
                    "Invalid input. Please enter two integers separated by space or comma (e.g., 7 8 or 7,8). Try again."
                )
