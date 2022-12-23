import chess.svg
from IPython.display import SVG, display

from algorithms import get_move_pvs
from utils import Evaluator

board = chess.Board()
eval1 = Evaluator(pawn=100, knight=300, bishop=350, rook=500, queen=900, potential_coefficient=10)
eval2 = Evaluator(pawn=100, knight=350, bishop=300, rook=500, queen=900, potential_coefficient=10)
for i in range(15):
    m = None
    if not i % 2:
        m = get_move_pvs(board, 2, eval1)
        print("White: ", m)
    else:
        m = get_move_pvs(board, 2, eval2)
        print("Black: ", m)
    board.push(m)

    pg.display.update()

    display(SVG(chess.svg.board(board, size=400)))
