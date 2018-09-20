import tkinter
from Piece import Piece, WhitePiece, BlackPiece
from PIL import ImageTk, Image
from os import getcwd


class GameWindow:
    def callback(self, event):
        row, column = self.get_field_pos(event.y, event.x)
        cell = self.field[row][column]
        if cell:
            if isinstance(cell, Piece):
                if cell.side == self.turn:
                    if not cell.focused:
                        self.reset_focus()
                        cell.set_focus(self.can_hit)
                        self.focused = cell
                    else:
                        self.reset_focus()
                        self.focused = None
            else:
                self.reset_focus()
                self.focused.move(row, column)
                self.end_turn()

    def get_moves(self):
        has_moves = False
        for row in self.field:
            for cell in row:
                if isinstance(cell, Piece) and cell.side == self.turn:
                    can_hit = cell.find_moves(cell.pos, [])
                    if can_hit and not self.can_hit:
                        self.can_hit = True
                    if cell.moves:
                        has_moves = True
        return has_moves

    def end_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
        self.can_hit = False
        if not self.get_moves():
            self.end_game()

    def end_game(self):
        if self.turn == 'white':
            print('black won')
        else:
            print('white won')
            self.root.destroy()

    def reset_focus(self):
        for row in range(len(self.field)):
            for column in range(len(self.field[row])):
                if isinstance(self.field[row][column], Piece):
                    self.field[row][column].remove_focus()
                else:
                    self.remove_focus_on_field(row, column)

    def remove_focus_on_field(self, row, column):
        if not isinstance(self.field[row][column], Piece):
            self.canvas.delete(self.field[row][column])
            self.field[row][column] = None

    def set_focus_on_field(self, row, column):
        if not isinstance(self.field[row][column], Piece):
            y, x = self.get_screen_pos(row, column)
            sprite = self.sprites['focus']
            self.field[row][column] = self.canvas.create_image(x, y, image=sprite)

    def get_screen_pos(self, row, column):
        x = (2 * column + 1) * self.cell_radius
        y = (2 * row + 1) * self.cell_radius
        return y, x

    def get_field_pos(self, y, x):
        column = int(x // (self.cell_radius * 2))
        row = int(y // (self.cell_radius * 2))
        return row, column

    def draw_field(self, color1, color2):
        colors = {color1: color2, color2: color1}
        color = color1
        y = 0
        for row in range(8):
            x = 0
            for column in range(8):
                self.canvas.create_rectangle(x, y, x + self.screen_size // 8, y + self.screen_size // 8, fill=color,
                                             outline=color)
                color = colors[color]
                x = (column + 1) * self.screen_size / 8
            color = colors[color]
            y += self.screen_size / 8

    def setup_pieces(self, side):
        offset = {0: 1, 1: 0}
        if side == 'black':
            start = offset[0]
            row = 0
        else:
            start = 0
            row = 5
        for row in range(row, row + 3):
            column = start
            for column in range(column, 8, 2):
                if side == 'white':
                    piece = WhitePiece(self, row, column)
                else:
                    piece = BlackPiece(self, row, column)
                self.field[row][column] = piece
            start = offset[start]

    def get_sprites(self):
        for name in ['white', 'black', 'white_focus', 'black_focus', 'focus',
                     'white_king', 'black_king', 'white_king_focus', 'black_king_focus']:
            image = Image.open(f'{getcwd()}\Sprites\\{name}.png')
            image = image.resize((self.screen_size // 8, self.screen_size // 8))
            image = ImageTk.PhotoImage(image)
            self.sprites[name] = image

    def root_setup(self):
        self.root = tkinter.Tk()
        self.root.geometry(f'{self.screen_size}x{self.screen_size}+250+30')
        self.root.resizable(False, False)
        self.root.bind('<Button-1>', self.callback)
        self.root.bind('<Return>', self.callback)
        self.root.title('Checkers')

    def set_game(self):
        self.root_setup()
        self.canvas = tkinter.Canvas(self.root, bg='black')
        self.canvas.place(x=0, y=0, width=self.screen_size, height=self.screen_size)
        self.get_sprites()
        self.draw_field('white', 'gray')
        self.setup_pieces('white')
        self.setup_pieces('black')
        self.get_moves()

    def __init__(self, screen_size):
        self.root = None
        self.canvas = None
        self.focused = None
        self.can_hit = False
        self.sprites = {}
        self.turn = 'white'
        self.screen_size = screen_size
        self.cell_radius = self.screen_size / 16
        self.field = [[None, None, None, None, None, None, None, None] for _ in range(8)]
        self.set_game()


game_window = GameWindow(640)
game_window.root.mainloop()
