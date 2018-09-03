

class Piece:
    def eat_pieces(self, row, column):
        for move in self.moves:
            if row == move[0] and column == move[1]:
                for piece in move[2]:
                    self.window.piece_count[self.window.field[piece[0]][piece[1]].side] -= 1
                    self.window.field[piece[0]][piece[1]] = None

                    
    def check_edge(self, current_pos):
        if current_pos[1] == 0:
            moves = [1]
        elif current_pos[1] == 7:
            moves = [-1]
        else:
            moves = [-1,1]
        return moves


    def find_moves(self, current_pos, targets, depth = 0, is_final = False):
        sides = self.check_edge(current_pos)
        for front_move in [-1,1]:
            row = current_pos[0] + front_move
            for side_move in sides:
                column = current_pos[1] + side_move
                if row < 0 or row > 7 or column < 0 or column > 7:
                    continue
                next_cell = self.window.field[row][column]
                if next_cell == None:
                    if depth == 0 and front_move == self.front:
                        self.window.set_focus_on_field(row, column)
                        self.moves.append([row,column,[]])
                elif type(next_cell) != type(self) and  0 <= column + side_move < 8 and 0 <= row + front_move < 8:
                    if self.window.field[row + front_move][column + side_move] == None:
                        is_final = False
                        targets.append([row,column])
                        self.window.set_focus_on_field(row + front_move, column + side_move)
                        targets = self.find_moves([row + front_move, column + side_move], targets, depth + 1, True)
        if is_final:
            self.moves.append([current_pos[0],current_pos[1], targets])
        else:
            self.window.remove_focus_on_field(current_pos[0],current_pos[1])
        return targets

    
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
        self.eat_pieces(row, column)
        self.window.canvas.move(self.image, x, y)
        self.window.field[self.pos[0]][self.pos[1]] = None
        self.pos[0] = row
        self.pos[1] = column
        self.window.field[self.pos[0]][self.pos[1]] = self
        if self.pos[0] == 3.5 * (self.front + 1) and not isinstance(self, King):
            print('king!')
#            window.[self.pos[0]][self.pos[1] = King(self.pos[0], self.pos[1], self.side)


    def set_sprite(self, side):
         y,x = self.window.get_screen_pos(self.pos[0], self.pos[1])
         sprite = self.window.sprites[side]
         self.image = self.window.canvas.create_image(x, y, image=sprite)


    def set_front(self, side):
        if side == 'white':
            self.front = -1
        else:
            self.front = 1


    def __init__(self, window, side, row, column):
        self.window = window
        self.moves = []
        self.side = side
        self.focused = False
        self.pos = [row, column]
        self.set_front(self.side)
        self.set_sprite(self.side)


    def __del__(self):
        self.window.canvas.delete(self.image)


class WhitePiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'white', row, column)

        
class BlackPiece(Piece):
    def __init__(self,window, row, column):
        super().__init__(window, 'black', row, column)
        
