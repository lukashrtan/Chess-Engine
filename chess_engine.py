from moves import check_mate
from board import Board
from constants import BISHOP, KING, KNIGHT, PAWN, QUEEN, ROCK, UNCOLOR, WHITE, SWITCH_COLOR, EMPTY, BLACK
from moves import (Move, all_moves, available_moves)
from tile import A8, H8, A1, H1

def computer_move(board: Board) -> Move:
    moves_evaluated: list[tuple[int, Move]] = []
    for move in available_moves(board):
        moves_evaluated.append((recursive_evaluation(board.clone().move(move),
                  3, -99999999999, 99999999999, True), move))
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
    if board.color == BLACK:
        king = board.black_king_pos
    else:
        king = board.white_king_pos
    if depth == 0 or check_mate(board, king) == True:
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

def engine_move_board(board: "Board", move: Move, color:int) -> tuple[int, tuple[int, Move]|None, int, bool]:
    # rošáda

    moving_piece = board[move.fr] % UNCOLOR
    moving_color = color
    if moving_piece == KING and move.fr - move.to == 2:
        piece = board[move.to]
        board[move.to] = board[move.fr]
        board[move.fr] = EMPTY
        castling = (board[move.to + 1], Move(move.fr + 1, move.to - 4))
        board[move.to + 1] = board[move.fr - 4]
        board[move.fr - 4] = EMPTY

    # rošáda
    elif moving_piece == KING and move.to - move.fr == 2:
        piece = board[move.to]
        board[move.to] = board[move.fr]
        board[move.fr] = EMPTY
        castling = (board[move.to - 1], Move(move.fr - 1, move.to + 3))
        board[move.to - 1] = board[move.fr + 3]
        board[move.fr + 3] = EMPTY

    # prostě tah
    else:
        castling = None
        piece = board[move.to]
        board[move.to] = board[move.fr]
        board[move.fr] = EMPTY

    # promo
    if move.promo is not None:
        board[move.to] = move.promo

    # castling rights
    if moving_piece == KING:
        if moving_color == WHITE:
            board.white_ooo = False
            board.white_oo = False
        else:
            board.black_ooo = False
            board.black_oo = False
    if moving_piece == ROCK:
        if move.fr == A8:
            board.black_ooo = False
        if move.fr == H8:
            board.black_oo = False
        if move.fr == A1:
            board.white_ooo = False
        if move.fr == H1:
            board.white_oo = False

    color = SWITCH_COLOR[color]
    promo = not Move.promo is None
    return piece, castling, color, promo

def engine_unmove_board(board: "Board", move: Move, piece: int, castling: tuple[int, Move], color: int, promo: bool) -> int:
    if promo:
        board[move.to], board[move.fr] = piece, promo
    else:
        board[move.to], board[move.fr] = piece, board[move.to]
    if castling:
        board[castling[1].to], board[castling[1].fr] = castling[0], board[castling[1].to]
    color = SWITCH_COLOR[color]
    return color

