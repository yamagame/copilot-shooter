import pyxel
import random

class PowerUp:
    def __init__(self):
        self.x = random.randint(0, pyxel.width - 8)
        self.y = -10  # Start above the screen
        self.width = 8
        self.height = 8
        self.speed = 0.5  # Slow falling speed
        self.amplitude = 20  # Amplitude for floating effect
        self.frequency = 1.0  # Frequency for floating effect
        self.base_x = self.x
        self.time = 0
        self.active = True

    def update(self):
        self.y += self.speed
        self.time += 3
        self.x = self.base_x + self.amplitude * pyxel.sin(self.frequency * self.time)

        # Deactivate if it goes off the screen
        if self.y > pyxel.height:
            self.active = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 9)  # Draw as a yellow rectangle