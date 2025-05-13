from player import Player
from board import Board


class MinimaxAI(Player):
    def __init__(self, name: str, mark: str, opponent_mark: str, max_depth: int = 3):
        super().__init__(name, mark)
        self.opponent_mark = opponent_mark
        self.max_depth = max_depth

    def get_move(self, game_state: Board):
        """
        Chooses best move by running Minimax on game_state (Board).
        """
        _, move = self._minimax(game_state, True, 0)
        return move

    def _minimax(self, board: Board, is_maximizing: bool, depth: int):
        # Terminal state checks
        if board.is_winner(self.mark):
            return (1, None)
        if board.is_winner(self.opponent_mark):
            return (-1, None)
        if board.draw() or depth >= self.max_depth:
            return (0, None)

        best_move = None
        moves = self._filtered_moves(board)

        if is_maximizing:
            best_value = float("-inf")
            for x, y in moves:
                board.apply_move(x, y, self.mark)
                value, _ = self._minimax(board, False, depth + 1)
                # undo move
                board.grid[x][y] = "."
                if value > best_value:
                    best_value, best_move = value, (x, y)
            return best_value, best_move
        else:
            best_value = float("inf")
            for x, y in moves:
                board.apply_move(x, y, self.opponent_mark)
                value, _ = self._minimax(board, True, depth + 1)
                # undo move
                board.grid[x][y] = "."
                if value < best_value:
                    best_value, best_move = value, (x, y)
            return best_value, best_move

    def _filtered_moves(self, board: Board):
        neighbors = set()
        # consider empty board case: allow center
        if all(cell == "." for row in board.grid for cell in row):
            mid = board.size // 2
            return [(mid, mid)]
        # define neighborhood radius
        radius = 2
        for i in range(board.size):
            for j in range(board.size):
                if board.grid[i][j] != ".":
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            x, y = i + dx, j + dy
                            if (
                                0 <= x < board.size
                                and 0 <= y < board.size
                                and board.grid[x][y] == "."
                            ):
                                neighbors.add((x, y))
        return list(neighbors)
