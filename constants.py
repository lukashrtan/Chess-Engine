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



class Moves:
    def Rock(self, board, position):
        positions = []
        for x in range(1, 8):
            if position + x * 8 < 64 and self.board[position + x * 8] == 0:
                positions.append(position + x * 8)
            else:
                break

        for x in range(1, 8):
            if position - x * 8 > 64 and self.board[position - x * 8] == 0:
                positions.append(position + x * 8)
            else:
                break

        for x in range(1, 8 - position % 8):
            if self.board[position + x] == 0:
                positions.append(position + x)
            else:
                break

        for x in range(1, position % 8 + 1):
            if self.board[position - x] == 0:
                positions.append(position - x)
            else:
                break
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

