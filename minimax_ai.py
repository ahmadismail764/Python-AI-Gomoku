from player import Player
from board import Board
from ai_utils import GomokuAIEvalMixin, DIRECTIONS


class MinimaxAI(Player, GomokuAIEvalMixin):
    def __init__(self, name: str, mark: str, opponent_mark: str, max_depth: int = 3):
        super().__init__(name, mark)
        self.opponent_mark = opponent_mark
        self.max_depth = max_depth

    def get_move(self, game_state: Board):
        print("AI is thinking...")
        _, move = self._minimax(game_state, True, self.max_depth)
        return move

    def get_best_valid_moves(self, board: Board):
        moves = set()
        has_stone = False
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != ".":
                    has_stone = True
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if (
                                0 <= nr < board.size
                                and 0 <= nc < board.size
                                and board.grid[nr][nc] == "."
                            ):
                                moves.add((nr, nc))
        if not has_stone:
            moves.add((int(board.size / 2), int(board.size / 2)))
        return list(moves)

    def _minimax(self, board: Board, is_max: bool, depth: int):
        valid_moves = self.get_best_valid_moves(board)
        if depth == 0 or not valid_moves:
            return self.evaluate(board), None
        best_move = None
        if is_max:
            best_val = float("-inf")
            for x, y in valid_moves:
                board.apply_move(x, y, self.mark)
                if self.is_win(board, self.mark):
                    board.undo_move(x, y)
                    best_move = (x, y)
                    return 1_000_000, best_move
                eval_score, _ = self._minimax(board, False, depth - 1)
                board.undo_move(x, y)
                if eval_score > best_val:
                    best_val, best_move = eval_score, (x, y)
            return (best_val, best_move)
        else:
            best_val = float("inf")
            for x, y in valid_moves:
                board.apply_move(x, y, self.opponent_mark)
                if self.is_win(board, self.opponent_mark):
                    board.undo_move(x, y)
                    best_move = (x, y)
                    return -1_000_000, best_move
                val, _ = self._minimax(board, True, depth - 1)
                board.undo_move(x, y)
                if val < best_val:
                    best_val, best_move = val, (x, y)
            return (best_val, best_move)
