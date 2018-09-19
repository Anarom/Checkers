class Piece:
    def is_clear(self, pos, next_pos):
        koef_y = abs(next_pos[0] - pos[0])//(next_pos[0] - pos[0])
        koef_x = abs(next_pos[1] - pos[1])//(next_pos[1] - pos[1])
        if pos[0] + koef_y == next_pos[0] and pos[1] + koef_x == next_pos[1]:
            return True
        pos[0] += koef_y
        pos[1] += koef_x
        while(pos != next_pos):
            if isinstance(self.window.field[pos[0]][pos[1]], Piece):
                return False
            pos[0] += koef_y
            pos[1] += koef_x
        return True

    
    def eat_pieces(self, row, column):
        for move in self.moves:
            if row == move[0] and column == move[1]:
                for piece in move[2]:
                    self.window.field[piece[0]][piece[1]] = None               


    def find_moves(self, current_pos, targets, depth = 0, main_side = 0, main_front = 0, is_final = False):
        self.moves = []
        for front_move in range(-self.move_modifier,self.move_modifier + 1):
            row = current_pos[0] + front_move
            if row < 0 or front_move == 0 or row > 7:
                continue
            for side_move in range(-self.move_modifier,self.move_modifier + 1):
                column = current_pos[1] + side_move
                if column < 0 or side_move == 0 or column > 7 or abs(side_move) != abs(front_move):
                    continue
                next_cell = self.window.field[row][column]
                side_dir = abs(side_move)//side_move
                front_dir = abs(front_move)//front_move
                if self.is_clear([current_pos[0],current_pos[1]],[row,column]):
                    if next_cell == None:
                        if (depth == 0 or (self.is_king and side_dir == main_side and front_dir == main_front)) and not(not self.is_king and front_move != self.front):
                            if self.is_king and depth != 0:
                                self.moves.append([row,column,targets])
                            else:
                                self.moves.append([row,column,[]])
                    elif type(next_cell) != type(self) and  0 <= column + side_dir < 8 and 0 <= row + front_dir < 8:
                        if self.window.field[row + front_dir][column + side_dir] == None:
                            if [row,column] not in targets:
                                is_final = False
                                targets.append([row,column])
                                targets = self.find_moves([row + front_dir, column + side_dir], targets, depth + 1,side_dir, front_dir, True)
        if is_final:
            self.moves.append([current_pos[0],current_pos[1], targets])
        else:
            self.window.remove_focus_on_field(current_pos[0],current_pos[1])
        if depth != 0:
            return targets
        else:
            for move in self.moves:
                if move[2]:
                    return True
            return False


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
        if self.pos[0] == 3.5 * (self.front + 1) and not self.is_king:
            self.is_king = True
            self.move_modifier = 7
            self.window.canvas.delete(self.image)
            self.set_sprite(self.side+'_king')

    
    def remove_focus(self):
        self.window.canvas.delete(self.image)
        if self.is_king:
            self.set_sprite(f'{self.side}_king')
        else:
            self.set_sprite(f'{self.side}')
        self.focused = False

        
    def set_focus(self,can_hit):
        self.window.canvas.delete(self.image)
        if self.is_king:
            self.set_sprite(f'{self.side}_king_focus')
        else:
            self.set_sprite(f'{self.side}_focus')
        self.focused = True
        for move in self.moves:
            if can_hit:
                if move[2]:
                    self.window.set_focus_on_field(move[0],move[1])
            else:
                self.window.set_focus_on_field(move[0],move[1])


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
        self.is_king = False
        self.move_modifier = 1
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
        
