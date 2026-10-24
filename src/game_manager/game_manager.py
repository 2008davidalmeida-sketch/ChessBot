import chess


class GameManager:
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0,
    }

    PAWN_TABLE = [
        0,   0,   0,   0,   0,   0,   0,   0,
        5,  10,  10, -20, -20,  10,  10,   5,
        5,  -5, -10,   0,   0, -10,  -5,   5,
        0,   0,   0,  20,  20,   0,   0,   0,
        5,   5,  10,  25,  25,  10,   5,   5,
        10,  10,  20,  30,  30,  20,  10,  10,
        50,  50,  50,  50,  50,  50,  50,  50,
        0,   0,   0,   0,   0,   0,   0,   0,
    ]

    KNIGHT_TABLE = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ]

    BISHOP_TABLE = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   0,  10,  10,  10,  10,   0, -10,
        -10,   5,   5,  10,  10,   5,   5, -10,
        -10,   0,   5,  10,  10,   5,   0, -10,
       -10,   0,   0,   0,   0,   0,   0, -10,
       -20, -10, -10, -10, -10, -10, -10, -20,
    ]

    ROOK_TABLE = [
        0,   0,   0,   5,   5,   0,   0,   0,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        5,  10,  10,  10,  10,  10,  10,   5,
        0,   0,   0,   0,   0,   0,   0,   0,
    ]

    QUEEN_TABLE = [
        -20, -10, -10,  -5,  -5, -10, -10, -20,
        -10,   0,   5,   0,   0,   0,   0, -10,
        -10,   5,   5,   5,   5,   5,   0, -10,
        0,     0,   5,   5,   5,   5,   0,  -5,
        -5,    0,   5,   5,   5,   5,   0,  -5,
        -10,   0,   5,   5,   5,   5,   0, -10,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -20, -10, -10,  -5,  -5, -10, -10, -20,
    ]

    KING_MIDDLEGAME_TABLE = [
        20,  30,  10,   0,   0,  10,  30,  20,
        20,  20,   0,   0,   0,   0,  20,  20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
    ]

    KING_ENDGAME_TABLE = [
       -50, -30, -30, -30, -30, -30, -30, -50,
       -30, -30,   0,   0,   0,   0, -30, -30,
       -30, -10,  20,  30,  30,  20, -10, -30,
       -30, -10,  30,  40,  40,  30, -10, -30,
       -30, -10,  30,  40,  40,  30, -10, -30,
       -30, -10,  20,  30,  30,  20, -10, -30,
       -30, -20, -10,   0,   0, -10, -20, -30,
       -50, -40, -30, -20, -20, -30, -40, -50,
    ]

    PIECE_POSITIONAL_VALUE = {
        chess.PAWN: PAWN_TABLE,
        chess.KNIGHT: KNIGHT_TABLE,
        chess.BISHOP: BISHOP_TABLE,
        chess.ROOK: ROOK_TABLE,
        chess.QUEEN: QUEEN_TABLE,
        chess.KING: KING_MIDDLEGAME_TABLE,
    }


    def __init__(self):
        self.board = chess.Board()


    def get_piece_at(self, square: chess.Square) -> chess.Piece:
        return self.board.piece_at(square)


    def get_piece_value(self, piece: chess.Piece) -> int:
        if piece is None:
            return 0
        return self.piece_values.get(piece.piece_type, 0)


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


    def get_positional_value(self, piece: chess.Piece, square: chess.Square) -> int:
        if piece is None:
            return 0
        
        sq = square if piece.color == chess.WHITE else chess.square_mirror(square)
        return self.PIECE_POSITIONAL_VALUE[piece.piece_type][sq]

    def in_endgame(self) -> bool:
        if (self.board.pieces_count(chess.QUEEN) > 0 and 
            self.board.pieces_count(chess.ROOK) > 0):
            return False
        return True