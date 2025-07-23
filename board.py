from constants import (BLACK_ROCK, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_PAWN, BLACK_KNIGHT,
                       WHITE_ROCK, WHITE_KING, WHITE_KNIGHT, WHITE_PAWN, WHITE_QUEEN, WHITE_BISHOP,
                       BLACK, WHITE, UNICODE_CODING, Moves, PAWN, QUEEN,
                       BISHOP, KNIGHT, ROCK, KING, SWITCHABLE, POSSIBLE_COLORS, UNCOLOR)
import pygame

class Drawer:
    def __init__(self, mode):
        self.mode = mode
        if self.mode != "Lukas": pass
        self.screen = pygame.display.set_mode((100 * 8, 100 * 8))
        pygame.font.init()
        self.font = pygame.font.Font("./font/DejaVuSans.ttf", 80) #segoeuisymbol
        pygame.init()

    def draw(self, board):
        if self.mode == "Lukas":
            self.screen.fill("black")
            for y in range(8):
                for x in range(8):
                    pos = y * 8 + x
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(self.screen, (118, 150, 86), (x * 100, y * 100, 100, 100))
                    else:
                        pygame.draw.rect(self.screen, (238, 238, 210), (x * 100, y * 100, 100, 100))
                    self.screen.blit(self.font.render(UNICODE_CODING[board[pos]], True, (0, 0, 0)), (x * 100 + 10, y * 100 + 5))
            pygame.display.flip()
        else:
            string = "|"
            for i, pies in enumerate(board):
                if i % 8 == 0 and i != 0:
                    string += "\n|"
                string += UNICODE_CODING[pies] + "|"
            print(string)




class Board:
    def __init__(self, draw_mode):
        self.board = [0 for _ in range(64)]
        self.draw_mode = draw_mode
        self.white_oo = True
        self.white_ooo = True
        self.black_oo = True
        self.black_ooo = True

    def __str__(self):
        string = "|"
        for i, pies in enumerate(self.board):
            if i % 8 == 0 and i != 0:
                string += "\n|"
            string += UNICODE_CODING[pies] + "|"
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

    def move(self, move_from, move_to, move_promo):
        moving_piece = self.board[move_from] % UNCOLOR
        moving_color = self.board[move_from] - moving_piece
        if moving_piece == KING and move_from - move_to == 2:
            self.board[move_to] = self.board[move_from]
            self.board[move_from] = 0
            self.board[move_to + 1] = self.board[move_from - 4]
            self.board[move_from - 4] = 0

        elif moving_piece == KING and move_to - move_from == 2:
            self.board[move_to] = self.board[move_from]
            self.board[move_from] = 0
            self.board[move_to - 1] = self.board[move_from + 3]
            self.board[move_from + 3] = 0
        else:
            self.board[move_to] = self.board[move_from]
            self.board[move_from] = 0
        if moving_piece == PAWN and move_to // 8 in (0, 7):
            self.board[move_to] = move_promo
        if moving_piece == KING:
            if moving_color == WHITE:
                self.board.white_ooo = False
                self.board.white_oo = False
            else:
                self.board.black_ooo = False
                self.board.black_oo = False
        if moving_piece == ROCK:
            if move_from == 0:
                self.board.black_ooo = False
            if move_from == 7:
                self.board.black_oo = False
            if move_from == 56:
                self.board.white_ooo = False
            if move_from == 63:
                self.board.white_oo = False


class Game:
    def __init__(self, mode: str):
        self.mode = mode
        self.draw_mode = input("Jak chces vykreslovat sachovnici? Metod: konzole, Lukas: aplikace")
        self.drawer = Drawer(self.draw_mode)
        self.board = []
        self.moves = None
        self.pieces_moved = {
            0: False,
            4: False,
            7: False,
            56: False,
            60: False,
            63: False,
        }
        self.black_king = 4
        self.white_king = 60

    def start(self):
        chess = Board(self.draw_mode)
        self.moves = Moves(self.pieces_moved)
        self.board = chess.board
        chess.create_board()
        color = 0
        while True:
            self.drawer.draw(self.board)
            if POSSIBLE_COLORS[color] == BLACK:
                print("HRAJE CERNY")
            else:
                print("HRAJE BILY")
            self.get_move(POSSIBLE_COLORS[color])
            color = abs(color - 1)
            self.is_check_mate()

    def get_move(self, color: int):
        return self.chose_pies(color)

    def chose_pies(self, color):
        piece = -1
        move = False
        to_move = -1
        move_promo = None
        while not move:
            piece = to_move
            while self.board[piece] // color != 1 or piece == -1:
                piece = self.event_listener("Jakou chces figurku?")
                if type(piece) is str:
                    x, y = piece
                    piece = (ord(x) - 97) + (8 - int(y)) * 8
            move, to_move = self.chose_position(piece, color)
        if self.board[to_move] % UNCOLOR == PAWN and to_move // 8 in (0, 7):
            move_promo = self.choose_piece(color)
        return piece, to_move

    def chose_position(self, piece, color):
        positions = []
        possible_moves = []
        if self.board[piece] % color == ROCK:
            positions = self.moves.rock(self.board, piece)
        elif self.board[piece] % color == PAWN:
            positions = self.moves.pawn(self.board, piece)
        elif self.board[piece] % color == KING:
            positions = self.moves.king(self.board, piece)
        elif self.board[piece] % color == QUEEN:
            positions = self.moves.queen(self.board, piece)
        elif self.board[piece] % color == KNIGHT:
            positions = self.moves.knight(self.board, piece)
        elif self.board[piece] % color == BISHOP:
            positions = self.moves.bishop(self.board, piece)
        for i in range(len(positions)):
            possible_moves.append(chr((positions[i] % 8) + 97) + str(8 - (positions[i] // 8)))
        position = self.event_listener(f"Kam chces tahnout? Mozne pozice: {possible_moves}")
        if type(position) is str:
            x, y = position
            position = (ord(x) - 97) + (8 - int(y)) * 8
        if position in positions:
            return True, position
        return False, position

    def choose_piece(self, color):
        while True:
            piece = self.event_listener("Za jakou figurku chces vymenit pesaka")
            if piece not in SWITCHABLE: continue
            return color + piece

    def event_listener(self, input_message):
        if self.draw_mode == "Lukas":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return -1
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        position = pygame.mouse.get_pos()
                        position = position[0] // 100 + position[1] // 100 * 8
                        return position
        else:
            data = input(input_message)
            return data

    def is_check_mate(self):
        if (not self.moves.king(self.board, self.white_king, self.pieces_moved) or
                not self.moves.king(self.board, self.black_king, self.pieces_moved)):
            # self.moves.check_mate()
            pass

