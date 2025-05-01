import pyxel
import random
from obj.enemy_bullet import EnemyBullet
from obj.fragment import Fragment


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.alive = True
        self.direction = 1  # 1: moving right, -1: moving left
        self.shoot_timer = random.randint(30, 90)  # Random initial timer
        self.fragments = []  # List to store fragments
        self.active = True

    def update(self, bullets, player_x, player_y):
        if self.alive:
            self.x += self.direction * 2
            # Reverse direction if hitting screen edges
            if self.x <= 0 or self.x >= pyxel.width - self.width:
                self.direction *= -1

            # Shooting logic with random intervals
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                bullets.append(EnemyBullet(self.x + self.width //
                               2, self.y + self.height, player_x, player_y))
                # Reset timer with random value
                self.shoot_timer = random.randint(10, 50)

        # Update fragments
        for fragment in self.fragments:
            fragment.update()
        self.fragments = [f for f in self.fragments if f.lifetime > 0]

    def explode(self):
        """Generate fragments when the enemy is hit."""
        for _ in range(100):  # Create 100 fragments
            self.fragments.append(
                Fragment(self.x + self.width // 2, self.y + self.height // 2))

    def respawn(self):
        # Respawn at a random position
        self.x = random.randint(0, pyxel.width - self.width)
        self.y = random.randint(0, pyxel.height // 2)
        self.alive = True
        self.active = True

    def draw(self):
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, 8)
        # Draw fragments
        for fragment in self.fragments:
            fragment.draw()
