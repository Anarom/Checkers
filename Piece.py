def get_screen_pos(cell_radius, row, column):
        x = (2 * column + 1) * cell_radius
        y = (2 * row + 1) * cell_radius
        return y, x
    

class Move():
    def __init__(self,y0,x0,y1,x1,targets,piece):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.king = False
        self.targets = targets

        
class Piece:
    def line_is_clear(self, pos, next_pos):
        dy = abs(next_pos[0] - pos[0]) // (next_pos[0] - pos[0])
        dx = abs(next_pos[1] - pos[1]) // (next_pos[1] - pos[1])
        if pos[0] + dy == next_pos[0] and pos[1] + dx == next_pos[1]:
            return True
        pos[0] += dy
        pos[1] += dx
        while pos != next_pos:
            if isinstance(self.window.field[pos[0]][pos[1]], Piece):
                return False
            pos[0] += dy
            pos[1] += dx
        return True

    def find_moves(self, current_pos, targets, depth=0, main_side=0, main_front=0, is_final=False):
        if depth == 0:
            self.moves = []
        for vertical in range(-self.move_modifier, self.move_modifier + 1):
            row = current_pos[0] + vertical
            if row < 0 or vertical == 0 or row > 7:
                continue
            for horizontal in range(-self.move_modifier, self.move_modifier + 1):
                column = current_pos[1] + horizontal
                if column < 0 or horizontal == 0 or column > 7 or abs(horizontal) != abs(vertical):
                    continue
                if depth == 0:
                    targets = []
                next_cell = self.window.field[row][column]
                vertical_dir = abs(horizontal) // horizontal
                horizontal_dir = abs(vertical) // vertical
                if self.line_is_clear([current_pos[0], current_pos[1]], [row, column]):
                    if not next_cell:
                        if (depth == 0 or (self.is_king and vertical_dir == main_side and horizontal_dir == main_front)) and not (not self.is_king and vertical != self.front):
                            if self.is_king and depth != 0:
                                move = Move(self.pos[0],self.pos[1], row, column, targets.copy(), self)
                            else:
                                move = Move(self.pos[0],self.pos[1], row, column, [], self)
                            self.moves.append(move)
                    elif next_cell.side != self.side and 0 <= column + vertical_dir < 8 and 0 <= row + horizontal_dir < 8:
                        if not self.window.field[row + horizontal_dir][column + vertical_dir]:
                            if [row, column] not in targets:
                                is_final = False
                                targets.append([row, column])
                                self.find_moves([row + horizontal_dir, column + vertical_dir], targets, depth + 1,
                                                vertical_dir, horizontal_dir, True)
                                targets.pop(-1)
        if is_final:
            move = Move(self.pos[0],self.pos[1], current_pos[0], current_pos[1], targets.copy(), self)
            self.moves.append(move)
        if not depth == 0:
            return targets
        else:
            for move in self.moves:
                if move.targets:
                    return True
            return False

    def eat_targets(self, move):
        eaten = []
        for piece in move.targets:
            target = self.window.field[piece[0]][piece[1]]
            if target.side == 'white':
                if not target.is_king:
                    modifier = 0
                else:
                    modifier = 1
            else:
                if not target.is_king:
                    modifier = 2
                else:
                    modifier = 3
            eaten.append([piece[0],piece[1],modifier])
            self.window.field[piece[0]][piece[1]] = None
        return eaten
    
    def change_pos(self, row , column):
        dy = row - self.pos[0]
        dx = column - self.pos[1]
        y = dy * self.window.cell_radius * 2
        x = dx * self.window.cell_radius * 2
        self.window.canvas.move(self.image, x, y)
        self.window.field[self.pos[0]][self.pos[1]] = None
        self.pos[0] = row
        self.pos[1] = column
        self.window.field[self.pos[0]][self.pos[1]] = self
                                                      
    def move(self, row, column):
        for move in self.moves:
            if move.y1 == row and move.x1 == column:
                break
        move.targets = self.eat_targets(move)
        self.window.move_history.append(move)
        self.change_pos(move.y1, move.x1)
        if self.pos[0] == 3.5 * (self.front + 1) and not self.is_king:
            self.window.move_history[-1].king = True
            self.set_king()

    def validate_moves(self, can_hit):
        max_hits = 1
        for move in self.moves:
            if len(move.targets) > max_hits:
                max_hits = len(move.targets)
            for move in self.moves.copy():
                if can_hit:
                    if len(move.targets) < max_hits:
                        self.moves.remove(move)
                        continue

    def set_sprite(self, side):
        y, x = get_screen_pos(self.window.cell_radius,self.pos[0], self.pos[1])
        sprite = self.window.sprites[side]
        self.image = self.window.canvas.create_image(x, y, image=sprite)

    def set_king(self):
        self.is_king = True
        self.move_modifier = 7
        self.window.canvas.delete(self.image)
        self.set_sprite(self.side + '_king')

    def reset_king(self):
        self.is_king = False
        self.move_modifier = 1
        self.window.canvas.delete(self.image)
        self.set_sprite(self.side)        

    def __init__(self, window, side, row, column):
        self.front = None
        self.image = None
        self.is_king = False
        self.focused = False
        self.moves = []
        self.move_modifier = 1
        self.window = window
        self.side = side
        if self.side == 'white':
            self.front = -1
        else:
            self.front = 1
        self.pos = [row, column]
        self.set_sprite(self.side)

    def __del__(self):
        try:
            self.window.canvas.delete(self.image)
        except:
            pass
