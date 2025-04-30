import pyxel


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 4
        self.active = True

    def update(self):
        self.y -= 4
        if self.y < 0:
            self.active = False

    def draw(self):
        if self.active:
            pyxel.rect(self.x, self.y, self.width, self.height, 10)

    def collides_with(self, obj):
        return (
            self.x < obj.x + obj.width and
            self.x + self.width > obj.x and
            self.y < obj.y + obj.height and
            self.y + self.height > obj.y
        )
