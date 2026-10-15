import chess


class GameManager:
    def __init__(self):
        self.board = chess.Board()


    def get_piece_at(self, square: chess.Square) -> chess.Piece:
        return self.board.piece_at(square)

    def get_piece_value(self, piece: chess.Piece) -> int:
        if piece is None:
            return 0
        
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0,
        }
        return piece_values.get(piece.piece_type, 0)


    def is_game_over(self) -> bool:
        return self.board.is_game_over()


    def get_turn(self) -> chess.Color:
        return self.board.turn


    def get_legal_moves(self) -> list[chess.Move]:
        return list(self.board.legal_moves)

    
    def is_legal_move(self, move: chess.Move) -> bool:
        return move in self.board.legal_moves


    def make_move(self, move: chess.Move) -> bool:
        if self.is_legal_move(move):
            self.board.push(move)
            return True
        return False


    def undo_move(self) -> None:
        if self.board.move_stack:
            self.board.pop()


    def get_last_move(self) -> chess.Move:
        if len(self.board.move_stack) > 0:
            return self.board.peek()
        return None


    def get_game_over_reason(self) -> tuple[str | None, str | None]:
        if not self.is_game_over():
            return None, None

        # Check for checkmate, stalemate, and draw
        if self.board.is_checkmate():
            reason = "Checkmate!"
        elif self.board.is_stalemate():
            reason = "Stalemate!"
        else:
            reason = "Draw!"
        return reason, self.board.result()
