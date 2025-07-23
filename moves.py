from dataclasses import dataclass
from typing import Generator
from board import Board
from constants import (
    UNCOLOR,
    BLACK,
    WHITE,
    KING,
    SWITCH_COLOR,
    ROCK,
    PAWN,
    KING,
    QUEEN,
    KNIGHT,
    BISHOP,
    UP,
    RIGHT,
    DOWN,
    LEFT,
)
from tile import fileA, fileH, rank2, rank7


@dataclass(frozen=True)
class Move:
    fr: int
    to: int
    promo: int | None = None


def check_detection(board: Board, curr_pos: int, to: int) -> bool:
    color = board[curr_pos] - board[curr_pos] % UNCOLOR
    deleted_place, board[to], board[curr_pos] = board[to], board[curr_pos], 0
    possible_moves = {"bishop": [], "knight": [], "rock": [], "pawn": []}
    king_pos = 0
    for x in range(len(board.board)):
        if board[x] - color == KING:
            possible_moves["bishop"] = bishop(board, x)
            possible_moves["knight"] = knight(board, x)
            possible_moves["rock"] = rock(board, x)
            possible_moves["pawn"] = pawn(board, x)
            king_pos = x
            break
    board[to], board[curr_pos] = deleted_place, board[to]
    for x in possible_moves["bishop"]:
        if (
            board[x] - SWITCH_COLOR[color] == BISHOP
            or board[x] - SWITCH_COLOR[color] == QUEEN
        ) and SWITCH_COLOR[color] == board[x] - board[x] % UNCOLOR:
            return False
    for x in possible_moves["knight"]:
        if (
            board[x] - SWITCH_COLOR[color] == KNIGHT
            and SWITCH_COLOR[color] == board[x] - board[x] % UNCOLOR
        ):
            return False
    for x in possible_moves["rock"]:
        if (
            board[x] - SWITCH_COLOR[color] == ROCK
            or board[x] - SWITCH_COLOR[color] == QUEEN
        ) and SWITCH_COLOR[color] == board[x] - board[x] % UNCOLOR:
            return False
    for x in possible_moves["pawn"]:
        if (
            board[x] - SWITCH_COLOR[color] == PAWN
            and SWITCH_COLOR[color] == board[x] - board[x] % UNCOLOR
            and x % 8 - king_pos % 8 != 0
        ):
            return False
    return True


def available_moves(board: Board) -> Generator[Move]:
    for move in all_moves(board):
        subboard = board.clone()
        subboard.move(move)

        king_under_attack = False  # TODO

        if king_under_attack:
            continue
        else:
            yield move


def rock(board: Board, pos: int) -> Generator[Move]:
    color = board[pos] - (board[pos] % UNCOLOR)

    for x in range(1, 8):
        p = pos + x * DOWN
        if p > 63:
            break
        if board[p] == 0:
            yield Move(pos, p)
            continue
        elif board[p] // color != 1:
            yield Move(pos, p)
        break

    for x in range(1, 8):
        p = pos + x * UP
        if p < 0:
            break
        if board[p] == 0:
            yield Move(pos, p)
            continue
        elif board[p] // color != 1:
            yield Move(pos, p)
        break

    for x in range(1, 8 - pos % 8):
        if board[pos + x] == 0:
            yield Move(pos, pos + x)
            continue
        elif board[pos + x] // color != 1:
            yield Move(pos, pos + x)
        break

    for x in range(1, pos % 8 + 1):
        if board[pos - x] == 0:
            yield Move(pos, pos - x)
            continue
        elif board[pos - x] // color != 1:
            yield Move(pos, pos - x)
        break


def pawn(board: Board, pos: int) -> Generator[Move]:
    color = board[pos] - board[pos] % UNCOLOR
    jump_to = 2

    if color == BLACK:
        if pos in rank7 and color == BLACK:
            jump_to = 3
        for x in range(1, jump_to):
            if board[pos + x * UP] == 0 and pos + x * UP < 64:
                yield Move(pos, pos + 8 * x)
            else:
                break
        if board[pos + DOWN + LEFT] // WHITE == 1 and pos not in fileA:
            yield Move(pos, pos + DOWN + LEFT)
        if board[pos + DOWN + RIGHT] // WHITE == 1 and pos not in fileH:
            yield Move(pos, pos + DOWN + RIGHT)

    elif color == WHITE:
        if pos in rank2 and color == WHITE:
            jump_to = 3
        for x in range(1, jump_to):
            if board[pos + x * DOWN] == 0:
                yield Move(pos, pos + x * DOWN)
            else:
                break
        if board[pos + UP + LEFT] // BLACK == 1 and pos not in fileA:
            yield Move(pos, pos + UP + LEFT)
        if board[pos + UP + RIGHT] // BLACK == 1 and pos not in fileH:
            yield Move(pos, pos + UP + RIGHT)


def king(board: Board, position: int) -> Generator[Move]:
    color = board[position] - board[position] % UNCOLOR

    if (
        board.white_ooo == True
        and board[position - 1] == 0
        and board[position - 2] == 0
        and board[position - 3] == 0
    ):
        yield Move(position, position - 2)

    if board.white_oo == True and board[position + 1] == 0 and board[position + 2] == 0:
        yield Move(position, position + 2)

    if (
        board.black_ooo == True
        and board[position - 1] == 0
        and board[position - 2] == 0
        and board[position - 3] == 0
    ):
        yield Move(position, position - 2)

    if board.black_oo == True and board[position + 1] == 0 and board[position + 2] == 0:
        yield Move(position, position + 2)

    for i in range(3):
        if (
            position - 7 - i > -1
            and board[position - 7 - i] // color != 1
            and abs(position % 8 - (position - 7 - i) % 8) < 2
        ):
            yield Move(position, position - 7 - i)

    for i in range(-1, 2, 2):
        if (
            64 > position + i > -1
            and board[position + i] // color != 1
            and abs(position % 8 - (position + i) % 8) < 2
        ):
            yield Move(position, position + i)

    for i in range(3):
        if (
            position + 7 + i < 64
            and board[position + 7 + i] // color != 1
            and abs(position % 8 - (position + 7 + i) % 8) < 2
        ):
            yield Move(position, position + 7 + i)


def knight(board, position: int) -> Generator[Move]:
    color = board[position] - board[position] % UNCOLOR
    for i in (UP + UP, DOWN + DOWN):
        if position + i < 0 or position + i > 63:
            continue
        for j in (LEFT, RIGHT):
            if abs((position + j) % 8 - position % 8) != 1:
                continue
            if board[position + i + j] // color != 1:
                yield Move(position, position + i + j)
    for i in (UP, DOWN):
        if 0 > position + i or position + i > 63:
            continue
        for j in (LEFT + LEFT, RIGHT + RIGHT):
            if abs((position + j) % 8 - position % 8) != 2:
                continue
            if board[position + i + j] // color != 1:
                yield Move(position, position + i + j)


def bishop(board: Board, position: int) -> Generator[Move]:
    color = board[position] - board[position] % UNCOLOR
    for x in range(1, 8):
        p = position + x * (DOWN + RIGHT)
        if p % 8 <= position % 8 or p > 63:
            break
        if board[p] == 0:
            yield Move(position, p)
            continue
        elif board[p] // color != 1:
            yield Move(position, p)
        break

    for x in range(1, 8):
        p = position + x * (UP + LEFT)
        if p % 8 >= position % 8 or p < 0:
            break
        if board[p] == 0:
            yield Move(position, p)
            continue
        elif board[p] // color != 1:
            yield Move(position, p)
        break

    for x in range(1, 8):
        p = position + x * (DOWN + LEFT)
        if p % 8 >= position % 8 or p > 63:
            break
        if board[p] == 0:
            yield Move(position, p)
            continue
        elif board[p] // color != 1:
            yield Move(position, p)
        break

    for x in range(1, 8):
        p = position + x * (UP + RIGHT)
        if p % 8 <= position % 8 or p < 0:
            break
        if board[p] == 0:
            yield Move(position, p)
            continue
        elif board[p] // color != 1:
            yield Move(position, p)
        break


def queen(board: Board, position: int) -> Generator[Move]:
    yield from rock(board, position)
    yield from bishop(board, position)


def check_mate(board, curr_pos, to):
    color = board[curr_pos] - board[curr_pos] % UNCOLOR
    deleted_place = board[to]
    board[to], board[curr_pos] = board[curr_pos], 0
    possible_moves = {}

    for i, x in enumerate(board):
        if x % UNCOLOR == ROCK:
            possible_moves[i] = rock(board, i, False)
        elif x % UNCOLOR == PAWN:
            possible_moves[i] = pawn(board, i, False)
        elif x % UNCOLOR == KNIGHT:
            possible_moves[i] = knight(board, i, False)
        elif x % UNCOLOR == BISHOP:
            possible_moves[i] = bishop(board, i, False)
        elif x % UNCOLOR == QUEEN:
            possible_moves[i] = queen(board, i, False)
        elif x % UNCOLOR == KING:
            possible_moves[i] = king(board, i, pieces_moved, False)
    for piece in list(possible_moves):
        for pos in possible_moves[piece]:
            if board[pos] % UNCOLOR == KING:
                board[to], board[curr_pos] = deleted_place, board[to]
                if board[curr_pos] // color == 1:
                    return False
    board[to], board[curr_pos] = deleted_place, board[to]
    return True


def all_moves(board: Board) -> Generator[Move]:
    for i, tile in enumerate(board.board):
        if tile // board.color == 1:
            piece = tile % board.color
            if piece == ROCK:
                yield from rock(board, i)
            elif piece == PAWN:
                yield from pawn(board, i)
            elif piece == KING:
                yield from king(board, i)
            elif piece == QUEEN:
                yield from queen(board, i)
            elif piece == KNIGHT:
                yield from knight(board, i)
            elif piece == BISHOP:
                yield from bishop(board, i)
