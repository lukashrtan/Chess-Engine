from board import Board
from drawer import Drawer

draw_mode = input("Jak chces vykreslovat sachovnici? Metod: konzole, Lukas: aplikace")
drawer = Drawer(draw_mode)

board = Board.create_board()

self.moves = Moves(pieces_moved)
self.board = chess.board
chess.create_board()
color = WHITE

while True:
    self.drawer.draw(self.board)
    if POSSIBLE_COLORS[color] == BLACK:
        print("HRAJE CERNY")
    else:
        print("HRAJE BILY")
    self.get_move(POSSIBLE_COLORS[color])
    color = BLACK if color == WHITE else WHITE
    self.is_check_mate()

def get_move(self, color: int):
    return self.chose_pies(color)

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
                piece = (ord(x) - 97) + (8 - int(y)) * 8
        move, to_move = self.chose_position(piece, color)
    if self.board[to_move] % UNCOLOR == PAWN and to_move // 8 in (0, 7):
        self.choose_piece(color)
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


game.start()
