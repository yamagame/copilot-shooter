import pyxel


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

    def move(self):
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < pyxel.width - self.width:
            self.x += 2

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 9)
