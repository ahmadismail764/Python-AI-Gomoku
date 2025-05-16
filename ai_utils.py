from player import Player
from board import Board

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


class GomokuAIEvalMixin:
    """Mixin for shared AI evaluation logic."""

    def is_win(self, board: Board, mark: str) -> bool:
        return board.is_winner(mark)

    def count_open_seq(self, board: Board, mark: str, length: int) -> int:
        count = 0
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != mark:
                    continue
                for dr, dc in DIRECTIONS:
                    seq = []
                    for k in range(length):
                        nr, nc = r + dr * k, c + dc * k
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            seq.append(board.grid[nr][nc])
                        else:
                            break
                    if len(seq) == length and all(x == mark for x in seq):
                        # Check for open ends
                        before_r, before_c = r - dr, c - dc
                        after_r, after_c = r + dr * length, c + dc * length
                        before_open = (
                            0 <= before_r < board.size
                            and 0 <= before_c < board.size
                            and board.grid[before_r][before_c] == "."
                        )
                        after_open = (
                            0 <= after_r < board.size
                            and 0 <= after_c < board.size
                            and board.grid[after_r][after_c] == "."
                        )
                        if before_open or after_open:
                            count += 1
        return count

    def evaluate(self, board: Board) -> int:
        score = 0
        score += 10 * self.count_open_seq(board, self.mark, 2)
        score += 100 * self.count_open_seq(board, self.mark, 3)
        score += 1000 * self.count_open_seq(board, self.mark, 4)
        score -= 12 * self.count_open_seq(board, self.opponent_mark, 2)
        score -= 120 * self.count_open_seq(board, self.opponent_mark, 3)
        score -= 1000 * self.count_open_seq(board, self.opponent_mark, 4)
        return score
