DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [["." for _ in range(size)] for _ in range(size)]

    def display(self):
        col_headers = "    " + " ".join(f"{i:2}" for i in range(self.size))
        print(col_headers)
        for i, row in enumerate(self.grid):
            row_str = " ".join(f"{cell:2}" for cell in row)
            print(f"{i:2} | {row_str}")
        print()

    def is_valid_move(self, x, y):
        in_bound = 0 <= x < self.size and 0 <= y < self.size
        free_cell = self.grid[x][y] == "."
        return in_bound and free_cell

    def apply_move(self, x: int, y: int, mark: str) -> None:
        """Apply a move to the board if valid."""
        if self.is_valid_move(x, y):
            self.grid[x][y] = mark

    def undo_move(self, x: int, y: int) -> None:
        """Undo a move at the given coordinates."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = "."

    def is_winner(self, mark):
        for r in range(self.size):
            for c in range(self.size):
                for dr, dc in DIRECTIONS:
                    coords = []
                    for k in range(5):
                        nr, nc = r + dr * k, c + dc * k
                        if (
                            0 <= nr < self.size
                            and 0 <= nc < self.size
                            and self.grid[nr][nc] == mark
                        ):
                            coords.append((nr, nc))
                        else:
                            break
                    if len(coords) == 5:
                        return coords
        return None

    def draw(self):
        for row in self.grid:
            if "." in row:
                return False
        return True

    def reset(self):
        self.grid = [["." for _ in range(self.size)] for _ in range(self.size)]
