from player import Player
from board import Board

class AlphaBetaAI(Player):
    def __init__(self, name: str, mark: str, opponent_mark: str, max_depth: int = 3):

        super().__init__(name, mark)
        self.opponent_mark = opponent_mark
        self.max_depth = max_depth

    def get_move(self, game_state: Board):

        _, move = self._alphabeta(game_state, True, 0, float('-inf'), float('inf'))
        return move

    def _alphabeta(self, board: Board, is_maximizing: bool, depth: int, alpha: float, beta: float):
        # Terminal state checks
        if board.is_winner(self.mark):
            return (float('inf'), None)
        if board.is_winner(self.opponent_mark):
            return (float('-inf'), None)
        if board.draw() or depth >= self.max_depth:
            return (0, None)

        best_move = None
        moves = self._filtered_moves(board)

        if is_maximizing:
            value = float('-inf')
            for x, y in moves:
                board.apply_move(x, y, self.mark)
                score, _ = self._alphabeta(board, False, depth + 1, alpha, beta)
                board.grid[x][y] = '.'  # undo move
                if score > value:
                    value, best_move = score, (x, y)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # beta cut-off
            return value, best_move
        else:
            value = float('inf')
            for x, y in moves:
                board.apply_move(x, y, self.opponent_mark)
                score, _ = self._alphabeta(board, True, depth + 1, alpha, beta)
                board.grid[x][y] = '.'  # undo move
                if score < value:
                    value, best_move = score, (x, y)
                beta = min(beta, value)
                if beta <= alpha:
                    break  # alpha cut-off
            return value, best_move

    def _filtered_moves(self, board: Board):

        neighbors = set()
        # Center move if board empty
        if all(cell == '.' for row in board.grid for cell in row):
            mid = board.size // 2
            return [(mid, mid)]

        radius = 2
        for i in range(board.size):
            for j in range(board.size):
                if board.grid[i][j] != '.':
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            x, y = i + dx, j + dy
                            if (0 <= x < board.size and 0 <= y < board.size
                                and board.grid[x][y] == '.'):
                                neighbors.add((x, y))
        return list(neighbors)
