import chess
import chess.svg


def get_moves_list(game_board, otherSide=False):
    if otherSide:
        game_board.push(chess.Move.null())
        moves = list(game_board.legal_moves)
        game_board.pop()
        return moves
    else:
        return list(game_board.legal_moves)


def algorithm_stub(function, game_board, depth, alpha, beta):
    maximum = -1_000_000
    best = None
    for move in get_moves_list(game_board):
        board_copy = game_board.copy()
        board_copy.push(move)
        value = function(board_copy, depth, alpha, beta)
        if value > maximum:
            maximum = value
            best = move
    return best


class Evaluator:
    # coefficients
    pawn = 100
    knight = 300
    bishop = 300
    rook = 500
    queen = 900
    potential_coefficient = 10

    def __init__(self, pawn=100, knight=300, bishop=300, rook=500, queen=900, potential_coefficient=10):
        self.pawn = pawn
        self.queen = queen
        self.bishop = bishop
        self.knight = knight
        self.rook = rook
        self.potential_coefficient = potential_coefficient

    def evaluate_position(self, game_board, isWhiteMove):
        def get_material_balance():
            white = game_board.occupied_co[chess.WHITE]
            black = game_board.occupied_co[chess.BLACK]
            return (
                    self.pawn * (chess.popcount(white & game_board.pawns) - chess.popcount(black & game_board.pawns)) +
                    self.knight * (chess.popcount(white & game_board.knights) - chess.popcount(
                black & game_board.knights)) +
                    self.bishop * (chess.popcount(white & game_board.bishops) - chess.popcount(
                black & game_board.bishops)) +
                    self.rook * (chess.popcount(white & game_board.rooks) - chess.popcount(black & game_board.rooks)) +
                    self.queen * (chess.popcount(white & game_board.queens) - chess.popcount(black & game_board.queens))
            )

        def get_potential():
            moves0 = len(list(game_board.legal_moves))
            game_board.push(chess.Move.null())
            moves_weight = self.potential_coefficient * (moves0 - len(list(game_board.legal_moves)))
            game_board.pop()
            if game_board.turn != isWhiteMove:
                return -moves_weight
            return moves_weight

        material = get_material_balance()
        potential = get_potential()
        if not isWhiteMove:
            return - material + potential
        else:
            return material + potential
