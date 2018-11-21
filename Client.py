from Piece import Piece, get_screen_pos
from random import randint

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
        has_moves = self.get_moves()
        if isinstance(self, PlayerClient):
            self.click1 = self.window.root.bind('<Button-1>', self.callback)
            self.click2 = self.window.root.bind('<Button-3>', self.undo_turn)
        elif has_moves:
            self.process()
        return has_moves

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


class PlayerClient(Client):

    def callback(self, event):
        row, column = self.get_field_pos(event.y, event.x)
        piece = self.window.field[row][column]
        if piece:
            if type(piece) == int or piece.side == self.side:
                if isinstance(piece, Piece):
                    if not piece.focused:
                        self.reset_focus()
                        self.set_focus(piece)
                        self.focused = piece
                    else:
                        self.reset_focus()
                        self.focused = None
                else:
                    self.reset_focus()
                    self.focused.move(row, column)
                    self.focused = None
                    self.window.root.unbind(self.click1)
                    self.window.root.unbind(self.click2)
                    self.window.end_turn()
        
    def undo_turn(self, event):
        iter = 2
        if isinstance(self.window.client1, PlayerClient) or isinstance(self.window.client2, PlayerClient): 
            iter = 1
        for __ in range(iter):
            self.reset_focus()
            if not self.window.move_history:
                return 0
            move = self.window.move_history[-1]
            self.window.field[move.y1][move.x1].change_pos(move.y0,move.x0)
            if move.king:
                self.window.field[move.y0][move.x0].reset_king()
            for target in move.targets:
                if target[2] < 2:
                    self.window.field[target[0]][target[1]] = Piece(self.window, 'white',
                                                                    target[0], target[1])
                else:
                    self.window.field[target[0]][target[1]] = Piece(self.window, 'black',
                                                                    target[0], target[1])
                self.window.active_client.pieces.append(self.window.field[target[0]][target[1]])
                if target[2] % 2 == 1:
                    self.window.field[target[0]][target[1]].set_king()
            self.window.move_history.pop()
        if iter == 1:
            self.window.end_turn(True)

    def reset_focus(self):
        for piece in self.pieces:
            self.remove_focus(self.window.field[piece.pos[0]][piece.pos[1]])
        for row in range(len(self.window.field)):
            for column in range(len(self.window.field[row])):
                if not isinstance(self.window.field[row][column], Piece):
                    self.remove_focus_on_field(row, column)

    def remove_focus_on_field(self, row, column):
        if not isinstance(self.window.field[row][column], Piece):
            self.window.canvas.delete(self.window.field[row][column])
            self.window.field[row][column] = None

    def set_focus_on_field(self, row, column):
        if not isinstance(self.window.field[row][column], Piece):
            y, x = get_screen_pos(self.window.cell_radius, row, column)
            sprite = self.window.sprites['focus']
            self.window.field[row][column] = self.window.canvas.create_image(x, y, image=sprite)

    def get_field_pos(self, y, x):
        column = int(x // (self.window.cell_radius * 2))
        row = int(y // (self.window.cell_radius * 2))
        return row, column

    def set_focus(self, piece):
        self.window.canvas.delete(piece.image)
        if piece.is_king:
            piece.set_sprite(f'{self.side}_king_focus')
        else:
            piece.set_sprite(f'{self.side}_focus')
        piece.focused = True
        for move in piece.moves:
            self.set_focus_on_field(move.y1, move.x1)

    def remove_focus(self, piece):
        self.window.canvas.delete(piece.image)
        if piece.is_king:
            piece.set_sprite(f'{self.side}_king')
        else:
            piece.set_sprite(f'{self.side}')
        piece.focused = False


class AIClient(Client):

    def do_move(self, move):
        for piece in self.pieces:
            if piece.pos == [move.y0, move.x0]:
                break
        piece.move(move.y1, move.x1)
        self.window.end_turn()

    def process(self):
        self.moves = []
        for piece in self.pieces:
            for move in piece.moves:
                self.moves.append(move)
        number = randint(0,len(self.moves)-1)
        self.do_move(self.moves[number])
