from player import Player
from board import Board
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

class AlphaBetaAI(Player):
    def __init__(self, name: str, mark: str, opponent_mark: str, max_depth: int = 3, move_limit: int = 10):
        super().__init__(name, mark)
        self.opponent_mark = opponent_mark
        self.max_depth = max_depth
        self.move_limit = move_limit

    def get_move(self, game_state: Board):
        print('AI is thinking...')
        alpha = float('-inf')
        beta = float('inf')
        _ ,move =self._alphabeta(game_state, self.max_depth , True, alpha, beta)
        return move

    def _alphabeta(self, board: Board, depth: int, is_max: bool, alpha: float, beta: float):

        valid_moves= self.get_best_valid_moves(board)
        if depth == 0 or not valid_moves:
            return self.evaluate(board), None

        best_move = None
        if is_max:
            best_val = float('-inf')
            for x, y in valid_moves:
                board.apply_move(x, y, self.mark)

                if self.is_win(board, self.mark):
                    board.grid[x][y] = '.'
                    best_move = (x, y)
                    return 1_000_000, best_move

                eval_score, _ = self._alphabeta(board, depth - 1, False, alpha, beta)
                board.grid[x][y] = '.'
                if eval_score > best_val:
                    best_val = eval_score
                    best_move =  (x, y)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return best_val, best_move
        else:
            best_val = float('inf')
            for x, y in valid_moves:
                board.apply_move(x, y, self.opponent_mark)

                if self.is_win(board, self.opponent_mark):
                    board.grid[x][y] = '.'
                    best_move = (x, y)
                    return -1_000_000, best_move

                eval_score, _ = self._alphabeta(board, depth - 1, True, alpha, beta)
                board.grid[x][y] = '.'
                if eval_score < best_val:
                    best_val, best_move = eval_score, (x, y)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return (best_val, best_move)

    def is_win(self,board: Board,Mark):
        return board.is_winner(Mark)

    def count_open_seq(self,board: Board,Mark, length):
        count = 0
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != Mark:
                    continue
                for dr, dc in DIRECTIONS:
                    seq = []
                    for k in range(length):
                        nr, nc = r + dr * k, c + dc * k
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            seq.append(board.grid[nr][nc])
                        else:
                            break
                    if len(seq) == length and all(x == Mark for x in seq):
                        # Check for open ends
                        before_r, before_c = r - dr, c - dc
                        after_r, after_c = r + dr * length, c + dc * length
                        before_open = (0 <= before_r < board.size and 0 <= before_c < board.size and board.grid[before_r][
                            before_c] =='.')
                        after_open = (0 <= after_r < board.size and 0 <= after_c < board.size and board.grid[after_r][after_c] == '.')
                        if before_open or after_open:
                            count += 1
        return count

    def evaluate(self,board: Board):
        score = 0

        # Heuristic: open 2, open 3, open 4
        score += 10 * self.count_open_seq(board, self.mark, 2)
        score += 100 * self.count_open_seq(board, self.mark, 3)
        score += 1000 * self.count_open_seq(board, self.mark, 4)

        score -= 12 * self.count_open_seq(board, self.opponent_mark, 2)
        score -= 120 * self.count_open_seq(board, self.opponent_mark, 3)
        score -= 1000 * self.count_open_seq(board, self.opponent_mark, 4)

        return score

    def get_best_valid_moves(self,board):
        moves = set()
        has_stone = False
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != '.':
                    has_stone = True
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < board.size and 0 <= nc < board.size and board.grid[nr][nc] == '.':
                                moves.add((nr, nc))
        if not has_stone:
            # If board is empty, allow all moves
                        moves.add((int(board.size/2), int (board.size/2)))
        return list(moves)