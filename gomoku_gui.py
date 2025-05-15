import customtkinter as ctk
from board import Board
from game_engine import GameEngine
from minimax_ai import MinimaxAI
from alphabeta_ai import AlphaBetaAI

# Color scheme
WOOD_COLOR = "#deb887"  # Base wood color
WOOD_DARK = "#b38b4d"   # Darker wood shade for borders
GRID_COLOR = "#6d4c2b"  # Dark brown for grid
STAR_COLOR = "#3e2723"  # Even darker for star points
STONE_SHADOW = "#bfa77a"  # Light shadow for stones
BG_COLOR = "#e6c9a3"    # Light wood background

class GomokuGUI(ctk.CTk):
    def __init__(self, board_size=15):
        super().__init__()
        self.title("Gomoku - Modern GUI")
        self.geometry("900x900")
        self.configure(fg_color=BG_COLOR)
        
        self.board_size = board_size
        self.selected_board_size = ctk.StringVar(value="15")
        self.custom_board_size = ctk.StringVar()
        self.cell_size = 40
        self.margin = 30
        self.board = None
        self.current_mark = 'X'
        self.mode = None
        self.ai_algo = None
        self.ai_player = None
        self.ai1 = None
        self.ai2 = None
        self.winning_coords = []
        self.player1_name = 'Player 1'
        self.player2_name = 'Player 2'
        self.last_move = None
        self.canvas_frame = None
        self.canvas = None
        self.create_welcome_page()
        self.create_widgets()
        self.hide_board_widgets()

    def create_welcome_page(self):
        self.welcome_frame = ctk.CTkFrame(self, fg_color=WOOD_COLOR)
        self.welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(self.welcome_frame, text="Welcome to Gomoku!", 
                            font=("Arial", 28), text_color="#2d1810")
        label.pack(pady=30)

        size_label = ctk.CTkLabel(self.welcome_frame, text="Select Board Size:", 
                                 font=("Arial", 18), text_color="#2d1810")
        size_label.pack(pady=(10, 0))
        
        size_option = ctk.CTkOptionMenu(self.welcome_frame, 
                                      variable=self.selected_board_size,
                                      values=["9", "13", "15", "19"],
                                      fg_color=WOOD_DARK,
                                      button_color=WOOD_DARK,
                                      button_hover_color="#96744c")
        size_option.pack(pady=(0, 5))
        
        custom_label = ctk.CTkLabel(self.welcome_frame, text="Or enter custom size:", 
                                   font=("Arial", 14), text_color="#2d1810")
        custom_label.pack(pady=(5, 0))
        
        custom_entry = ctk.CTkEntry(self.welcome_frame, 
                                   textvariable=self.custom_board_size,
                                   width=80)
        custom_entry.pack(pady=(0, 5))
        
        self.custom_size_error = ctk.CTkLabel(self.welcome_frame, text="",
                                             font=("Arial", 12),
                                             text_color="#c0392b")
        self.custom_size_error.pack(pady=(0, 10))

        # Game mode buttons
        btn_style = {
            "width": 220,
            "height": 50,
            "fg_color": WOOD_DARK,
            "hover_color": "#96744c",
            "text_color": "#ffffff"
        }

        btn1 = ctk.CTkButton(self.welcome_frame, text="Human vs Human",
                            command=lambda: self.start_game('hvh'), **btn_style)
        btn1.pack(pady=10)
        
        btn2 = ctk.CTkButton(self.welcome_frame, text="Human vs AI",
                            command=lambda: self.start_game('hvai'), **btn_style)
        btn2.pack(pady=10)
        
        btn3 = ctk.CTkButton(self.welcome_frame, text="AI vs AI",
                            command=lambda: self.start_game('aivai'), **btn_style)
        btn3.pack(pady=10)

    def create_name_entry_page(self, mode):
        self.name_frame = ctk.CTkFrame(self, fg_color=WOOD_COLOR)
        self.name_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(self.name_frame, text="Enter Player Name(s)", 
                            font=("Arial", 22), text_color="#2d1810")
        label.pack(pady=30)
        
        self.name_entries = []
        if mode == 'hvh':
            label1 = ctk.CTkLabel(self.name_frame, text="Player 1 Name:", 
                                font=("Arial", 16), text_color="#2d1810")
            label1.pack(pady=(10, 0))
            entry1 = ctk.CTkEntry(self.name_frame)
            entry1.pack(pady=(0, 10))
            self.name_entries.append(entry1)
            
            label2 = ctk.CTkLabel(self.name_frame, text="Player 2 Name:", 
                                font=("Arial", 16), text_color="#2d1810")
            label2.pack(pady=(10, 0))
            entry2 = ctk.CTkEntry(self.name_frame)
            entry2.pack(pady=(0, 10))
            self.name_entries.append(entry2)
        elif mode == 'hvai':
            label1 = ctk.CTkLabel(self.name_frame, text="Your Name:", 
                                font=("Arial", 16), text_color="#2d1810")
            label1.pack(pady=(10, 0))
            entry1 = ctk.CTkEntry(self.name_frame)
            entry1.pack(pady=(0, 10))
            self.name_entries.append(entry1)

        button_frame = ctk.CTkFrame(self.name_frame, fg_color=WOOD_COLOR)
        button_frame.pack(pady=20)
        
        btn_style = {
            "width": 120,
            "height": 45,
            "fg_color": WOOD_DARK,
            "hover_color": "#96744c",
            "text_color": "#ffffff"
        }
        
        undo_btn = ctk.CTkButton(button_frame, text="Back",
                                command=lambda: self.undo_to_welcome(),
                                **btn_style)
        undo_btn.pack(side="left", padx=10)
        
        start_btn = ctk.CTkButton(button_frame, text="Next",
                                 command=lambda: self.confirm_names(mode),
                                 **btn_style)
        start_btn.pack(side="left", padx=10)

    def create_algo_select_page(self):
        self.algo_frame = ctk.CTkFrame(self, fg_color=WOOD_COLOR)
        self.algo_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(self.algo_frame, text="Choose AI Algorithm", 
                            font=("Arial", 24), text_color="#2d1810")
        label.pack(pady=30)
        
        button_frame = ctk.CTkFrame(self.algo_frame, fg_color=WOOD_COLOR)
        button_frame.pack(pady=20)
        
        btn_style = {
            "width": 120,
            "height": 45,
            "fg_color": WOOD_DARK,
            "hover_color": "#96744c",
            "text_color": "#ffffff"
        }
        
        undo_btn = ctk.CTkButton(button_frame, text="Back",
                                command=lambda: self.undo_to_name_entry(),
                                **btn_style)
        undo_btn.pack(side="left", padx=10)
        
        btn_minimax = ctk.CTkButton(button_frame, text="Minimax",
                                   command=lambda: self.select_ai_algo('minimax'),
                                   **btn_style)
        btn_minimax.pack(side="left", padx=10)
        
        btn_alphabeta = ctk.CTkButton(button_frame, text="AlphaBeta",
                                     command=lambda: self.select_ai_algo('alphabeta'),
                                     **btn_style)
        btn_alphabeta.pack(side="left", padx=10)

    def undo_to_welcome(self):
        if hasattr(self, 'name_frame') and self.name_frame.winfo_exists():
            self.name_frame.pack_forget()
        if hasattr(self, 'algo_frame') and self.algo_frame.winfo_exists():
            self.algo_frame.pack_forget()
        self.create_welcome_page()

    def undo_to_name_entry(self):
        if hasattr(self, 'algo_frame') and self.algo_frame.winfo_exists():
            self.algo_frame.pack_forget()
        self.create_name_entry_page('hvai')

    def confirm_names(self, mode):
        if mode == 'hvh':
            self.player1_name = self.name_entries[0].get() or 'Player 1'
            self.player2_name = self.name_entries[1].get() or 'Player 2'
        elif mode == 'hvai':
            self.player1_name = self.name_entries[0].get() or 'Player'
            self.player2_name = None
        self.name_frame.pack_forget()
        if mode == 'hvai':
            self.create_algo_select_page()
        else:
            self.reset_board()
            self.show_board_widgets()

    def select_ai_algo(self, algo):
        self.ai_algo = algo
        ai_name = 'Minimax' if algo == 'minimax' else 'Alphabeta'
        if algo == 'minimax':
            self.ai_player = MinimaxAI(ai_name, 'O', 'X')
        else:
            self.ai_player = AlphaBetaAI(ai_name, 'O', 'X')
        self.algo_frame.pack_forget()
        self.reset_board()
        self.show_board_widgets()

    def create_widgets(self):
        self.status_label = ctk.CTkLabel(self, text="Gomoku: X's turn", 
                                        font=("Arial", 22, "bold"), 
                                        text_color="#2d1810")
        
        self.button_frame = ctk.CTkFrame(self, fg_color=WOOD_COLOR)
        
        btn_style = {
            "fg_color": WOOD_DARK,
            "hover_color": "#96744c",
            "text_color": "#ffffff"
        }
        
        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", 
                                         command=self.reset_board, **btn_style)
        self.home_button = ctk.CTkButton(self.button_frame, text="Back to Home", 
                                        command=self.back_to_home, **btn_style)

    def show_board_widgets(self):
        self.status_label.pack(pady=(20, 0))
        self.canvas_frame.pack(expand=True)
        self.canvas.pack(expand=True, padx=20, pady=20)
        self.button_frame.pack(side="bottom", fill="x", pady=(10, 20), padx=20)
        self.reset_button.pack(side="left", expand=True, padx=20, pady=10)
        self.home_button.pack(side="right", expand=True, padx=20, pady=10)
        self.draw_board()

    def hide_board_widgets(self):
        if self.canvas_frame: 
            self.canvas_frame.pack_forget()
        if self.canvas: 
            self.canvas.pack_forget()
        if self.status_label: 
            self.status_label.pack_forget()
        if self.button_frame: 
            self.button_frame.pack_forget()
        if self.reset_button:
            self.reset_button.pack_forget()
        if self.home_button:
            self.home_button.pack_forget()

    def start_game(self, mode):
        self.mode = mode
        # Use custom size if provided and valid, else use dropdown
        custom_val = self.custom_board_size.get()
        try:
            custom_size = int(custom_val)
            if custom_size < 5:
                self.custom_size_error.configure(text="Board size must be at least 5.")
                return
            else:
                self.custom_size_error.configure(text="")
            if 5 <= custom_size <= 30:
                self.board_size = custom_size
            else:
                self.board_size = int(self.selected_board_size.get())
        except ValueError:
            self.board_size = int(self.selected_board_size.get())
            self.custom_size_error.configure(text="")
        self.board = Board(self.board_size)
        self.custom_board_size.set("")
        
        # Calculate canvas and board dimensions
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        max_canvas_size = min(window_width - 100, window_height - 200, 700)  # Cap maximum size
        self.canvas_size = max_canvas_size
        self.cell_size = (max_canvas_size - 80) // (self.board_size - 1)  # Adjust for grid lines
        self.margin = 40  # Fixed margin
        
        # Create canvas with calculated dimensions
        self.canvas_frame = ctk.CTkFrame(self, fg_color=WOOD_COLOR)
        self.canvas = ctk.CTkCanvas(
            self.canvas_frame, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg=WOOD_COLOR, 
            highlightthickness=0
        )

        self.welcome_frame.pack_forget()
        if mode == 'hvai' or mode == 'hvh':
            self.create_name_entry_page(mode)
        elif mode == 'aivai':
            self.ai1 = MinimaxAI('Minimax', 'X', 'O')
            self.ai2 = AlphaBetaAI('Alphabeta', 'O', 'X')
            self.reset_board()
            self.show_board_widgets()
            self.after(800, self.ai_vs_ai_move)

    def draw_board(self):
        self.canvas.delete("all")
        
        # Calculate board dimensions
        board_size = (self.board_size - 1) * self.cell_size
        
        # Draw brown border around the entire board area
        border_margin = self.margin - 5
        self.canvas.create_rectangle(
            border_margin, border_margin,
            border_margin + board_size + 10, border_margin + board_size + 10,
            outline="#8B5C2A", width=6
        )

        # Draw grid
        for i in range(self.board_size):
            # Vertical lines
            x = self.margin + i * self.cell_size
            self.canvas.create_line(
                x, self.margin,
                x, self.margin + board_size,
                fill=GRID_COLOR, width=1
            )
            # Horizontal lines
            y = self.margin + i * self.cell_size
            self.canvas.create_line(
                self.margin, y,
                self.margin + board_size, y,
                fill=GRID_COLOR, width=1
            )

        # Draw star points
        self.draw_star_points()
        
        # Draw stones
        for r in range(self.board_size):
            for c in range(self.board_size):
                mark = self.board.grid[r][c]
                if mark != '.':
                    highlight = (r, c) in self.winning_coords
                    is_last = self.last_move == (r, c)
                    self.draw_stone(r, c, mark, highlight, is_last)

    def draw_star_points(self):
        # Star points for 9x9, 13x13, 15x15, 19x19
        star_points = {
            9:  [(2,2), (2,6), (4,4), (6,2), (6,6)],
            13: [(3,3), (3,9), (6,6), (9,3), (9,9)],
            15: [(3,3), (3,7), (3,11), (7,3), (7,7), (7,11), (11,3), (11,7), (11,11)],
            19: [(3,3), (3,9), (3,15), (9,3), (9,9), (9,15), (15,3), (15,9), (15,15)]
        }
        points = star_points.get(self.board_size, [])
        for r, c in points:
            x = self.margin + c * self.cell_size
            y = self.margin + r * self.cell_size
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=STAR_COLOR, outline=STAR_COLOR)

    def draw_stone(self, row, col, mark, highlight=False, is_last=False):
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        stone_radius = int(self.cell_size * 0.43)  # Slightly larger stones
        shadow_radius = int(self.cell_size * 0.45)
        border_radius = int(self.cell_size * 0.48)
        
        # Draw shadow
        self.canvas.create_oval(
            x - shadow_radius, y - shadow_radius + 3,
            x + shadow_radius, y + shadow_radius + 3,
            fill=STONE_SHADOW, outline=""
        )
        
        # Draw stone
        color = "#222" if mark == 'X' else "#fff"
        border_color = "#111" if mark == 'X' else "#bbb"
        self.canvas.create_oval(
            x - stone_radius, y - stone_radius,
            x + stone_radius, y + stone_radius,
            fill=color, outline=border_color, width=1
        )
        
        # Draw highlight for winning stones
        if highlight:
            self.canvas.create_oval(
                x - border_radius, y - border_radius,
                x + border_radius, y + border_radius,
                outline="#27ae60", width=3
            )
        
        # Draw shine on white stones
        if mark == 'O' and not highlight:
            shine_radius_x = int(stone_radius * 0.6)
            shine_radius_y = int(stone_radius * 0.35)
            self.canvas.create_oval(
                x - shine_radius_x, y - shine_radius_y - 5,
                x, y,
                fill="#f7f7f7", outline=""
            )
        
        # Draw last move indicator
        if is_last and not highlight:
            self.canvas.create_oval(
                x - border_radius, y - border_radius,
                x + border_radius, y + border_radius,
                outline="#e74c3c", width=3
            )

    def on_canvas_click(self, event):
        if self.mode == 'aivai':
            return  # Disable clicks in AI vs AI mode
        col = round((event.x - self.margin) / self.cell_size)
        row = round((event.y - self.margin) / self.cell_size)
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.board.is_valid_move(row, col):
                self.board.apply_move(row, col, self.current_mark)
                self.last_move = (row, col)
                self.draw_board()
                win_coords = self.board.is_winner(self.current_mark)
                if win_coords:
                    self.winning_coords = win_coords
                    self.draw_board()
                    winner_name = self.get_player_name(self.current_mark)
                    self.status_label.configure(text=f"{winner_name} ({self.current_mark}) wins!")
                    self.canvas.unbind("<Button-1>")
                    return
                elif self.board.draw():
                    self.status_label.configure(text="It's a draw!")
                    return
                self.current_mark = 'O' if self.current_mark == 'X' else 'X'
                player_name = self.get_player_name(self.current_mark)
                self.status_label.configure(text=f"{player_name} ({self.current_mark})'s turn")
                if self.mode == 'hvai' and self.current_mark == 'O':
                    self.after(500, self.ai_move)

    def ai_move(self):
        if self.ai_player:
            move = self.ai_player.get_move(self.board)
            if move:
                x, y = move
                self.board.apply_move(x, y, 'O')
                self.last_move = (x, y)
                self.draw_board()
                win_coords = self.board.is_winner('O')
                if win_coords:
                    self.winning_coords = win_coords
                    self.draw_board()
                    self.status_label.configure(text=f"{self.ai_player.name} (O) wins!")
                    self.canvas.unbind("<Button-1>")
                    return
                elif self.board.draw():
                    self.status_label.configure(text="It's a draw!")
                    return
                self.current_mark = 'X'
                player_name = self.get_player_name(self.current_mark)
                self.status_label.configure(text=f"{player_name} ({self.current_mark})'s turn")

    def ai_vs_ai_move(self):
        if not (self.ai1 and self.ai2):
            return
        win_coords_X = self.board.is_winner('X')
        win_coords_O = self.board.is_winner('O')
        if win_coords_X:
            self.winning_coords = win_coords_X
            self.draw_board()
            self.status_label.configure(text=f"{self.ai1.name} (X) wins!")
            return
        if win_coords_O:
            self.winning_coords = win_coords_O
            self.draw_board()
            self.status_label.configure(text=f"{self.ai2.name} (O) wins!")
            return
        if self.board.draw():
            self.status_label.configure(text="It's a draw!")
            return
        if self.current_mark == 'X':
            move = self.ai1.get_move(self.board)
            if move:
                x, y = move
                self.board.apply_move(x, y, 'X')
                self.last_move = (x, y)
                self.draw_board()
                win_coords_X = self.board.is_winner('X')
                if win_coords_X:
                    self.winning_coords = win_coords_X
                    self.draw_board()
                    self.status_label.configure(text=f"{self.ai1.name} (X) wins!")
                    return
                elif self.board.draw():
                    self.status_label.configure(text="It's a draw!")
                    return
                self.current_mark = 'O'
        else:
            move = self.ai2.get_move(self.board)
            if move:
                x, y = move
                self.board.apply_move(x, y, 'O')
                self.last_move = (x, y)
                self.draw_board()
                win_coords_O = self.board.is_winner('O')
                if win_coords_O:
                    self.winning_coords = win_coords_O
                    self.draw_board()
                    self.status_label.configure(text=f"{self.ai2.name} (O) wins!")
                    return
                elif self.board.draw():
                    self.status_label.configure(text="It's a draw!")
                    return
                self.current_mark = 'X'
        player_name = self.get_player_name(self.current_mark)
        self.status_label.configure(text=f"{player_name} ({self.current_mark})'s turn")
        self.after(800, self.ai_vs_ai_move)

    def get_player_name(self, mark):
        if self.mode == 'aivai':
            if mark == 'X':
                return self.ai1.name
            elif mark == 'O':
                return self.ai2.name
        elif self.mode == 'hvai' and mark == 'O' and self.ai_player:
            return self.ai_player.name
        elif self.mode == 'hvai' and mark == 'X':
            return self.player1_name
        elif self.mode == 'hvh':
            if mark == 'X':
                return self.player1_name
            elif mark == 'O':
                return self.player2_name
        return 'Player'

    def reset_board(self):
        if not self.board: return # Board not yet created
        self.board.reset()
        self.current_mark = 'X'
        self.winning_coords = []
        self.last_move = None
        self.draw_board()
        player_name = self.get_player_name(self.current_mark)
        self.status_label.configure(text=f"{player_name} ({self.current_mark})'s turn")
        if self.canvas: self.canvas.bind("<Button-1>", self.on_canvas_click)

    def back_to_home(self):
        self.hide_board_widgets()
        if hasattr(self, 'algo_frame') and self.algo_frame.winfo_exists():
            self.algo_frame.pack_forget()
        self.create_welcome_page()
        self.board.reset()
        self.current_mark = 'X'
        self.mode = None
        self.ai_algo = None
        self.ai_player = None
        self.ai1 = None
        self.ai2 = None

if __name__ == "__main__":
    app = GomokuGUI()
    app.mainloop() 