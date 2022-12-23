from utils import get_moves_list, algorithm_stub


def get_move_negamax(game_board, game_depth, evaluator):
    def negamax(board, depth):
        if depth == 0:
            return evaluator.evaluate_position(board, board.turn)
        max_ = -1_000_000
        for move in get_moves_list(board):
            board_ = board.copy()
            board_.push(move)
            value_ = -negamax(board_, depth - 1)
            if value_ > max_:
                max_ = value_
        return max_

    return algorithm_stub(negamax, game_board, game_depth)


def get_move_negascout(game_board, game_depth, evaluator):
    def negascout(board, depth, alpha=-1_000_000, beta=1_000_000):
        if depth == 0:
            return evaluator.evaluate_position(board, board.turn)
        low = -1_000_000
        high = beta
        for move in get_moves_list(board):
            board_ = board.copy()
            board_.push(move)
            value_ = -negascout(board_, depth - 1, -high, -max(alpha, low))
            if value_ > low:
                if high == beta or depth < 3 or value_ >= beta:
                    low = value_
                else:
                    low = -negascout(board_, depth - 1, -beta, -value_)
            if low >= beta:
                return low
            high = max(alpha, low) + 1
        return low

    return algorithm_stub(negascout, game_board, game_depth)


def get_move_pvs(game_board, game_depth, evaluator):
    def pvs(board, depth, alpha=-1_000_000, beta=1_000_000):
        if depth == 0:
            return evaluator.evaluate_position(board, board.turn)
        low = -1_000_000
        high = beta
        for move in get_moves_list(board):
            board_ = board.copy()
            board_.push(move)
            value_ = -pvs(board_, depth - 1, -high, -max(alpha, low))
            if value_ > low:
                low = -pvs(board_, depth - 1, -beta, -alpha)
            if low >= beta:
                return low
            high = max(alpha, low) + 1
        return low

    return algorithm_stub(pvs, game_board, game_depth)
