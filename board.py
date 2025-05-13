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

    def apply_move(self, x, y, mark):
        if self.is_valid_move(x, y):
            self.grid[x][y] = mark

    def is_winner(self, mark):
        # Horizontal
        for r in range(self.size):
            for c in range(self.size - 4):
                if all(self.grid[r][c + i] == mark for i in range(5)):
                    return True
        # Vertical
        for r in range(self.size - 4):
            for c in range(self.size):
                if all(self.grid[r + i][c] == mark for i in range(5)):
                    return True
        # Diagonal bottom-left to top-right
        for r in range(self.size - 4):
            for c in range(self.size - 4):
                if all(self.grid[r + i][c + i] == mark for i in range(5)):
                    return True
        # Diagonal top-left to bottom-right
        for r in range(self.size - 4):
            for c in range(4, self.size):
                if all(self.grid[r + i][c - i] == mark for i in range(5)):
                    return True
        return False

    def draw(self):
        for row in self.grid:
            if "." in row:
                return False
        return True

    def getAvailableMoves(self):
        available_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == ".":
                    available_moves.append((i, j))
        return available_moves

    def reset(self):
        self.grid = [["." for _ in range(self.size)] for _ in range(self.size)]
