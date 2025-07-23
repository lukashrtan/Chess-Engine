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

POSSIBLE_COLORS = (WHITE, BLACK)

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
    def __init__(self, pieces_moved):
        self.pieces_moved = pieces_moved

    def rock(self, board, position, out=True):
        color = board[position] - board[position] % 100
        positions = []
        for x in range(1, 8):
            if position + x * 8 > 63: break
            if board[position + x * 8] == 0:
                positions.append(position + x * 8)
                continue
            elif board[position + x * 8] // color != 1:
                positions.append(position + x * 8)
            break

        for x in range(1, 8):
            if position - x * 8 < 0: break
            if board[position - x * 8] == 0:
                positions.append(position - x * 8)
                continue
            elif board[position - x * 8] // color != 1:
                positions.append(position - x * 8)
            break

        for x in range(1, 8 - position % 8):
            if board[position + x] == 0:
                positions.append(position + x)
                continue
            elif board[position + x] // color != 1:
                positions.append(position + x)
            break

        for x in range(1, position % 8 + 1):
            if board[position - x] == 0:
                positions.append(position - x)
                continue
            elif board[position - x] // color != 1:
                positions.append(position - x)
            break
        return self.available_moves(board, position, positions, out)

    def pawn(self, board, position, out=True):
        color = board[position] - board[position] % 100
        positions = []
        jump_to = 2

        if color == BLACK:
            if 7 < position < 16 and color == BLACK:
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

        elif color == WHITE:
            if 47 < position < 56 and color == WHITE:
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
        return self.available_moves(board, position, positions, out)

    def king(self, board, position, pieces_moved, out=True):
        color = board[position] - board[position] % 100
        positions = []
        try:
            if pieces_moved[position] == False and pieces_moved[position-4] == False and board[position-1] == 0 and board[position-2] == 0 and board[position-3] == 0:
                positions.append(position - 2)
            if pieces_moved[position] == False and pieces_moved[position+3] == False and board[position+1] == 0 and board[position+2] == 0:
                positions.append(position + 2)
        except Exception:
            pass
        for i in range(3):
            if position - 7 - i > -1 and board[position - 7 - i]  // color != 1 and abs(position % 8 - (position - 7 - i) % 8) < 2:
                positions.append(position - 7 - i)

        for i in range(-1, 2, 2):
            if  64 > position + i > -1 and board[position + i] // color != 1 and abs(position % 8 - (position + i) % 8) < 2:
                positions.append(position + i)

        for i in range(3):
            if  position + 7 + i < 64 and board[position + 7 + i]  // color != 1 and abs(position % 8 - (position + 7 + i) % 8) < 2:
                positions.append(position + 7 + i)

        return self.available_moves(board, position, positions, out)



    def knight(self, board, position, out=True):
        color = board[position] - board[position] % 100
        positions = []
        for i in (-16, 16):
            if 0 > position + i or position + i > 63: continue
            for j in (-1, 1):
                if abs((position + j) % 8 - position % 8) != 1: continue
                if board[position + i + j] // color != 1:
                    positions.append(position + i + j)
        for i in (-2, 2):
            if abs((position + i) % 8 - position % 8 != 2): continue
            for j in (-8, 8):
                if 0 > position + j or position + j > 63: continue
                if board[position + i + j] // color != 1:
                    positions.append(position + i + j)
        return self.available_moves(board, position, positions, out)


    def bishop(self, board, position, out=True):
        color = board[position] - board[position] % 100
        positions = []
        for x in range(1, 8):
            if (position + x * 9) % 8 <= position % 8 or position + x * 9 > 63: break
            if board[position + x * 9] == 0:
                positions.append(position + x * 9)
                continue
            elif board[position + x * 9] // color != 1:
                positions.append(position + x * 9)
            break
        for x in range(1, 8):
            if (position - x * 9) % 8 >= position % 8 or position - x * 9 < 0: break
            if board[position - x * 9] == 0:
                positions.append(position - x * 9)
                continue
            elif board[position - x * 9] // color != 1:
                positions.append(position - x * 9)
            break
        for x in range(1, 8):
            if (position + x * 7) % 8 >= position % 8 or position + x * 7 > 63: break
            if board[position + x * 7] == 0:
                positions.append(position + x * 7)
                continue
            elif board[position + x * 7] // color != 1:
                positions.append(position + x * 7)
            break
        for x in range(1, 8):
            if (position - x * 7) % 8 <= position % 8 or position - x * 7 < 0: break
            if board[position - x * 7] == 0:
                positions.append(position - x * 7)
                continue
            elif board[position - x * 7] // color != 1:
                positions.append(position - x * 7)
            break
        return self.available_moves(board, position, positions, out)

    def queen(self, board, position, out=True):
        positions = []
        for x in self.rock(board, position, out):
            positions.append(x)
        for x in self.bishop(board, position, out):
            positions.append(x)
        return self.available_moves(board, position, positions, out)

    def available_moves(self, board, position, positions, out):
        if not out:
            return positions
        to_delete = []
        print(positions, 0)
        for x in range(len(positions)):
            if not self.check_detection(board, position, positions[x]):
                print("add")
                to_delete.append(x)
        for x in range(len(to_delete) - 1, -1, -1):
            print(x)
            del positions[x]
        print(positions, 1)
        return positions

    def check_detection(self, board, curr_pos, to):
        print("checking")
        deleted_place = board[to]
        color = board[curr_pos] - board[curr_pos] % 100
        board[to], board[curr_pos] = board[curr_pos], 0
        possible_moves = {}
        for i, x in enumerate(board):
            if x % 100 == ROCK:
                possible_moves[i] = self.rock(board, i, False)
            elif x % 100 == PAWN:
                possible_moves[i] = self.pawn(board, i, False)
            elif x % 100 == KNIGHT:
                possible_moves[i] = self.knight(board, i, False)
            elif x % 100 == BISHOP:
                possible_moves[i] = self.bishop(board, i, False)
            elif x % 100 == QUEEN:
                possible_moves[i] = self.queen(board, i, False)
            elif x % 100 == KING:
                possible_moves[i] = self.king(board, i, self.pieces_moved, False)
        for piece in list(possible_moves):
            for pos in possible_moves[piece]:
                if board[pos] % 100 == KING:
                    board[to], board[curr_pos] = deleted_place, board[to]
                    if board[curr_pos] // color == 1:
                        return False
        board[to], board[curr_pos] = deleted_place, board[to]
        return True









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