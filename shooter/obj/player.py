import pyxel


class Player:
    def __init__(self, x, y):
        self.x = 76  # Adjusted for new resolution
        self.y = 200  # Adjusted for new resolution
        self.width = 8
        self.height = 8

    def move(self):
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn( pyxel.GAMEPAD1_BUTTON_DPAD_LEFT )) and self.x > 0:
            self.x -= 2
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn( pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT )) and self.x < pyxel.width - self.width:
            self.x += 2

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 9)

    def collides_with(self, obj):
        return (
            self.x < obj.x + obj.width and
            self.x + self.width > obj.x and
            self.y < obj.y + obj.height and
            self.y + self.height > obj.y
        )
