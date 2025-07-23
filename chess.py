from constants import (BLACK_ROCK, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_PAWN, BLACK_KNIGHT,
                       WHITE_ROCK, WHITE_KING, WHITE_KNIGHT, WHITE_PAWN, WHITE_QUEEN, WHITE_BISHOP,
                       BLACK, WHITE, UNICODE_CODING, Moves, PAWN, QUEEN,
                       BISHOP, KNIGHT, ROCK, KING, SWITCHABLE, POSSIBLE_COLORS)
import pygame

class Game:
    def __init__(self, mode):
        self.mode = mode
        self.draw_mode = input("Jak chces vykreslovat sachovnici? Metod: konzole, Lukas: aplikace")
        self.drawer = Drawer(self.draw_mode)

    def start(self):
        chess = Chess(self.draw_mode)
        chess.create_board()
        color = 0
        while True:
            self.drawer.draw(chess.board)
            if POSSIBLE_COLORS[color] == BLACK:
                print("HRAJE CERNY")
            else:
                print("HRAJE BILY")
            chess.move(POSSIBLE_COLORS[color])
            color = abs(color - 1)

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





class Chess:
    def __init__(self, draw_mode):
        self.board = [0 for _ in range(64)]
        self.draw_mode = draw_mode
        self.pieces_moved = {
            0: False,
            4: False,
            7: False,
            56: False,
            60: False,
            63: False,
        }

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

    def move(self, color):
        piece, where = self.chose_pies(color)
        if self.board[piece] % color == KING and piece-where == 2:
            self.board[where] = self.board[piece]
            self.board[piece] = 0
            self.board[where+1] = self.board[piece-4]
            self.board[piece-4] = 0
        elif self.board[piece] % color == KING and where-piece == 2:
            self.board[where] = self.board[piece]
            self.board[piece] = 0
            self.board[where-1] = self.board[piece+3]
            self.board[piece+3] = 0
        else:
            self.board[where] = self.board[piece]
            self.board[piece] = 0
        if self.board[where] - color == PAWN and where // 8 in (0, 7):
            self.board[where] = self.choose_piece(color)
        try:
            self.pieces_moved[piece] = True
        except Exception:
            pass


    def chose_pies(self, color):
        piece = -1
        move = False
        to_move = -1
        while not move:
            piece = to_move
            while self.board[piece] // color != 1 or piece == -1:
                piece = self.event_listener("Jakou chces figurku?")
                if type(piece) is str:
                    x, y = piece
                    piece = (ord(x)-97) + (8 - int(y))*8
                # piece = int(input("Jakou chces figurku?"))
            move, to_move = self.chose_position(piece, color)
        return piece, to_move

    def chose_position(self, piece, color):
        moves = Moves(self.pieces_moved)
        positions = []
        possible_moves = []
        if self.board[piece] % color == ROCK:
            positions = moves.rock(self.board, piece)
        elif self.board[piece] % color == PAWN:
            positions = moves.pawn(self.board, piece)
        elif self.board[piece] % color == KING:
            positions = moves.king(self.board, piece, self.pieces_moved)
        elif self.board[piece] % color == QUEEN:
            positions = moves.queen(self.board, piece)
        elif self.board[piece] % color == KNIGHT:
            positions = moves.knight(self.board, piece)
        elif self.board[piece] % color == BISHOP:
            positions = moves.bishop(self.board, piece)
        for i in range(len(positions)):
            possible_moves.append(chr((positions[i] % 8) + 97) + str(8 - (positions[i] // 8)))
        position = self.event_listener(f"Kam chces tahnout? Mozne pozice: {possible_moves}")
        if type(position) is str:
            x, y = position
            position = (ord(x) - 97) + (8 - int(y)) * 8
        # position = int(input(f"Kam chces tahnout? Mozne pozice: {positions}"))
        if position in positions:
            return True, position
        return False, position

    def choose_piece(self, color):
        while True:
            # piece = int(input("Za jakou figurku chces vymenit pesaka?"))
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

