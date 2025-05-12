from player import Player
from board import Board
from alphabeta_ai import AlphaBetaAI
from minimax_ai import MinimaxAI


class GameEngine:
    def __init__(self, board_size=15):
        self.board = Board(board_size)
        self.player1 = None
        self.player2 = None

    def initiate_game(self):
        print("Starting the game...")
        print("Welcome to the game!")

        print("\nChoose game mode:")
        print("1. Human vs Human")
        print("2. Human vs AI")
        print("3. AI vs AI (Watch and learn!)")
        choice = int(input("Enter your choice: "))
        # Two human players case
        if choice == 1:
            player1name = input("Enter name for Player 1: ")
            player1mark = input(
                "Enter mark for Player 1 (Any character you like, one character): "
            )
            self.player1 = Player(player1name, player1mark[0])
            player2name = input("Enter name for Player 2: ")
            player2mark = input(
                "Enter mark for Player 2 (Any character you like, one character): "
            )
            self.player2 = Player(player2name, player2mark[0])
        # Human vs AI case
        elif choice == 2:
            player1name = input("Enter name for Player 1: ")
            player1mark = input(
                "Enter your mark (Any character you like, one character): "
            )
            self.player1 = Player(player1name, player1mark[0])
            player2name = input("Enter name for your AI opponent:")
            player2mark = input(
                "Enter mark for your AI opponent (Any character you like, one character):"
            )
            algo = input("Choose AI algorithm (1 for Minimax, 2 for Alpha-Beta): ")
            if algo == "1":
                self.player2 = MinimaxAI(player2name, player2mark[0])
            else:
                self.player2 = AlphaBetaAI(player2name, player2mark[0])
        # AI vs AI case
        else:
            player1name = input("Enter name for Minimax AI Player: ")
            player1mark = input(
                "Enter mark for Minimax AI Player (Any character you like, one character): "
            )
            self.player1 = MinimaxAI(player1name, player1mark[0])
            player2name = input("Enter name for AlphaBeta AI Player:")
            player2mark = input(
                "Enter mark for AlphaBeta AI Player (Any character you like, one character):"
            )
            self.player2 = AlphaBetaAI(player2name, player2mark[0])

    def play(self):
        self.board.reset()
        curr_player = self.player1
        while True:
            self.board.display()
            move = curr_player.get_move()
            x, y = move
            if self.board.is_valid_move(x, y):
                self.board.apply_move(x, y, curr_player.mark)
                print(f"{curr_player.name} placed {curr_player.mark} at ({x}, {y})")
            if self.board.is_winner(curr_player.mark):
                print(f"{curr_player.name} wins!")
                break
            if self.board.draw():
                print("It's a draw!")
                break
            curr_player = self.player2 if curr_player == self.player1 else self.player1
