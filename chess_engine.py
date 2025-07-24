from board import Board
from moves import (Move, all_moves)
from constants import (UNCOLOR, WHITE, ROCK, PAWN, KING, QUEEN, KNIGHT, BISHOP)

def computer_move(board: Board) -> Move:
    moves_evaluaited: list[tuple[int, Move]] = []
    for move in all_moves(board):
        moves_evaluaited.append((recursive_evaluation(board.clone().move(move), 1), move))
    if board.color == WHITE:
        return max(moves_evaluaited)[1]
    else:
        return min(moves_evaluaited)[1]



def recursive_evaluation(board: Board, depth: int) -> int:
    if depth == 0:
        return position_evaluation(board)
    else:
        scores = []
        for move in all_moves(board):
            scores.append(recursive_evaluation(board.clone().move(move), depth - 1))
        if board.color == WHITE:
            return max(scores)
        else:
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
        elif piece == KNIGHT:
            square = 3
        elif piece == BISHOP:
            square = 3
        else:
            raise AssertionError()


        if color == WHITE:
            square = square * 1
        else:
            square = square  * -1

        evaluation += square

    return evaluation

