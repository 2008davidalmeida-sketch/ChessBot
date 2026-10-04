import chess
import customtkinter as ctk
from engine.game import GameManager

class ChessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.game = GameManager()
        
        self.title("Chess Board")
        self.geometry("550x650")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.unicode_pieces = {
            chess.PAWN: {"white": "♙", "black": "♟"},
            chess.KNIGHT: {"white": "♘", "black": "♞"},
            chess.BISHOP: {"white": "♗", "black": "♝"},
            chess.ROOK: {"white": "♖", "black": "♜"},
            chess.QUEEN: {"white": "♕", "black": "♛"},
            chess.KING: {"white": "♔", "black": "♚"}
        }
        
        self.selected_square = None
        
        # UI Setup
        self.title_label = ctk.CTkLabel(self, text="Chess Engine", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)
        
        self.board_frame = ctk.CTkFrame(self)
        self.board_frame.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="White to move", font=("Arial", 16))
        self.status_label.pack(pady=10)
        
        self.buttons = {}
        self.create_board_ui()
        self.update_board_ui()
        
    def create_board_ui(self):
        for rank in range(7, -1, -1):
            for file in range(8):
                square = chess.square(file, rank)
                # Traditional chess board colors
                color = "white" if (rank + file) % 2 != 0 else "gray"
                fg_col = "#f0d9b5" if color == "white" else "#b58863"
                
                btn = ctk.CTkButton(
                    self.board_frame, 
                    text="", 
                    width=60, 
                    height=60, 
                    font=("Arial", 36),
                    fg_color=fg_col,
                    text_color="black",
                    hover_color="#e8a87c",
                    corner_radius=0,
                    command=lambda sq=square: self.on_square_click(sq)
                )
                btn.grid(row=7-rank, column=file)
                self.buttons[square] = btn
                
    def update_board_ui(self):
        for square in chess.SQUARES:
            piece = self.game.get_piece_at(square)
            btn = self.buttons[square]
            if piece:
                color_key = "white" if piece.color == chess.WHITE else "black"
                btn.configure(text=self.unicode_pieces[piece.piece_type][color_key])
            else:
                btn.configure(text="")
                
            # Reset background colors
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            default_color = "#f0d9b5" if (rank + file) % 2 != 0 else "#b58863"
            btn.configure(fg_color=default_color)
            
        # Highlight selected piece
        if self.selected_square is not None:
            self.buttons[self.selected_square].configure(fg_color="#809a69")
            
        # Highlight last move
        last_move = self.game.get_last_move()
        if last_move:
            self.buttons[last_move.from_square].configure(fg_color="#cdd26a")
            self.buttons[last_move.to_square].configure(fg_color="#cdd26a")

    def on_square_click(self, square):
        if self.game.is_game_over():
            return
            
        if self.selected_square is None:
            # Selecting a piece
            piece = self.game.get_piece_at(square)
            if piece and piece.color == self.game.get_turn():
                self.selected_square = square
                self.update_board_ui()
        else:
            # Clicking same square unselects
            if self.selected_square == square:
                self.selected_square = None
                self.update_board_ui()
                return

            # Attempting to move
            move = chess.Move(self.selected_square, square)
            
            # Handle pawn promotion simply by promoting to queen for now
            piece = self.game.get_piece_at(self.selected_square)
            if piece and piece.piece_type == chess.PAWN:
                if chess.square_rank(square) in [0, 7]:
                    move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            
            if self.game.make_move(move):
                self.selected_square = None
                self.update_board_ui()
                
                # Update status
                if self.game.get_turn() == chess.WHITE:
                    self.status_label.configure(text="White to move")
                else:
                    self.status_label.configure(text="Black to move")
                    
                self.check_game_over()
            else:
                # If clicked on another of own pieces, select it instead
                piece = self.game.get_piece_at(square)
                if piece and piece.color == self.game.get_turn():
                    self.selected_square = square
                else:
                    self.selected_square = None
                self.update_board_ui()
                
    def check_game_over(self):
        reason, result = self.game.get_game_over_reason()
        if reason:
            self.status_label.configure(text=f"Game Over: {reason} ({result})", text_color="red")

if __name__ == "__main__":
    app = ChessApp()
    app.mainloop()
