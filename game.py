from board import Board
from drawer import Drawer
from constants import (UNCOLOR, BLACK, PAWN, ROCK, KING, QUEEN, KNIGHT, SWITCHABLE)
from moves import (rock, pawn, king, queen, knight, bishop, Move, available_moves_specific_pos)
import pygame




def chose_piece() -> Move:
    tile = -1
    move = False
    to_move = -1
    while not move:
        tile = to_move
        while board[tile] // board.color != 1 or tile == -1:
            tile = event_listener("Jakou chces figurku?")
            if type(tile) is str:
                x, y = tile
                tile = (ord(x) - 97) + (8 - int(y)) * 8
        move, to_move = chose_position(board[tile] - board.color, tile)
        print("end?", move, to_move)
    if board[to_move] % UNCOLOR == PAWN and to_move // 8 in (0, 7):
        promo = chose_promotion()
    else:
        promo = None
    print(Move(tile, to_move, promo))
    return Move(tile, to_move, promo)

def chose_position(piece: int, pos: int) -> tuple[bool, int]:
    if piece == QUEEN:
        positions = list(queen(board, pos))
    elif piece == KNIGHT:
        positions = list(knight(board, pos))
    elif piece == ROCK:
        positions = list(rock(board, pos))
    elif piece == PAWN:
        positions = list(pawn(board, pos))
    elif piece == KING:
        positions = list(king(board, pos))
    else:
        positions = list(bishop(board, pos))
    position = event_listener(f"Kam chces tahnout? Mozne pozice: {positions}")
    if type(position) is str:
        x, y = position
        position = (ord(x) - 97) + (8 - int(y)) * 8
    for move in list(available_moves_specific_pos(board, positions)):
        if position == move.to:
            return True, position
    return False, position

def chose_promotion():
    while True:
        piece = event_listener("Za jakou figurku chces vymenit pesaka")
        if piece not in SWITCHABLE: continue
        return board.color + piece

def event_listener(input_message):
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
        return data


draw_mode = "Lukas"#input("Jak chces vykreslovat sachovnici? Metod: konzole, Lukas: aplikace")
drawer = Drawer(draw_mode)

board = Board.create_board()

while True:
    drawer.draw(board)
    if board.color == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
    board.move(chose_piece())