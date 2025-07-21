from constants import (BLACK_ROCK, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_PAWN, BLACK_KNIGHT,
                       WHITE_ROCK, WHITE_KING, WHITE_KNIGHT, WHITE_PAWN, WHITE_QUEEN, WHITE_BISHOP,
                       BLACK, WHITE, UNICODE_CODING, WINDOWS_UNICODE_CODING, Moves, PAWN, QUEEN,
                       BISHOP, KNIGHT, ROCK, KING, SWITCHABLE)
import pygame

class Game:
    def __init__(self, mode):
        self.mode = mode
        self.drawer = Drawer()

    def start(self):
        chess = Chess()
        chess.create_board()
        print(chess.__str__())
        colors = [None, WHITE, BLACK]
        color = 1
        while True:
            self.drawer.draw(chess.board)
            if colors[color] == BLACK:
                print("HRAJE CERNY")
            else:
                print("HRAJE BILY")
            chess.move(colors[color])
            print(chess.__str__())
            color *= -1

class Drawer:
    def __init__(self):
        self.screen = pygame.display.set_mode((100 * 8, 100 * 8))
        pygame.font.init()
        self.font = pygame.font.SysFont("dejavu sans", 80)
        pygame.init()

    def draw(self, board):
        self.screen.fill("black")
        for y in range(8):
            for x in range(8):
                pos = y * 8 + x
                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.screen, (118, 150, 86), (x * 100, y * 100, 100, 100))
                else:
                    pygame.draw.rect(self.screen, (238, 238, 210), (x * 100, y * 100, 100, 100))
                self.screen.blit(self.font.render(WINDOWS_UNICODE_CODING[board[pos]], True, (0, 0, 0)), (x * 100 + 20, y * 100))
        pygame.display.flip()





class Chess:
    def __init__(self):
        self.board = [0 for x in range(64)]

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
        self.board[where] = self.board[piece]
        self.board[piece] = 0
        if self.board[where] - color == PAWN and where // 8 in (0, 7):
            self.board[where] = self.choose_piece(color)


    def chose_pies(self, color):
        piece = -1
        move = False
        to_move = -1
        while not move:
            piece = to_move
            while self.board[piece] // color != 1 or piece == -1:
                x, y = input("Jakou chces figurku?")
                piece = (ord(x)-97) + int(y)*8
                piece = int(input("Jakou chces figurku?"))
                piece = self.event_listener()
            move, to_move = self.chose_position(piece, color)
        return piece, to_move

    def chose_position(self, piece, color):
        moves = Moves(color)
        positions = []
        positionsSachy = []
        if self.board[piece] % color == ROCK:
            positions = moves.rock(self.board, piece)
        elif self.board[piece] % color == PAWN:
            positions = moves.pawn(self.board, piece)
        elif self.board[piece] % color == KING:
            positions = moves.king(self.board, piece)
        elif self.board[piece] % color == QUEEN:
            positions = moves.queen(self.board, piece)
        elif self.board[piece] % color == KNIGHT:
            positions = moves.knight(self.board, piece)
        elif self.board[piece] % color == BISHOP:
            positions = moves.bishop(self.board, piece)
        for i in range(len(positions)):
            positionsSachy.append(chr((positions[i] % 8) + 97) + str(positions[i] // 8))
        x, y = input(f"Kam chces tahnout? Mozne pozice: {positionsSachy}")
        position = (ord(x)-97) + int(y)*8
        position = int(input(f"Kam chces tahnout? Mozne pozice: {positions}"))
        position = self.event_listener()
        if position in positions:
            return True, position
        return False, position

    def choose_piece(self, color):
        while True:
            piece = int(input("Za jakou figurku chces vymenit pesaka?"))
            piece = self.event_listener()
            if piece not in SWITCHABLE: continue
            return color + piece

    def event_listener(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    position = position[0] // 100 + position[1] // 100 * 8
                    return position

