from board import Board


class Player:
    def __init__(self, name: str, mark: str, is_ai: int = 0):
        self.name = name
        self.mark = mark  # The mark the player puts on the board, character
        self.is_ai = is_ai  # 0 for human, 1 for Minimax, 2 for Alpha-Beta pruning

    def get_move(self, game_state: Board = None):
        if not self.is_ai:
            x, y = map(
                int, input(f"{self.name}, enter your move (row, column): ").split()
            )
            return (x, y)
        elif self.is_ai == 1:
            # Minimax logic to choose a move
            # Import locally to avoid circular dependencies
            from minimax_ai import MinimaxAI

            ai_agent = MinimaxAI(self.name, self.mark)
            return ai_agent.get_move(game_state)
        else:
            from alphabeta_ai import AlphaBetaAI

            ai_agent = AlphaBetaAI(self.name, self.mark)
            return ai_agent.get_move(game_state)
