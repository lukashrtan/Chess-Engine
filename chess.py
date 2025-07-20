from constants import (BLACK_ROCK, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_PAWN, BLACK_KNIGHT,
                       WHITE_ROCK, WHITE_KING, WHITE_KNIGHT, WHITE_PAWN, WHITE_QUEEN, WHITE_BISHOP,
                       BLACK, WHITE, UNICODE_CODING)

class Game:
    def __init__(self, mode):
        self.mode = mode

    def start(self):
        chess = Chess()
        chess.create_board()
        print(chess.__str__())
        while True:
            chess.move(BLACK)
            print(chess.__str__())
        pass




class Chess:
    def __init__(self):
        self.board = [0 for x in range(64)]

    def __str__(self):
        string = ""
        for i, pies in enumerate(self.board):
            if i % 8 == 0 and i != 0:
                string += "\n"
            string += UNICODE_CODING[pies] + " | "
        return string

    def create_board(self):
        self.board[0] = BLACK_ROCK
        self.board[1] = BLACK_KNIGHT
        self.board[2] = BLACK_BISHOP
        self.board[3] = BLACK_QUEEN
        self.board[4] = BLACK_KING
        self.board[5] = BLACK_BISHOP
        self.board[6] = BLACK_KNIGHT
        self.board[7] = BLACK_ROCK
        for x in range(8):
            self.board[8 + x] = BLACK_PAWN
        self.board[63] = WHITE_ROCK
        self.board[62] = WHITE_KNIGHT
        self.board[61] = WHITE_BISHOP
        self.board[60] = WHITE_KING
        self.board[59] = WHITE_QUEEN
        self.board[58] = WHITE_BISHOP
        self.board[57] = WHITE_KNIGHT
        self.board[56] = WHITE_ROCK
        for x in range(8):
            self.board[55 - x] = WHITE_PAWN

    def move(self, color):
        pies = self.chose_pies(color)

        where = int(input("Kam chces tahnout?"))


        self.board[where] = self.board[pies]
        self.board[pies] = 0

    def chose_pies(self, color):
        pies = -1
        while True:
            while self.board[pies] // color != 1 or pies == -1:
                pies = int(input("Jakou chces figurku?"))
            self.chose_position()
        return pies

    def chose_position(self, pies):
        PIEC_MOVE[pies].get

