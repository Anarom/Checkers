class Piece:

    def check_edge(self, current_pos):
        if current_pos[1] == 0:
            moves = [1]
        elif current_pos[1] == 7:
            moves = [-1]
        else:
            moves = [-1,1]
        return moves

    def find_moves(self, current_pos, depth):
        moves = self.check_edge(current_pos)
        for head in [-1,1]:
            row = current_pos[0] + head
            for move in moves:
                column = current_pos[1] + move
                if row < 0 or row > 7 or column < 0 or column > 7:
                    continue
                cell = self.window.field[row][column]
                if cell == None:
                    if depth == 0 and head == self.head:
                        self.window.set_focus_on_field(row, column)
                elif type(cell) != type(self) and column + move < 8 and row + head < 8:
                    if self.window.field[row + head][column + move] == None:
                        self.window.set_focus_on_field(row + head, column + move)
                        self.find_moves([row + head, column + move], depth + 1)
                             
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

    def __init__(self, window, side, head, row, column):
        self.window = window
        self.head = head
        self.side = side
        self.focused = False
        self.pos = [row, column]
        self.set_sprite(self.side)

    def __del__(self):
        self.window.canvas.delete(self.image)
        print('removed', self.pos)


class WhitePiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'white', -1, row, column)
        
class BlackPiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'black', 1, row, column)
        
