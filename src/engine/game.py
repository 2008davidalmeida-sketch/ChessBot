import chess

class GameManager:
    def __init__(self):
        self.board = chess.Board()

    def get_piece_at(self, square):
        return self.board.piece_at(square)

    def is_game_over(self):
        return self.board.is_game_over()

    def get_turn(self):
        return self.board.turn

    def is_legal_move(self, move):
        return move in self.board.legal_moves

    def make_move(self, move):
        """Attempts to make a move. Returns True if successful, False otherwise."""
        if self.is_legal_move(move):
            self.board.push(move)
            return True
        return False

    def get_last_move(self):
        if len(self.board.move_stack) > 0:
            return self.board.peek()
        return None

    def get_game_over_reason(self):
        if not self.is_game_over():
            return None, None
            
        result = self.board.result()
        if self.board.is_checkmate():
            reason = "Checkmate!"
        elif self.board.is_stalemate():
            reason = "Stalemate!"
        else:
            reason = "Draw!"
        return reason, result
