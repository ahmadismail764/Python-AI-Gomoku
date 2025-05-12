from player import Player


class AlphaBetaAI(Player):
    def __init__(self, name: str, mark: str):
        super().__init__(name, mark)

    def get_move(self):
        # Implement AlphaBeta logic to choose a move
        return (0, 0)  # Placeholder for now
