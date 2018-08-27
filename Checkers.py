import tkinter
from PIL import ImageTk, Image
from os import getcwd

def callback(event):
    column, row = deswap(event.x, event.y)
    piece = field[row][column]  
    if piece:
        if piece.focused == False:
            for row in field:
                for column in row:
                    if column:
                        column.remove_focus()
            piece.set_focus()
        else:
            piece.remove_focus()
        
def swap(column, row):
    return (2 * column + 1) * cell_radius, (2 * row + 1) * cell_radius

def deswap(x, y):
    return  int(x // (cell_radius * 2)), int(y // (cell_radius * 2))

def draw_field(color1, color2):
    colors = {color1: color2, color2: color1}
    color = color1
    y = 0
    for row in range(8):
        x = 0
        for column in range(8):
            canvas.create_rectangle(x, y, x + screen_size // 8, y + screen_size // 8, fill=color, outline = color)
            color = colors[color]
            x = (column + 1) * screen_size / 8
        color = colors[color]
        y += screen_size / 8

def setup_pieces(side):
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
            piece = Piece(side, column, row)
            field[row][column] = piece
        start = offset[start]

        
class Piece:

    def remove_focus(self):
        canvas.delete(self.image)
        self.set_sprite(f'{self.side}')
        self.focused = False
        
    def set_focus(self):
        canvas.delete(self.image)
        self.set_sprite(f'{self.side}_focus')
        self.focused = True
        
    def move(self, column, row):
        dx = column - self.pos[0]
        dy = row - self.pos[1]
        x, y = swap(dx, dy)
        canvas.move(self.image, x, y)
        field[self.pos[0]][self.pos[1]] = None
        self.pos[0] = column
        self.pos[1] = row
        field[self.pos[0]][self.pos[1]] = self

    def set_sprite(self, side):
         x,y = swap(self.pos[0], self.pos[1])
         self.sprite = sprites[side]
         self.image = canvas.create_image(x, y, image=self.sprite)

    def __init__(self, side, column, row):
        self.side = side
        self.focused = False
        self.pos = [column, row]
        self.set_sprite(self.side)

screen_size = 600
cell_radius = screen_size / 16
field = [[None,None,None,None,None,None,None,None] for elem in range(8)]
root = tkinter.Tk()
root.geometry(f'{screen_size}x{screen_size}+650+30')
root.bind('<Button-1>', callback)
root.title('Checkers')
canvas = tkinter.Canvas(root, bg='black')
canvas.place(x=0, y=0, width=screen_size, height=screen_size)
sprites = {'white': ImageTk.PhotoImage(Image.open(f'{getcwd()}\Sprites\\white piece.png').resize((screen_size // 8, screen_size // 8))),
           'black': ImageTk.PhotoImage(Image.open(f'{getcwd()}\Sprites\\black piece.png').resize((screen_size // 8, screen_size // 8))),
           'black_focus': ImageTk.PhotoImage(Image.open(f'{getcwd()}\Sprites\\black_focus piece.png').resize((screen_size // 8, screen_size // 8))),
           'white_focus': ImageTk.PhotoImage(Image.open(f'{getcwd()}\Sprites\\white_focus piece.png').resize((screen_size // 8, screen_size // 8)))}                                   
draw_field('white', 'brown')
setup_pieces('black')
setup_pieces('white')
root.mainloop()
