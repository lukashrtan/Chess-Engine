import moves
from board import Board
from constants import BISHOP, KING, KNIGHT, PAWN, QUEEN, ROCK, UNCOLOR, WHITE
from moves import (Move, all_moves, available_moves)


def computer_move(board: Board) -> Move:
    moves_evaluaited: list[tuple[int, Move]] = []
    for move in available_moves(board):
        moves_evaluaited.append((recursive_evaluation(board.clone().move(move), 3, -99999999999, 99999999999, True), move))
    if board.color == WHITE:
        return max(moves_evaluaited)[1]
    return min(moves_evaluaited)[1]



def recursive_evaluation(board: Board, depth: int, alpha: int, beta: int, max_player: bool) -> int:
    if depth == 0 or moves.check_mate(board, board.black_king_pos) == True:
        return position_evaluation(board)
    if max_player:
        score = -99999999999
        for move in available_moves(board):
            evaluation = recursive_evaluation(board.clone().move(move), depth - 1, alpha, beta, False)
            score = max(score, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return score
    else:
        score = 99999999999
        for move in available_moves(board):
            evaluation = recursive_evaluation(board.clone().move(move), depth - 1, alpha, beta, True)
            score = min(score, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return score


def position_evaluation(board: Board) -> int:
    evaluation = 0
    for i in board.board:
        piece = i % UNCOLOR
        color = i - piece

        if i == 0:
            continue

        if piece == ROCK:
            square = 5
        elif piece == PAWN:
            square = 1
        elif piece == KING:
            square = 0
        elif piece == QUEEN:
            square = 9
        elif piece in (KNIGHT, BISHOP):
            square = 3
        else:
            raise AssertionError


        square = square * 1 if color == WHITE else square * -1

        evaluation += square

    #if moves.check_mate(board, board.white_king_pos):
        #square = 100000

    return evaluation

