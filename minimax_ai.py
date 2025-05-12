from player import Player
from board import Board

class MinimaxAI(Player):
    def __init__(self, name: str, mark: str, max_depth: int = 5):
        super().__init__(name, mark, is_ai=1)
        self.max_depth = max_depth

    def get_move(self, game_state: Board):
        """
        Returns the best move as (row, col) using Minimax with Alpha-Beta pruning.
        """
        _, move = self._minimax(game_state, True, 0, float('-inf'), float('inf'))
        return move

    def _minimax(self, board: Board, is_maximizing: bool, depth: int, alpha: float, beta: float):
        # Terminal checks
        if board.is_winner(self.mark):
            return (1, None)
        opponent_mark = 'O' if self.mark == 'X' else 'X'
        if board.is_winner(opponent_mark):
            return (-1, None)
        if board.draw() or depth >= self.max_depth:
            return (0, None)

        best_move = None
        moves = self._filtered_moves(board)

        if is_maximizing:
            value = float('-inf')
            for move in moves:
                x, y = move
                board.apply_move(x, y, self.mark)
                score, _ = self._minimax(board, False, depth + 1, alpha, beta)
                board.grid[x][y] = '.'
                if score > value:
                    value, best_move = score, move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff
            return value, best_move
        else:
            value = float('inf')
            for move in moves:
                x, y = move
                board.apply_move(x, y, opponent_mark)
                score, _ = self._minimax(board, True, depth + 1, alpha, beta)
                board.grid[x][y] = '.'
                if score < value:
                    value, best_move = score, move
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return value, best_move

    def _filtered_moves(self, board: Board):
        """
        Return only moves near existing stones to reduce branching.
        """
        neighbors = set()
        directions = [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(-2,2),(2,-2),(2,2)]
        for i in range(board.size):
            for j in range(board.size):
                if board.grid[i][j] != '.':
                    for dx, dy in directions:
                        x, y = i + dx, j + dy
                        if 0 <= x < board.size and 0 <= y < board.size and board.grid[x][y] == '.':
                            neighbors.add((x,y))
        return list(neighbors) if neighbors else board.getAvailableMoves()
