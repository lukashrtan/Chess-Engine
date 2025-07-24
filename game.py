import pygame

from board import Board
from chess_engine import computer_move
from constants import BLACK
from drawer import Drawer
from moves import Move, available_moves


def pick_move(board: Board) -> Move:
    while True:
        while True:
            from_tile = pick_square()
            if from_tile != -1:
                break

        while True:
            to_tile = pick_square()
            if to_tile != -1:
                break

        matching_moves = [
            move for move in available_moves(board)
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
    if board.color == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
    board.move(pick_move(board))
    drawer.draw(board)
    if board.color == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
    computer_move(board)
