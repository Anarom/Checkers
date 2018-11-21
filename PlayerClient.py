from Piece import Piece, get_screen_pos
from Client import Client

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
        
    def undo_move(self, move):
        self.window.field[move[1][0]][move[1][1]].change_pos(move[0][0],move[0][1])
        if move[2]:
                self.window.field[move[0][0]][move[0][1]].reset_king()
        self.window.move_history.pop()
        
    def undo_hit(self, hits):
        for hit in hits:
            if hit[2] < 2:
                self.window.field[hit[0]][hit[1]] = WhitePiece(self, hit[0], hit[1])
            else:
                self.window.field[hit[0]][hit[1]] = BlackPiece(self, hit[0], hit[1])
            if hit[2] % 2 == 1:
                self.window.field[hit[0]][hit[1]].set_king()
        self.window.hit_history.pop()
        
    def undo_turn(self, event):
        if self.window.move_history:
            self.reset_focus()
            self.undo_move(self.window.move_history[-1])
            self.undo_hit(self.window.hit_history[-1])
            self.window.end_turn()

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
            self.set_focus_on_field(move[0], move[1])

    def remove_focus(self, piece):
        self.window.canvas.delete(piece.image)
        if piece.is_king:
            piece.set_sprite(f'{self.side}_king')
        else:
            piece.set_sprite(f'{self.side}')
        piece.focused = False
