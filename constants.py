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
            if position + x * 8 < 64 and board[position + x * 8] == 0:
                positions.append(position + x * 8)
                continue
            elif board[position + x * 8] // self.color != 1:
                positions.append(position + x * 8)
            break

        for x in range(1, 8):
            if position - x * 8 > 0 and board[position - x * 8] == 0:
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

    def pown(self, board, position):
        positions = []
        if 7 < position > 16 and self.color == 200:
            positions.append(position+8)





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

