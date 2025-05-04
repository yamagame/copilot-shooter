import pyxel
import random


class Fragment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 360)  # Random angle in radians
        speed = random.uniform(0.5, 2)  # Random speed
        self.vx = speed * pyxel.cos(angle)  # Horizontal speed based on angle
        self.vy = speed * pyxel.sin(angle)  # Vertical speed based on angle
        self.lifetime = random.randint(20, 40)  # Lifetime in frames
        self.color = random.choice([8, 9, 10, 11])  # Random color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95  # Gradually reduce horizontal speed
        self.vy *= 0.95  # Gradually reduce vertical speed
        self.lifetime -= 1
        self.color = random.choice([8, 9, 10, 11])  # Random color

    def draw(self):
        if self.lifetime > 0:
            # Make the fragment blink by alternating visibility based on lifetime
            if self.lifetime % 4 < 2:  # Visible for 2 frames, invisible for 2 frames
                pyxel.pset(self.x, self.y, self.color)  # Draw as a single pixel
