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


def check_detection(board: Board, from_pos: int, to_pos: int) -> bool:
    color = board[from_pos] - board[from_pos] % UNCOLOR
    if from_pos == to_pos:
        deleted_place = board[to_pos]
    else:
        deleted_place, board[to_pos], board[from_pos] = board[to_pos], board[from_pos], 0
    for pos in range(len(board.board)):
        if board[pos] - color == KING:
            bishop_moves = bishop(board, pos)
            knight_moves = knight(board, pos)
            rock_moves = rock(board, pos)
            pawn_moves = pawn(board, pos)
            king_pos = pos
            break
    else:
        raise AssertionError()
    board[to_pos], board[from_pos] = deleted_place, board[to_pos]
    for move in bishop_moves:
        to = move.to
        if (
            board[to] - SWITCH_COLOR[color] == BISHOP
            or board[to] - SWITCH_COLOR[color] == QUEEN
        ) and SWITCH_COLOR[color] == board[to] - board[to] % UNCOLOR:
            return False
    for move in knight_moves:
        to = move.to
        if (
            board[to] - SWITCH_COLOR[color] == KNIGHT
            and SWITCH_COLOR[color] == board[to] - board[to] % UNCOLOR
        ):
            return False
    for move in rock_moves:
        to = move.to
        if (
            board[to] - SWITCH_COLOR[color] == ROCK
            or board[to] - SWITCH_COLOR[color] == QUEEN
        ) and SWITCH_COLOR[color] == board[to] - board[to] % UNCOLOR:
            return False
    for move in pawn_moves:
        to = move.to
        if (
            board[to] - SWITCH_COLOR[color] == PAWN
            and SWITCH_COLOR[color] == board[to] - board[to] % UNCOLOR
            and to % 8 - king_pos % 8 != 0
        ):
            return False
    return True


def available_moves(board: Board) -> Generator[Move]:
    for move in all_moves(board):
        king_under_attack = check_detection(board, move.fr, move.to)
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


def check_mate(board: Board, king_pos: int) -> bool|None:
    if not available_moves(board):
        if check_detection(board, king_pos, king_pos):
            return None
        return True
    return False


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
