from constants import Moves

def computer_move(self, board, color):
    moves = Moves(self.pieces_moved)
    positions = moves.all_moves(board, color)



def position_evaluation(self, board):
    for i in range(len(board)):
