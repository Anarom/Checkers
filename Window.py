import tkinter
from Piece import Piece
from PIL import ImageTk, Image
from os import getcwd

     
class MainWindow:

    def set_focus_on_field(self, column, row):
        x,y = self.swap(column, row)
        sprite = self.sprites['focus']
        self.focus = self.canvas.create_image(x, y, image=sprite)
        
    def remove_focus_on_field(self, column, row):
        self.canvas.delete(self.focus)
        self.focus = None

    def reset_focus(self):
        for row in self.field:
            for column in row:
                if column:
                    column.remove_focus(column.side)
                else:
                    self.remove_focus_on_field(column, row)

    def swap(self, column, row):
        return (2 * column + 1) * self.cell_radius, (2 * row + 1) * self.cell_radius
    
    def deswap(self, x, y):
        return  int(x // (self.cell_radius * 2)), int(y // (self.cell_radius * 2))
    
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
                piece = Piece(self, side, column, row)
                self.field[row][column] = piece
            start = offset[start]
            
    def callback(self, event):
        column, row = self.deswap(event.x, event.y)
        piece = self.field[row][column]  
        if piece:
            if piece.focused == False:
                self.reset_focus()
                piece.set_focus(piece.side)
            else:
                piece.remove_focus(piece.side)
        else:
            #self.reset_focus()
            self.set_focus_on_field(column, row)

    def get_sprites(self):
        for name in ['white', 'black', 'white_focus', 'black_focus', 'focus']:
            image = Image.open(f'{getcwd()}\Sprites\\{name}.png')
            image = image.resize((self.screen_size // 8, self.screen_size // 8))
            image = ImageTk.PhotoImage(image)
            self.sprites[name] = image
            
    
    def root_setup(self):
        self.root = tkinter.Tk()
        self.root.geometry(f'{self.screen_size}x{self.screen_size}+650+30')
        self.root.bind('<Button-1>', self.callback)
        self.root.title('Checkers')
        
    def __init__(self, screen_size):
        self.sprites = {}
        self.focus = None
        self.screen_size = screen_size
        self.cell_radius = self.screen_size / 16
        self.field = [[None,None,None,None,None,None,None,None] for elem in range(8)]
        self.root_setup()
        self.canvas = tkinter.Canvas(self.root, bg='black')
        self.canvas.place(x=0, y=0, width=self.screen_size, height=self.screen_size)
        self.get_sprites()


window = MainWindow(640)
window.draw_field('white', 'brown')
window.setup_pieces('white')
window.setup_pieces('black')
window.root.mainloop()
