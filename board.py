import numpy as np
from constants import (
    BLACK_BISHOP,
    BLACK_KING,
    BLACK_KNIGHT,
    BLACK_PAWN,
    BLACK_QUEEN,
    BLACK_ROCK,
    EMPTY,
    KING,
    ROCK,
    SWITCH_COLOR,
    UNCOLOR,
    UNICODE_CODING,
    WHITE,
    WHITE_BISHOP,
    WHITE_KING,
    WHITE_KNIGHT,
    WHITE_PAWN,
    WHITE_QUEEN,
    WHITE_ROCK,
)
from moves import Move
from tile import (
    A1,
    A8,
    B1,
    B8,
    C1,
    C8,
    D1,
    D8,
    E1,
    E8,
    F1,
    F8,
    G1,
    G8,
    H1,
    H8,
    rank2,
    rank7,
)


class Board:
    def __init__(self) -> None:
        #self.board = np.array([0 for _ in range(64)])
        self.board = [0 for _ in range(64)]

        self.color = WHITE
        self.white_oo = True
        self.white_ooo = True
        self.black_oo = True
        self.black_ooo = True
        self.white_king_pos = 60
        self.black_king_pos = 4

    def clone(self, color: int|None = None) -> "Board":
        new = Board()
        new.board = self.board[:]
        if color is None:
            new.color = self.color
        else:
            new.color = color
        new.white_oo = self.white_oo
        new.white_ooo = self.white_ooo
        new.black_oo = self.black_oo
        new.black_ooo = self.black_ooo
        return new

    def __str__(self) -> str:
        string = "|"
        for i, pies in enumerate(self.board):
            if i % 8 == 0 and i != 0:
                string += "\n|"
            string += UNICODE_CODING[pies] + "|"
        return string

    def __getitem__(self, i: int) -> int:
        return self.board[i]

    def __setitem__(self, i: int, v: int) -> None:
        self.board[i] = v

    @staticmethod
    def create_board() -> "Board":
        b = Board()
        b.color = WHITE
        b.board[A8] = BLACK_ROCK
        b.board[B8] = BLACK_KNIGHT
        b.board[C8] = BLACK_BISHOP
        b.board[D8] = BLACK_QUEEN
        b.board[E8] = BLACK_KING
        b.board[F8] = BLACK_BISHOP
        b.board[G8] = BLACK_KNIGHT
        b.board[H8] = BLACK_ROCK
        for tile in rank7:
            b.board[tile] = BLACK_PAWN
        # b.board[8] = WHITE_PAWN
        b.board[A1] = WHITE_ROCK
        b.board[B1] = WHITE_KNIGHT
        b.board[C1] = WHITE_BISHOP
        b.board[D1] = WHITE_QUEEN
        b.board[E1] = WHITE_KING
        b.board[F1] = WHITE_BISHOP
        b.board[G1] = WHITE_KNIGHT
        b.board[H1] = WHITE_ROCK
        for tile in rank2:
            b.board[tile] = WHITE_PAWN
        # b.board[48] = BLACK_PAWN

        return b

    def move(self, move: Move) -> "Board":
        # rošáda
        moving_piece = self.board[move.fr] % UNCOLOR
        moving_color = self.color
        if moving_piece == KING and move.fr - move.to == 2:
            self.board[move.to] = self.board[move.fr]
            self.board[move.fr] = EMPTY
            self.board[move.to + 1] = self.board[move.fr - 4]
            self.board[move.fr - 4] = EMPTY
            if moving_color == WHITE:
                self.white_king_pos = move.to
            else:
                self.black_king_pos = move.to

        # rošáda
        elif moving_piece == KING and move.to - move.fr == 2:
            self.board[move.to] = self.board[move.fr]
            self.board[move.fr] = EMPTY
            self.board[move.to - 1] = self.board[move.fr + 3]
            self.board[move.fr + 3] = EMPTY
            if moving_color == WHITE:
                self.white_king_pos = move.to
            else:
                self.black_king_pos = move.to

        # prostě tah
        else:
            self.board[move.to] = self.board[move.fr]
            self.board[move.fr] = EMPTY
            if moving_piece == KING:
                if moving_color == WHITE:
                    self.white_king_pos = move.to
                else:
                    self.black_king_pos = move.to

        # promo
        if move.promo is not None:
            self.board[move.to] = move.promo

        # castling rights
        if moving_piece == KING:
            if moving_color == WHITE:
                self.white_ooo = False
                self.white_oo = False
            else:
                self.black_ooo = False
                self.black_oo = False
        if moving_piece == ROCK:
            if move.fr == A8:
                self.black_ooo = False
            if move.fr == H8:
                self.black_oo = False
            if move.fr == A1:
                self.white_ooo = False
            if move.fr == H1:
                self.white_oo = False

        self.color = SWITCH_COLOR[self.color]
        return self
