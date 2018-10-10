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
                        if (depth == 0 or (
                                self.is_king and vertical_dir == main_side and horizontal_dir == main_front)) and not (
                                not self.is_king and vertical != self.front):
                            if self.is_king and depth != 0:
                                self.moves.append([row, column, targets.copy()])
                            else:
                                self.moves.append([row, column, []])
                    elif type(next_cell) != type(
                            self) and 0 <= column + vertical_dir < 8 and 0 <= row + horizontal_dir < 8:
                        if not self.window.field[row + horizontal_dir][column + vertical_dir]:
                            if [row, column] not in targets:
                                is_final = False
                                targets.append([row, column])
                                self.find_moves([row + horizontal_dir, column + vertical_dir], targets, depth + 1,
                                                vertical_dir, horizontal_dir, True)
                                targets.pop(-1)
        if is_final:
            self.moves.append([current_pos[0], current_pos[1], targets.copy()])
        else:
            self.window.remove_focus_on_field(current_pos[0], current_pos[1])
        if not depth == 0:
            return targets
        else:
            for move in self.moves:
                if move[2]:
                    return True
            return False

    def eat_pieces(self, row, column):
        eaten = []
        for move in self.moves:
            if row == move[0] and column == move[1]:
                for piece in move[2]:
                    if self.window.field[piece[0]][piece[1]].side == 'white':
                        if not self.window.field[piece[0]][piece[1]].is_king:
                            modifier = 0
                        else:
                            modifier = 1
                    else:
                        if not self.window.field[piece[0]][piece[1]].is_king:
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
        self.window.move_history.append([self.pos.copy(), [row,column], False])
        self.window.hit_history.append(self.eat_pieces(row, column))
        self.change_pos(row, column)
        if self.pos[0] == 3.5 * (self.front + 1) and not self.is_king:
            self.window.move_history[-1][2] = True
            self.set_king()

    def set_focus(self, can_hit):
        self.window.canvas.delete(self.image)
        if self.is_king:
            self.set_sprite(f'{self.side}_king_focus')
        else:
            self.set_sprite(f'{self.side}_focus')
        self.focused = True
        max_hits = 1
        for move in self.moves:
            if len(move[2]) > max_hits:
                max_hits = len(move[2])
        for move in self.moves:
            if can_hit:
                if len(move[2]) == max_hits:
                    self.window.set_focus_on_field(move[0], move[1])
            else:
                self.window.set_focus_on_field(move[0], move[1])

    def remove_focus(self):
        self.window.canvas.delete(self.image)
        if self.is_king:
            self.set_sprite(f'{self.side}_king')
        else:
            self.set_sprite(f'{self.side}')
        self.focused = False

    def set_sprite(self, side):
        y, x = self.window.get_screen_pos(self.pos[0], self.pos[1])
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


class WhitePiece(Piece):
    def __init__(self, window, row, column):
        super().__init__(window, 'white', row, column)


class BlackPiece(Piece):
    def __init__(self, window, row, column):
        super().__init__(window, 'black', row, column)
