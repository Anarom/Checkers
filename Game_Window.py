import tkinter
from PIL import ImageTk, Image
from os import getcwd
from Client import PlayerClient, AIClient


class GameWindow:

    def end_turn(self, undo = False):
        self.active_client = self.client2 if self.active_client == self.client1 else self.client1
        if self.move_history and not undo:
            move = self.move_history[-1]
            for target in move.targets:
                for piece in self.active_client.pieces:
                    if target[:-1] == piece.pos:
                        self.active_client.pieces.remove(piece)
        if not self.active_client.get_turn():
            self.end_game()

    def end_game(self):
        if self.active_client.side == 'white':
            print('black won')
        else:
            print('white won')
        self.root.destroy()

    def get_field(self, color1, color2):
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

    def get_sprites(self):
        sprites = {}
        for name in ['white', 'black', 'white_focus', 'black_focus', 'focus',
                     'white_king', 'black_king', 'white_king_focus', 'black_king_focus']:
            image = Image.open(f'{getcwd()}\Sprites\\{name}.png')
            image = image.resize((self.screen_size // 8, self.screen_size // 8))
            image = ImageTk.PhotoImage(image)
            sprites[name] = image
        return sprites

    def get_root(self):
        root = tkinter.Tk()
        root.title('Checkers')
        root.geometry(f'{self.screen_size}x{self.screen_size}+250+30')
        root.resizable(False, False)
        return root

    def set_game(self):
        self.get_field('white', 'gray')
        self.client1 = PlayerClient(self, 'white')
        self.client2 = PlayerClient(self, 'black')       
        self.active_client = self.client1
        self.active_client.get_turn()

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.cell_radius = self.screen_size / 16
        self.move_history = []
        self.hit_history = []
        self.field = [[None for _ in range(8)] for __ in range(8)]
        self.root = self.get_root()
        self.sprites = self.get_sprites()
        self.canvas = tkinter.Canvas(self.root, bg='black')
        self.canvas.place(x=0, y=0, width=self.screen_size, height=self.screen_size)
        self.set_game()
        self.root.mainloop()
        
game = GameWindow(640)
