from board import Board


class Player:
    def __init__(self, name: str, mark: str):
        self.name = name
        self.mark = mark

    def get_move(self, game_state: Board = None):
        x, y = map(int, input(f"{self.name}, enter your move (row, column): ").split())
        return (x, y)
