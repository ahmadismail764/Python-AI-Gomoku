from player import Player
from board import Board


class MinimaxAI(Player):
    def __init__(self, name: str, mark: str):
        super().__init__(name, mark, is_ai=1)

    def get_move(self, game_state):
        # Implement Minimax logic to choose a move
        return (0, 0)  # Placeholder for now
