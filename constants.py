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
        if 7 < position > 16 and self.color == 200:
            positions.append(position+8)

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

    0: "  "
}

