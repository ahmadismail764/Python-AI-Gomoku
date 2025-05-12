from game_engine import GameEngine
from board import Board

gomoku_board = Board(15)
GG = GameEngine(15)
GG.initiate_game()
GG.play()
