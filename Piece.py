class Piece:

    def find_moves(self, current_pos, depth):
        if (current_pos[0] == 0 and self.side == 'white') or (current_pos[0] == 7 and self.side == 'black'):
            return
        moves = [-1, 1]
        if current_pos[1] == 0:
            moves = [1]
        elif current_pos[1] == 7:
            moves = [-1]
        for move in moves:
            row = current_pos[0] + self.head
            column = current_pos[1] + move
            cell = self.window.field[row][column]
            if cell == None:
                if depth == 0:
                    self.window.set_focus_on_field(row, column)
            elif type(cell) != type(self) and column + move < 8 and row + self.head < 8:
                if self.window.field[row + self.head][column + move] == None:
                    self.window.set_focus_on_field(row + self.head, column + move)
                    self.find_moves([row + self.head, column + move], depth + 1)
                             
    def remove_focus(self):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{self.side}')
        self.focused = False
        
    def set_focus(self):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{self.side}_focus')
        self.focused = True
        self.find_moves(self.pos, 0)
        
    def move(self, row, column):
        dy = row - self.pos[0]
        dx = column - self.pos[1]
        y = dy * self.window.cell_radius * 2
        x = dx * self.window.cell_radius * 2
        self.window.canvas.move(self.image, x, y)
        self.window.field[self.pos[0]][self.pos[1]] = None
        self.pos[0] = row
        self.pos[1] = column
        self.window.field[self.pos[0]][self.pos[1]] = self

    def set_sprite(self, side):
         y,x = self.window.get_screen_pos(self.pos[0], self.pos[1])
         sprite = self.window.sprites[side]
         self.image = self.window.canvas.create_image(x, y, image=sprite)

    def __init__(self, window, side, row, column):
        self.window = window
        self.head = None
        self.side = side
        self.focused = False
        self.pos = [row, column]
        self.set_sprite(self.side)

    def __del__(self):
        self.window.canvas.delete(self.image)
        print('removed', self.pos)


class WhitePiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'white', row, column)
        self.head = -1

class BlackPiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'black', row, column)
        self.head = 1
        
