from board import Board
from constants import BISHOP, KING, KNIGHT, PAWN, QUEEN, ROCK, UNCOLOR, WHITE
from moves import Move, all_moves


def computer_move(board: Board) -> Move:
    moves_evaluaited: list[tuple[int, Move]] = []
    for move in all_moves(board):
        moves_evaluaited.append((recursive_evaluation(board.clone().move(move), 1), move))
    if board.color == WHITE:
        return max(moves_evaluaited)[1]
    return min(moves_evaluaited)[1]



def recursive_evaluation(board: Board, depth: int) -> int:
    if depth == 0:
        return position_evaluation(board)
    scores = []
    for move in all_moves(board):
        scores.append(recursive_evaluation(board.clone().move(move), depth - 1))
    if board.color == WHITE:
        return max(scores)
    return min(scores)


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

    return evaluation

