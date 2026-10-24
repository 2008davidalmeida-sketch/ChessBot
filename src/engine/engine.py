import chess
from game_manager.game_manager import GameManager
from .config import DEPTH


class Engine():
    def __init__(self, game_manager: GameManager):
        self.gm = game_manager
        self.nodes_visited = 0


    def move(self) -> chess.Move:
        """Return the best move for the current position using negamax (depth 3)."""
        return self.search(depth=DEPTH)


    def search(self, depth: int) -> chess.Move:
        """Root search: iterate all legal moves and return the one with the best negamax score."""
        self.nodes_visited = 0

        legal_moves = self.gm.get_legal_moves()

        if not legal_moves:
            return None

        legal_moves = sorted(legal_moves, key=self.order_legal_moves, reverse=True)

        best_move = None
        best_score = float('-inf')

        for move in legal_moves:
            self.gm.make_move(move)
            # depth-1 recursive calls, total depth = depth
            score = -self.negamax(depth - 1)
            self.gm.undo_move()

            if score > best_score:
                best_score = score
                best_move = move

            print(f"Move: {move}, Score: {score}, Best: {best_score}")

        print(f"Root moves: {len(legal_moves)} | Total nodes visited: {self.nodes_visited}")
        print()
        return best_move


    def order_legal_moves(self, move: chess.Move) -> tuple:
        """Score a move for ordering: prioritise high-value captures with low-value attackers."""
        victim = self.gm.get_piece_value(self.gm.get_piece_at(move.to_square))
        attacker = self.gm.get_piece_value(self.gm.get_piece_at(move.from_square))
        return (victim, -attacker)


    def negamax(self, depth: int) -> float:
        """Recursive negamax search. Returns the score for the current side to move."""
        self.nodes_visited += 1

        if depth == 0:
            return self.evaluate()

        legal_moves = self.gm.get_legal_moves()

        # Terminal node: no moves available (checkmate or stalemate)
        if not legal_moves:
            if self.gm.board.is_checkmate():
                return float('-inf')  # Current side is in checkmate — worst outcome
            return 0  # Stalemate — draw

        legal_moves = sorted(legal_moves, key=self.order_legal_moves, reverse=True)
        best = float('-inf')

        for move in legal_moves:
            self.gm.make_move(move)
            score = -self.negamax(depth - 1)
            self.gm.undo_move()

            if score > best:
                best = score

        return best

    
    def evaluate(self) -> int:
        score = 0
        current_turn = self.gm.get_turn()

        for square in chess.SQUARES:
            piece = self.gm.get_piece_at(square)
            if piece is not None:
                value = self.get_score(piece, square)
                if piece.color == current_turn:
                    score += value
                else:
                    score -= value

        return score

    
    def get_score(self, piece: chess.Piece, square: chess.Square) -> int:    
        return self.gm.get_piece_value(piece) + self.gm.get_positional_value(piece, square)

    
            
        
