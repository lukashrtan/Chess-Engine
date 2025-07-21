BLACK_ROCK = 201
BLACK_PAWN = 202
BLACK_KING = 203
BLACK_QUEEN = 204
BLACK_KNIGHT = 205
BLACK_BISHOP = 206

WHITE_ROCK = 101
WHITE_PAWN = 102
WHITE_KING = 103
WHITE_QUEEN = 104
WHITE_KNIGHT = 105
WHITE_BISHOP = 106

WHITE = 100
BLACK = 200

ROCK = 1
PAWN = 2
KING = 3
QUEEN = 4
KNIGHT = 5
BISHOP = 6

SWITCHABLE = [
    KNIGHT,
    BISHOP,
    ROCK,
    QUEEN,
]

class Moves:
    def __init__(self, color):
        self.color = color
    def rock(self, board, position):
        positions = []
        for x in range(1, 8):
            if position + x * 8 > 63: break
            if board[position + x * 8] == 0:
                positions.append(position + x * 8)
                continue
            elif board[position + x * 8] // self.color != 1:
                positions.append(position + x * 8)
            break

        for x in range(1, 8):
            if position - x * 8 < 0: break
            print(position - x * 8, x, position)
            if board[position - x * 8] == 0:
                positions.append(position - x * 8)
                continue
            elif board[position - x * 8] // self.color != 1:
                positions.append(position - x * 8)
            break

        for x in range(1, 8 - position % 8):
            if board[position + x] == 0:
                positions.append(position + x)
                continue
            elif board[position + x] // self.color != 1:
                positions.append(position + x)
            break

        for x in range(1, position % 8 + 1):
            if board[position - x] == 0:
                positions.append(position - x)
                continue
            elif board[position - x] // self.color != 1:
                positions.append(position - x)
            break
        return positions

    def pawn(self, board, position):
        positions = []
        jump_to = 2

        if self.color == BLACK:
            if 7 < position < 16 and self.color == BLACK:
                jump_to = 3
            for x in range(1, jump_to):
                if board[position + 8 * x] == 0 and position + 8 * x < 64:
                    positions.append(position + 8 * x)
                else:
                    break
            if board[position + 7] // WHITE == 1 and position % 8 != 0:
                positions.append(position + 7)
            if board[position + 9] // WHITE == 1 and position % 8 != 7:
                positions.append(position + 9)

        elif self.color == WHITE:
            if 47 < position < 56 and self.color == WHITE:
                jump_to = 3
            for x in range(1, jump_to):
                if board[position - 8 * x] == 0:
                    positions.append(position - 8 * x)
                else:
                    break
            if board[position - 7] // BLACK == 1 and position % 8 != 7:
                positions.append(position - 7)
            if board[position - 9] // BLACK == 1 and position % 8 != 0:
                positions.append(position - 9)
        return positions

        return positions

    def king(self, board, position):
        positions = []
        for i in range(3):
            if position - 7 - i > -1 and board[position - 7 - i]  // self.color != 1 and abs(position % 8 - (position - 7 - i) % 8) < 2:
                positions.append(position - 7 - i)

        for i in range(-1, 2, 2):
            if  position + i < 64 and position + i > -1 and board[position + i] // self.color != 1 and abs(position % 8 - (position + i) % 8) < 2:
                positions.append(position + i)

        for i in range(3):
            if  position + 7 + i < 64 and board[position + 7 + i]  // self.color != 1 and abs(position % 8 - (position + 7 + i) % 8) < 2:
                positions.append(position + 7 + i)

        return positions



    def knight(self, board, position):
        positions = []
        for i in (-16, 16):
            if 0 > position + i or position + i > 63: continue
            for j in (-1, 1):
                if abs((position + j) % 8 - position % 8) != 1: continue
                if board[position + i + j] // self.color != 1:
                    positions.append(position + i + j)
        for i in (-2, 2):
            if abs((position + i) % 8 - position % 8 != 2): continue
            for j in (-8, 8):
                if 0 > position + j or position + j > 63: continue
                if board[position + i + j] // self.color != 1:
                    positions.append(position + i + j)
        return positions


    def bishop(self, board, position):
        positions = []
        for x in range(1, 8):
            if (position + x * 9) % 8 <= position % 8 or position + x * 9 > 63: break
            if board[position + x * 9] == 0:
                positions.append(position + x * 9)
                continue
            elif board[position + x * 9] // self.color != 1:
                positions.append(position + x * 9)
            break
        for x in range(1, 8):
            if (position - x * 9) % 8 >= position % 8 or position - x * 9 < 0: break
            if board[position - x * 9] == 0:
                positions.append(position - x * 9)
                continue
            elif board[position - x * 9] // self.color != 1:
                positions.append(position - x * 9)
            break
        for x in range(1, 8):
            if (position + x * 7) % 8 >= position % 8 or position + x * 7 > 63: break
            if board[position + x * 7] == 0:
                positions.append(position + x * 7)
                continue
            elif board[position + x * 7] // self.color != 1:
                positions.append(position + x * 7)
            break
        for x in range(1, 8):
            if (position - x * 7) % 8 <= position % 8 or position - x * 7 < 0: break
            if board[position - x * 7] == 0:
                positions.append(position - x * 7)
                continue
            elif board[position - x * 7] // self.color != 1:
                positions.append(position - x * 7)
            break
        return positions

    def queen(self, board, position):
        positions = []
        for x in self.rock(board, position):
            positions.append(x)
        for x in self.bishop(board, position):
            positions.append(x)
        return positions





UNICODE_CODING = {
    WHITE_ROCK: "♖",
    WHITE_PAWN: "♙",
    WHITE_KING: "♔",
    WHITE_QUEEN: "♕",
    WHITE_KNIGHT: "♘",
    WHITE_BISHOP: "♗",

    BLACK_QUEEN: "♛",
    BLACK_PAWN: "♟",
    BLACK_KING: "♚",
    BLACK_ROCK: "♜",
    BLACK_KNIGHT: "♞",
    BLACK_BISHOP: "♝",

    0: " "
}

