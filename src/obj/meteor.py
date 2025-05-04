import pyxel
import random
import math
from obj.fragment import Fragment


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



class GiantMeteor(Meteor):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = 3  # Takes 3 hits to destroy
        self.width = 16  # Larger size for giant meteor
        self.height = 16

    def update(self):
        super().update()
        if self.y > pyxel.height:
            self.active = False  # Deactivate if it goes off the screen

    def split(self):
        """Split into smaller meteors."""
        small_meteors = []
        for _ in range(5):
            dw = self.width
            dh = self.height
            meteor = FragmentMeteor(self.x + random.randint(-dw, dw),self.y + random.randint(-dh, dh), self.speed)
            small_meteors.append(meteor)
        return small_meteors

    def explode(self):
        """Create fragments when the GiantMeteor is destroyed."""
        fragments = []
        for _ in range(300):  # Create 100 fragments
            fragments.append(Fragment(self.x + self.width // 2, self.y + self.height // 2))
        return fragments

    def draw(self):
        pyxel.circ(self.x + self.width // 2, self.y + self.height // 2, self.width // 2, 8)  # Draw as a large circle

class FragmentMeteor(Meteor):
    def __init__(self, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.base_x = x
        self.width = 8
        self.height = 8
        self.speed = speed+random.randint(0, 2)
        self.active = True

    def reset(self):
        self.active = False  # Deactivate if it goes off the screen

    def collides_with(self, obj):
        return (
            self.x < obj.x + obj.width and
            self.x + self.width > obj.x and
            self.y < obj.y + obj.height and
            self.y + self.height > obj.y
        )

    def explode(self):
        """Create fragments when the GiantMeteor is destroyed."""
        fragments = []
        for _ in range(100):  # Create 100 fragments
            fragments.append(Fragment(self.x + self.width // 2, self.y + self.height // 2))
        return fragments

    def update(self):
        super().update()

    def draw(self):
        # Draw as a gray rectangle
        pyxel.rect(self.x, self.y, self.width, self.height, 8)
