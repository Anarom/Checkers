import tkinter
from Piece import Piece, WhitePiece, BlackPiece
from PIL import ImageTk, Image
from os import getcwd

     
class GameWindow:


    def side_has_moves(self,side):
        has_moves = False
        for row in self.field:
            for column in row:
                if isinstance(column, Piece) and column.side == self.turn:
                    column.find_moves(column.pos, [])
                    if column.moves:
                        has_moves =  True
        self.reset_focus()
        return has_moves
                        
    def callback(self, event):
        row, column = self.get_field_pos(event.y, event.x)
        piece = self.field[row][column]
        if piece:
            if isinstance(piece, Piece):
                if piece.side == self.turn:
                    if piece.focused == False:
                        self.reset_focus()
                        piece.set_focus()
                        self.focused = piece
                    else:
                        self.reset_focus()
                        self.focused = None
            else:
                self.reset_focus()
                self.focused.move(row, column)
                self.end_turn()

        
    def end_turn(self):
        for key in self.piece_count.keys():
            if self.piece_count[key] == 0:
                self.end_game(key)
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
        if not self.side_has_moves(self.turn):
            self.end_game(self.turn)


    def end_game(self,loser_side):
        if loser_side == 'white':
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
            y,x = self.get_screen_pos(row, column)
            sprite = self.sprites['focus']
            self.field[row][column] = self.canvas.create_image(x, y, image=sprite)


    def get_screen_pos(self, row, column):
        x = (2 * column + 1) *  self.cell_radius
        y = (2 * row + 1) * self.cell_radius
        return y, x

    
    def get_field_pos(self, y, x):
        column = int(x // (self.cell_radius * 2))
        row = int(y // (self.cell_radius * 2))
        return  row, column

    
    def draw_field(self, color1, color2):
        colors = {color1: color2, color2: color1}
        color = color1
        y = 0
        for row in range(8):
            x = 0
            for column in range(8):
                self.canvas.create_rectangle(x, y, x + self.screen_size // 8, y + self.screen_size // 8, fill=color, outline = color)
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
            for column in range (column, 8, 2):
                if side == 'white':
                    piece = WhitePiece(self, row, column)
                else:
                    piece = BlackPiece(self, row, column)
                self.piece_count[side] += 1
                self.field[row][column] = piece
            start = offset[start]

            
    def get_sprites(self):
        for name in ['white', 'black', 'white_focus', 'black_focus', 'focus']:
            image = Image.open(f'{getcwd()}\Sprites\\{name}.png')
            image = image.resize((self.screen_size // 8, self.screen_size // 8))
            image = ImageTk.PhotoImage(image)
            self.sprites[name] = image
            
    
    def root_setup(self):
        self.root = tkinter.Tk()
        self.root.geometry(f'{self.screen_size}x{self.screen_size}+250+30')
        self.root.bind('<Button-1>', self.callback)
        self.root.title('Checkers')


    def set_game(self):
        self.root_setup()
        self.canvas = tkinter.Canvas(self.root, bg='black')
        self.canvas.place(x=0, y=0, width=self.screen_size, height=self.screen_size)
        self.get_sprites()
        self.draw_field('white', 'brown')
        self.setup_pieces('white')
        self.setup_pieces('black')

        
    def __init__(self, screen_size):
        self.sprites = {}
        self.turn = 'white'
        self.piece_count = {'white': 0, 'black': 0}
        self.focused = None
        self.screen_size = screen_size
        self.cell_radius = self.screen_size / 16
        self.field = [[None,None,None,None,None,None,None,None] for _ in range(8)]
        self.set_game()


window = GameWindow(640)
window.root.mainloop()
