import pyxel


class EnemyBullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 4
        self.active = True

        # Calculate direction vector to target
        dx = target_x - x
        dy = target_y - y
        magnitude = (dx**2 + dy**2) ** 0.5
        self.vx = (dx / magnitude) * 2  # Speed in x direction
        self.vy = (dy / magnitude) * 2  # Speed in y direction

    def update(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy
            # Deactivate if out of bounds
            if self.x < 0 or self.x > pyxel.width or self.y < 0 or self.y > pyxel.height:
                self.active = False

    def draw(self):
        if self.active:
            pyxel.rect(self.x, self.y, self.width, self.height, 8)

    def collides_with(self, obj):
        return (
            self.x < obj.x + obj.width and
            self.x + self.width > obj.x and
            self.y < obj.y + obj.height and
            self.y + self.height > obj.y
        )
