import pyxel
import random


class Fragment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)  # Random horizontal speed
        self.vy = random.uniform(-2, 2)  # Random vertical speed
        self.lifetime = random.randint(20, 40)  # Lifetime in frames
        self.color = random.choice([8, 9, 10, 11])  # Random color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self):
        if self.lifetime > 0:
            pyxel.pset(self.x, self.y, self.color)  # Draw as a single pixel
