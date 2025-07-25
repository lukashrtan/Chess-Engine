from moves import check_mate, is_square_under_attack, rock
import pygame

from board import Board
from chess_engine import computer_move
from tile import rank7
from constants import BLACK, UNAVAILABLE_MOVE, SWITCHABLE, WHITE, UNCOLOR, PAWN, KNIGHT, QUEEN, KING, BISHOP
from drawer import Drawer
from moves import Move, available_moves, available_moves_specific_pos, pawn, king, queen, bishop, knight, queen
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

        if board[from_tile] % UNCOLOR == PAWN:
            drawer.draw(board, pos_to_move=list(available_moves_specific_pos(board, list(pawn(board, from_tile)))))
        elif board[from_tile] % UNCOLOR == KNIGHT:
            drawer.draw(board, pos_to_move=list(available_moves_specific_pos(board, list(knight(board, from_tile)))))
        elif board[from_tile] % UNCOLOR == QUEEN:
            drawer.draw(board, pos_to_move=list(available_moves_specific_pos(board, list(queen(board, from_tile)))))
        elif board[from_tile] % UNCOLOR == KING:
            drawer.draw(board, pos_to_move=list(available_moves_specific_pos(board, list(king(board, from_tile)))))
        elif board[from_tile] % UNCOLOR == BISHOP:
            drawer.draw(board, pos_to_move=list(available_moves_specific_pos(board, list(bishop(board, from_tile)))))
        else:
            drawer.draw(board, pos_to_move=list(available_moves_specific_pos(board, list(rock(board, from_tile)))))
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
            promo_piece = pick_promo(matching_moves[0].fr)
            for move in matching_moves:
                if move.promo == promo_piece:
                    return move


def pick_promo(from_pos: int) -> int:
    drawer.draw(board, from_pos)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if board.color == BLACK:
                    position = (800 - position[0], 800 - position[1])
                print(position)
                if position[0] // 100 == from_pos % 8:
                    if from_pos in rank7:
                        if position[1] // 100 not in range(len(SWITCHABLE)): continue
                        return SWITCHABLE[position[1] // 100] + board.color
                    else:
                        if abs(position[1] // 100 - 7) not in range(len(SWITCHABLE)): continue
                        return SWITCHABLE[abs(position[1] // 100 - 7)] + board.color



def pick_square() -> int:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if board.color == BLACK:
                    position = (800 - position[0], 800 - position[1])
                return position[0] // 100 + position[1] // 100 * 8


drawer = Drawer()

board = Board.create_board()

while True:
    drawer.draw(board)
    king = board.black_king_pos
    check_mate(board, board.white_king_pos)
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

    # drawer.draw(board)
    # #check_mate(board, board.black_king_pos)
    # if board.color == BLACK:
    #     print("HRAJE CERNY")
    # else:
    #     print("HRAJE BILY")
    # start = time.time()
    # board.move(computer_move(board))
    # print(time.time()-start)

