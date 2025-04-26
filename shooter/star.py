import pyxel
import random


class Star:
    def __init__(self):
        self.x = random.randint(0, pyxel.width - 1)
        self.y = random.randint(0, pyxel.height - 1)
        self.speed = random.randint(1, 3)  # Speed of the star
        self.color = random.choice([7, 10, 12])  # Random star color

    def update(self):
        self.y += self.speed
        # Reset position if the star goes off the screen
        if self.y >= pyxel.height:
            self.x = random.randint(0, pyxel.width - 1)
            self.y = 0

    def draw(self):
        pyxel.pset(self.x, self.y, self.color)  # Draw as a single pixel
