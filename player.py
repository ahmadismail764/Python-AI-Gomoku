class Player:
    def __init__(self, name: str, mark: str, is_ai: int = 0):
        self.name = name
        self.mark = mark  # The mark the player puts on the board, character
        self.is_ai = is_ai  # 0 for human, 1 for Minimax, 2 for Alpha-Beta pruning

    def get_move(self):
        if not self.is_ai:
            x, y = map(
                int, input(f"{self.name}, enter your move (row, column): ").split()
            )
            return (x, y)
        elif self.is_ai == 1:
            # Minimax logic to choose a move
            return (0, 0)
        else:
            # Alpha-Beta pruning logic to choose a move
            return (1, 1)
