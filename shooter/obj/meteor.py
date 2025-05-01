import pyxel
import random
import math


class Meteor:
    def __init__(self):
        self.x = random.randint(0, pyxel.width - 8)
        self.y = random.randint(-40, -5)  # Start above the screen
        self.width = 8
        self.height = 8
        self.speed = random.randint(1, 3)  # Random falling speed
        self.amplitude = 10  # Amplitude of the sine wave
        self.frequency = random.uniform(
            0.05, 0.1)  # Frequency of the sine wave
        self.base_x = self.x  # Base x position for sine wave movement
        self.time = 0  # Time counter for sine wave calculation
        self.active = True

    def update(self):
        self.y += self.speed
        self.time += 1
        # Update x position based on sine wave
        self.x = self.base_x + self.amplitude * \
            math.sin(self.frequency * self.time)
        # Reset position if it goes off the screen
        if self.y > pyxel.height:
            self.reset()

    def reset(self):
        self.x = random.randint(0, pyxel.width - 8)
        self.y = random.randint(-20, -5)
        self.speed = random.randint(1, 3)
        self.base_x = self.x
        self.time = 0

    def draw(self):
        # Draw as a gray rectangle
        pyxel.rect(self.x, self.y, self.width, self.height, 11)

    def collides_with(self, obj):
        return (
            self.x < obj.x + obj.width and
            self.x + self.width > obj.x and
            self.y < obj.y + obj.height and
            self.y + self.height > obj.y
        )
