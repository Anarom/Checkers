class Piece:

    def find_moves(self):
        moves = [-1, 1]
        if self.pos[0] == 0:
            moves = [1]
        elif self.pos[0] == 7:
            moves = [-1]
        for move in moves:
            if self.window.field[self.pos[1] + self.head][self.pos[0] + move] == None:
                self.window.set_focus_on_field(self.pos[0] + move, self.pos[1] + self.head)

    def remove_focus(self):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{self.side}')
        self.focused = False
        
    def set_focus(self):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{self.side}_focus')
        self.focused = True
        self.find_moves()

    def move(self, column, row):
        dx = column - self.pos[0]
        dy = row - self.pos[1]
        x, y = self.window.cell_radius * 2 * dx,self.window.cell_radius * 2 * dy
        self.window.canvas.move(self.image, x, y)
        self.window.field[self.pos[1]][self.pos[0]] = None
        self.pos[0] = column
        self.pos[1] = row
        self.window.field[self.pos[1]][self.pos[0]] = self

    def set_sprite(self, side):
         x,y = self.window.swap(self.pos[0], self.pos[1])
         sprite = self.window.sprites[side]
         self.image = self.window.canvas.create_image(x, y, image=sprite)

    def __init__(self, window, side, column, row):
        self.window = window
        self.head = None
        self.side = side
        self.focused = False
        self.pos = [column, row]
        self.set_sprite(self.side)

    def __del__(self):
        self.window.canvas.delete(self.image)
        print('removed', self.pos)


class WhitePiece(Piece):
    def __init__(self,window, column, row):
        super().__init__(window, 'white', column, row)
        self.head = -1

class BlackPiece(Piece):
    def __init__(self,window, column, row):
        super().__init__(window, 'black', column, row)
        self.head = 1
        
