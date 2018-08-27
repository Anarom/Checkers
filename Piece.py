class Piece:

    def remove_focus(self, side):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{side}')
        self.focused = False
        
    def set_focus(self, side):
        self.window.canvas.delete(self.image)
        self.set_sprite(f'{side}_focus')
        self.focused = True
        

    def set_sprite(self, side):
         x,y = self.window.swap(self.pos[0], self.pos[1])
         sprite = self.window.sprites[side]
         self.image = self.window.canvas.create_image(x, y, image=sprite)

    def __init__(self, window, side, column, row):
        self.window = window
        self.side = side
        self.focused = False
        self.pos = [column, row]
        self.set_sprite(self.side)



def move(self, column, row):
        dx = column - self.pos[0]
        dy = row - self.pos[1]
        x, y = self.window.swap(dx, dy)
        canvas.move(self.image, x, y)
        field[self.pos[0]][self.pos[1]] = None
        self.pos[0] = column
        self.pos[1] = row
        field[self.pos[0]][self.pos[1]] = self
