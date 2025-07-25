from moves import check_mate, check_detection, is_square_under_attack
from board import Board
import pygame

from board import Board
from chess_engine import computer_move, engine_move_board
from constants import BLACK, UNAVAILABLE_MOVE
from drawer import Drawer
from moves import Move, available_moves
import time


def pick_move(board: Board) -> Move:
    from_tile = -1
    moves = list(available_moves(board))
    if len(moves) == 0:
        return Move(UNAVAILABLE_MOVE, UNAVAILABLE_MOVE)
    while True:
        while True:
            if 64 > from_tile > -1 and board[from_tile] // board.color == 1:
                break
            from_tile = pick_square()

        to_tile = pick_square()
        if 64 < to_tile or to_tile < -1 or board[to_tile] // board.color == 1:
            from_tile = to_tile
            continue

        matching_moves = [
            move for move in moves
            if move.fr == from_tile and move.to == to_tile
        ]

        if len(matching_moves) == 0:
            continue
        if len(matching_moves) == 1:
            return matching_moves[0]
        while True:
            promo_piece = pick_promo()
            for move in matching_moves:
                if move.promo == promo_piece:
                    return move


def pick_promo() -> int:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                return position[0] // 100 + position[1] // 100 * 8
                # TODO: some gui for promo picking


def pick_square() -> int:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                return position[0] // 100 + position[1] // 100 * 8


drawer = Drawer()

board = Board.create_board()

while True:
    drawer.draw(board)
    king = board.black_king_pos
    if board.color == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
        king = board.white_king_pos
    move = pick_move(board)
    if move.to == UNAVAILABLE_MOVE:
        if is_square_under_attack(board, king):
            print(f"{board.color} lost")
        else:
            print("draw")
    board.move(move)

    drawer.draw(board)
    #check_mate(board, board.black_king_pos)
    if board.color == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
    start = time.time()
    board.move(computer_move(board))
    print(time.time()-start)

