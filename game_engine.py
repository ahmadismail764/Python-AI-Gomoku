from player import Player
from board import Board
from alphabeta_ai import AlphaBetaAI
from minimax_ai import MinimaxAI


class GameEngine:
    def __init__(self, board_size=15):
        self.board = Board(board_size)
        self.player1 = None
        self.player2 = None

    def get_valid_input(self, prompt, validation_func, error_message):
        while True:
            user_input = input(prompt)
            try:
                validated_input = validation_func(user_input)
                return validated_input
            except Exception as e:
                if str(e):
                    print(f"Error: {str(e)}")
                else:
                    print(f"Error: {error_message}")
                    
    def validate_game_mode(self, choice):
        choice = choice.strip()
        if not choice.isdigit() or int(choice) not in [1, 2, 3]:
            raise ValueError("Please choose 1, 2, or 3")
        return int(choice)
            
    def validate_name(self, name):
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        return name
        
    def validate_second_name(self, name, first_name):
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        if name.lower() == first_name.lower():
            raise ValueError(f"This name '{name}' is already taken by the other player")
        return name

    def validate_mark(self, mark):
        mark = mark.strip()
        if not mark or len(mark) != 1:
            raise ValueError("Please enter exactly one character")
        return mark[0]
        
    def validate_second_mark(self, mark, first_mark):
        mark = mark.strip()
        if not mark or len(mark) != 1:
            raise ValueError("Please enter exactly one character")
        if mark[0] == first_mark:
            raise ValueError(f"This mark '{mark[0]}' is already taken by the other player")
        return mark[0]
        
    def validate_algo_choice(self, choice):
        choice = choice.strip()
        if choice not in ["1", "2"]:
            raise ValueError("Please choose 1 or 2")
        return choice
        
    def validate_move(self, move_str, board):
        try:
            parts = move_str.split(',')
            if len(parts) != 2:
                raise ValueError()
                
            x, y = int(parts[0].strip()), int(parts[1].strip())
            
            if not board.is_valid_move(x, y):
                raise ValueError(f"Position ({x},{y}) is not available")
                
            return (x, y)
        except ValueError as e:
            if str(e):
                raise ValueError(str(e))
            raise ValueError("Please enter coordinates in the format: x,y")

    def initiate_game(self):
        print("Starting the game...")
        print("Welcome to the game!")

        print("\nChoose game mode:")
        print("1. Human vs Human")
        print("2. Human vs AI")
        print("3. AI vs AI (Watch and learn!)")
        
        choice = self.get_valid_input(
            "Enter your choice: ",
            self.validate_game_mode,
            "Please choose the correct game mode (1, 2, or 3)"
        )
        
        # Two human players case
        if choice == 1:
            player1name = self.get_valid_input(
                "Enter name for Player 1: ",
                self.validate_name,
                "Please enter a valid name for Player 1"
            )
            
            player1mark = self.get_valid_input(
                "Enter mark for Player 1 (Any character you like, one character): ",
                self.validate_mark,
                "Please enter exactly one character"
            )
            
            self.player1 = Player(player1name, player1mark)
            
            player2name = self.get_valid_input(
                "Enter name for Player 2: ",
                lambda name: self.validate_second_name(name, player1name),
                "Please enter a unique name for Player 2"
            )
            
            player2mark = self.get_valid_input(
                "Enter mark for Player 2 (Any character you like, one character): ",
                lambda mark: self.validate_second_mark(mark, player1mark),
                "Please enter a unique mark for Player 2"
            )
            
            self.player2 = Player(player2name, player2mark)
            
        # Human vs AI case
        elif choice == 2:
            player1name = self.get_valid_input(
                "Enter name for Player 1: ",
                self.validate_name,
                "Please enter a valid name for Player 1"
            )
            
            player1mark = self.get_valid_input(
                "Enter your mark (Any character you like, one character): ",
                self.validate_mark,
                "Please enter exactly one character"
            )
            
            self.player1 = Player(player1name, player1mark)
            
            player2name = self.get_valid_input(
                "Enter name for your AI opponent: ",
                lambda name: self.validate_second_name(name, player1name),
                "Please enter a unique name for your AI opponent"
            )
            
            player2mark = self.get_valid_input(
                "Enter mark for your AI opponent (Any character you like, one character): ",
                lambda mark: self.validate_second_mark(mark, player1mark),
                "Please enter a unique mark for the AI"
            )
            
            algo = self.get_valid_input(
                "Choose AI algorithm (1 for Minimax, 2 for Alpha-Beta): ",
                self.validate_algo_choice,
                "Please choose 1 or 2"
            )
            
            if algo == "1":
                self.player2 = MinimaxAI(player2name, player2mark, player1mark)
            else:
                self.player2 = AlphaBetaAI(player2name, player2mark, player1mark)
                
        # AI vs AI case
        else:
            player1name = self.get_valid_input(
                "Enter name for Minimax AI Player: ",
                self.validate_name,
                "Please enter a valid name for Minimax AI Player"
            )
            
            player1mark = self.get_valid_input(
                "Enter mark for Minimax AI Player (Any character you like, one character): ",
                self.validate_mark,
                "Please enter exactly one character"
            )
            
            player2name = self.get_valid_input(
                "Enter name for AlphaBeta AI Player: ",
                lambda name: self.validate_second_name(name, player1name),
                "Please enter a unique name for AlphaBeta AI"
            )
            
            player2mark = self.get_valid_input(
                "Enter mark for AlphaBeta AI Player (Any character you like, one character): ",
                lambda mark: self.validate_second_mark(mark, player1mark),
                "Please enter a unique mark for AlphaBeta AI"
            )
            
            self.player1 = MinimaxAI(player1name, player1mark, player2mark)
            self.player2 = AlphaBetaAI(player2name, player2mark, player1mark)

    def play(self):
        self.board.reset()
        curr_player = self.player1
        while True:
            self.board.display()
            
            # Get move with validation for human players
            if isinstance(curr_player, Player) and not isinstance(curr_player, MinimaxAI) and not isinstance(curr_player, AlphaBetaAI):
                print(f"{curr_player.name}'s turn ({curr_player.mark})")
                while True:
                    try:
                        move_str = input("Enter your move (x,y): ")
                        move = self.validate_move(move_str, self.board)
                        break
                    except ValueError as e:
                        print(f"Error: {str(e)}")
                        print("Please try again.")
            else:
                # AI player's move
                move = curr_player.get_move(self.board)
                
            x, y = move
            self.board.apply_move(x, y, curr_player.mark)
            print(f"{curr_player.name} placed {curr_player.mark} at ({x}, {y})")
            
            if self.board.is_winner(curr_player.mark):
                self.board.display()
                print(f"{curr_player.name} wins!")
                break
                
            if self.board.draw():
                self.board.display()
                print("It's a draw!")
                break
                
            curr_player = self.player2 if curr_player == self.player1 else self.player1

    def run(self):
        self.initiate_game()
        self.play()
