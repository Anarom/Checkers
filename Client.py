from Piece import Piece, get_screen_pos


class Client:
    
    def __init__(self, window, side):
        self.side = side
        self.window = window
        self.pieces = self.set_pieces()

    def set_pieces(self):
        pieces = []
        offset = {0: 1, 1: 0}
        if self.side == 'black':
            start = offset[0]
            row = 0
        else:
            start = offset[1]
            row = 5
        for row in range(row, row + 3):
            column = start
            for column in range(column, 8, 2):
                piece = Piece(self.window, self.side, row, column)
                pieces.append(piece)
                self.window.field[row][column] = piece
            start = offset[start]
        return pieces
        
    def get_turn(self):
        if isinstance(self, PlayerClient):
            self.click1 = self.window.root.bind('<Button-1>', self.callback)
            self.click2 = self.window.root.bind('<Button-3>', self.undo_turn)
        return self.get_moves()

    def get_moves(self):
        has_moves = False
        can_hit = False
        for piece in self.pieces:
            can_hit = piece.find_moves(piece.pos, []) or can_hit
            if piece.moves:
                has_moves = True
            for piece in self.pieces:
                piece.validate_moves(can_hit) 
        return has_moves
