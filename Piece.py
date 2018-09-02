class Piece:

    def check_edge(self, current_pos):
        if current_pos[1] == 0:
            moves = [1]
        elif current_pos[1] == 7:
            moves = [-1]
        else:
            moves = [-1,1]
        return moves

    def find_moves(self, current_pos, moves, depth = 0, is_final = False):
        sides = self.check_edge(current_pos)
        for front in [-1,1]:
            row = current_pos[0] + front
            for side in sides:
                column = current_pos[1] + side
                if row < 0 or row > 7 or column < 0 or column > 7:
                    continue
                cell = self.window.field[row][column]
                if cell == None:
                    if depth == 0 and front == self.front:
                        self.window.set_focus_on_field(row, column)
                        self.moves.append([row,column,[]])
                elif type(cell) != type(self) and  0 <= column + side < 8 and 0 <= row + front < 8:
                    if self.window.field[row + front][column + side] == None:
                        is_final = False
                        moves.append([row,column])
                        self.window.set_focus_on_field(row + front, column + side)
                        moves = self.find_moves([row + front, column + side], moves, depth + 1, True)
        if is_final:
            self.moves.append([current_pos[0],current_pos[1], moves])
        else:
            self.window.remove_focus_on_field(current_pos[0],current_pos[1])
        return moves
    
    def remove_focus(self):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{self.side}')
        self.focused = False
        
    def set_focus(self):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{self.side}_focus')
        self.focused = True
        self.moves = []
        self.find_moves(self.pos,[])
        
    def move(self, row, column):
        dy = row - self.pos[0]
        dx = column - self.pos[1]
        y = dy * self.window.cell_radius * 2
        x = dx * self.window.cell_radius * 2
        for move in self.moves:
            if row == move[0] and column == move[1]:
                for piece in move[2]:
                    self.window.field[piece[0]][piece[1]] = None
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
        self.moves = []
        self.side = side
        if self.side == 'white':
            self.front = -1
        else:
            self.front = 1
        self.focused = False
        self.pos = [row, column]
        self.set_sprite(self.side)

    def __del__(self):
        self.window.canvas.delete(self.image)


class WhitePiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'white', row, column)
        
class BlackPiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'black', row, column)
        
