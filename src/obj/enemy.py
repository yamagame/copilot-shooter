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
        self.active = True
        self.respawn_timer = 0  # Timer for respawn delay
        self.blink_timer = 60  # Set blink duration to 60 frames

    def update(self, bullets, player_x, player_y):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            return  # Skip update if in respawn delay

        if self.blink_timer > 0:
            self.blink_timer -= 1
            return  # Skip movement during blinking

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

    def explode(self):
        """Generate fragments when the enemy is hit."""
        fragments = []
        for _ in range(100):  # Create 100 fragments
            fragments.append(
                Fragment(self.x + self.width // 2, self.y + self.height // 2))
        return fragments

    def respawn(self):
        self.respawn_timer = 300  # Set respawn delay to 300 frames
        self.blink_timer = 60  # Reset blink timer
        # Respawn at a random position
        self.x = random.randint(0, pyxel.width - self.width)
        self.y = random.randint(0, pyxel.height // 2)
        self.alive = True
        self.active = True

    def draw(self):
        if self.respawn_timer > 0:
            return  # Do not draw if in respawn delay
        if self.blink_timer > 0:
            if self.blink_timer % 4 < 2:  # Blink effect
                pyxel.rect(self.x, self.y, self.width, self.height, 8)
            return
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, 8)

    def collides_with(self, obj):
        if self.respawn_timer > 0:
            return False  # No collision if in respawn delay
        return (
            self.x < obj.x + obj.width
            and self.x + self.width > obj.x
            and self.y < obj.y + obj.height
            and self.y + self.height > obj.y
        )
