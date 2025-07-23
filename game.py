from board import Board
from drawer import Drawer
from constants import (UNCOLOR, BLACK, WHITE, PAWN, ROCK, KING, QUEEN, KNIGHT, BISHOP, SWITCHABLE)
from moves import (rock, pawn, king, queen, knight, bishop)
import pygame




def chose_piece():
    piece = -1
    move = False
    to_move = -1
    while not move:
        piece = to_move
        while board[piece] // board.color != 1 or piece == -1:
            piece = event_listener("Jakou chces figurku?")
            if type(piece) is str:
                x, y = piece
                piece = (ord(x) - 97) + (8 - int(y)) * 8
        move, to_move = chose_position(piece, board.color)
    if board[to_move] % UNCOLOR == PAWN and to_move // 8 in (0, 7):
        choose_piece()
    return piece, to_move

def chose_position(piece, color):
    positions = []
    possible_moves = []
    if board[piece] % color == ROCK:
        positions = rock(board, piece)
    elif board[piece] % color == PAWN:
        positions = pawn(board, piece)
    elif board[piece] % color == KING:
        positions = king(board, piece)
    elif board[piece] % color == QUEEN:
        positions = queen(board, piece)
    elif board[piece] % color == KNIGHT:
        positions = knight(board, piece)
    elif board[piece] % color == BISHOP:
        positions = bishop(board, piece)
    for i in positions:
        possible_moves.append(chr((i.to % 8) + 97) + str(8 - (i.to // 8)))
    position = event_listener(f"Kam chces tahnout? Mozne pozice: {possible_moves}")
    if type(position) is str:
        x, y = position
        position = (ord(x) - 97) + (8 - int(y)) * 8
    if position in positions:
        return True, position
    return False, position

def choose_piece():
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
                    position = position[0] // 100 + position[1] // 100 * 8
                    return position
    else:
        data = input(input_message)
        return data


draw_mode = input("Jak chces vykreslovat sachovnici? Metod: konzole, Lukas: aplikace")
drawer = Drawer(draw_mode)

board = Board.create_board()

while True:
    drawer.draw(board)
    if board.color == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
    chose_piece()