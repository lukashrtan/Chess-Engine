import pygame

from board import Board
from chess_engine import computer_move
from constants import BLACK
from drawer import Drawer
from moves import Move, available_moves


def pick_move(board: Board) -> Move:
    while True:
        while True:
            from_tile = pick_square("Jakou chces figurku?")
            if from_tile != -1:
                break

        while True:
            to_tile = pick_square("Kam s ni?")
            if to_tile != -1:
                break

        matching_moves = [move for move in available_moves(board) if move.fr == from_tile and move.to == to_tile]

        if len(matching_moves) == 0:
            continue
        if len(matching_moves) == 1:
            return matching_moves[0]
        while True:
            promo_piece = pick_promo("Za co chces menit?")
            for move in matching_moves:
                if move.promo == promo_piece:
                    return move


def pick_promo(input_message: str) -> int:
    if draw_mode == "Lukas":
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    return position[0] // 100 + position[1] // 100 * 8
                    # TODO: some gui for promo picking
    else:
        return int(input(input_message))
        # TODO: check if valid if not return -1


def pick_square(input_message: str) -> int:
    if draw_mode == "Lukas":
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    return position[0] // 100 + position[1] // 100 * 8
    else:
        data = input(input_message)
        x, y = data
        return (ord(x) - 97) + (8 - int(y)) * 8
        # TODO: check if valid if not return -1


draw_mode = "Lukas"#input("Jak chces vykreslovat sachovnici? Metod: konzole, Lukas: aplikace")
drawer = Drawer(draw_mode)

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
