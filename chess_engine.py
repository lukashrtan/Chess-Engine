import moves
#from game import king_pos
from moves import check_mate, capture_moves
from board import Board
from constants import BISHOP, KING, KNIGHT, PAWN, QUEEN, ROCK, UNCOLOR, WHITE, SWITCH_COLOR, EMPTY, BLACK, PIECE_VALUE
from moves import (Move, available_moves)
from tile import A8, H8, A1, H1

counter = 0
counter_capture = 0


def computer_move(board: Board) -> Move:
    moves_evaluated: list[tuple[int, Move]] = [
        (recursive_evaluation(board.clone().move(move),
                              3, -99999999999, 99999999999, True), move)
        for move in available_moves(board)]
    if board.color == WHITE:
        return max(moves_evaluated)[1]
    return min(moves_evaluated)[1]


# def computer_move(board: Board) -> Move:
#     color = board.color
#     moves_evaluated: list[tuple[int, Move]] = []
#     for move in all_moves(board):
#         changes = engine_move_board(board, move, color)
#         moves_evaluated.append((recursive_evaluation(board, color,
#                       3, -99999999999, 99999999999, True), move))
#         color = engine_unmove_board(board, move, changes[0], changes[1], changes[2], changes[3])
#     if board.color == color:
#         return max(moves_evaluated)[1]
#     return min(moves_evaluated)[1]


def recursive_evaluation(board: Board, depth: int, alpha: int, beta: int, max_player: bool) -> int:
    if depth == 0:
        return capture_evaluation(board, 2, alpha, beta, max_player)

    if max_player:
        score = -99999999999
        for move in sorted(available_moves(board), key=lambda m: move_evaluation(board, m)):
            evaluation = recursive_evaluation(board.clone().move(move), depth - 1, alpha, beta, False)
            score = max(score, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return score
    else:
        score = 99999999999
        for move in sorted(available_moves(board), key=lambda m: move_evaluation(board, m)):
            evaluation = recursive_evaluation(board.clone().move(move), depth - 1, alpha, beta, True)
            score = min(score, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return score

def capture_evaluation(board: Board, depth: int, alpha: int, beta: int, max_player: bool):
    global counter_capture
    if depth == 0:
        counter_capture += 1
        return position_evaluation(board)
    if max_player:
        score = -99999999999
        #print(board.white_king_pos)
        for move in sorted(capture_moves(board), key=lambda m: move_evaluation(board, m)):
            evaluation = capture_evaluation(board.clone().move(move), depth - 1, alpha, beta, False)
            score = max(score, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        if score == -99999999999:
            return position_evaluation(board)
        return score

    else:
        score = 99999999999
        for move in sorted(capture_moves(board), key=lambda m: move_evaluation(board, m)):
            evaluation = capture_evaluation(board.clone().move(move), depth - 1, alpha, beta, True)
            score = min(score, evaluation)
            alpha = min(alpha, evaluation)
            if beta <= alpha:
                break
        if score == 99999999999:
            return position_evaluation(board)
        return score

# def recursive_evaluation(board: Board, color, depth: int, alpha: int, beta: int, max_player: bool) -> int:
#     if board.color == BLACK:
#         king = board.black_king_pos
#     else:
#         king = board.white_king_pos
#     if depth == 0 or check_mate(board, king) == True:
#         return position_evaluation(board)
#     if max_player:
#         score = -99999999999
#         for move in available_moves(board):
#             changes = engine_move_board(board, move, color)
#             evaluation = recursive_evaluation(board, color, depth - 1, alpha, beta, False)
#             color = engine_unmove_board(board, move, changes[0], changes[1], changes[2], changes[3])
#             score = max(score, evaluation)
#             alpha = max(alpha, evaluation)
#             if beta <= alpha:
#                 break
#         return score
#     else:
#         score = 99999999999
#         for move in available_moves(board):
#             changes = engine_move_board(board, move, color)
#             evaluation = recursive_evaluation(board, color, depth - 1, alpha, beta, True)
#             color = engine_unmove_board(board, move, changes[0], changes[1], changes[2], changes[3])
#             score = min(score, evaluation)
#             beta = min(beta, evaluation)
#             if beta <= alpha:
#                 break
#         return score

def position_evaluation(board: Board) -> int:
    global counter
    evaluation = 0
    counter += 1
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

    try:
        if moves.check_mate(board, board.white_king_pos):
            evaluation = 100000
        if moves.check_mate(board, board.black_king_pos):
            evaluation = -100000
    except:
        ...

    return evaluation

def move_evaluation(board: Board, move: Move) -> int:
    taker_value = PIECE_VALUE[board[move.fr] % UNCOLOR]
    victim_value = PIECE_VALUE[board[move.to] % UNCOLOR]

    return victim_value - taker_value
