import pyxel
from .state import State
from obj.bullet import Bullet
from obj.enemy import Enemy
from obj.meteor import Meteor, GiantMeteor
from obj.powerup import PowerUp
import random

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)

    def can_shoot_bullet(self):
        return len(self.game.bullets) < self.game.bullet_limit

    def start(self):
        self.shot_cooldown = 10  # Cooldown timer for continuous shooting
        self.mouse_shot_cooldown = 10  # Cooldown timer for mouse-based shooting
        return self

    def update(self):
        # Update stars
        for star in self.game.stars:
            star.update()

        # Player movement processing
        self.handle_player_movement_and_shooting()

        # Update bullets
        for bullet in self.game.bullets:
            bullet.update()
        self.game.bullets = [b for b in self.game.bullets if b.active]

        # Update enemy_bullets
        for bullet in self.game.enemy_bullets:
            bullet.update()

        # Update enemies
        for enemy in self.game.enemies:
            enemy.update(self.game.enemy_bullets, self.game.player.x, self.game.player.y)

        # Increase enemy count every 1000 points
        if self.game.score // 1000 > len(self.game.enemies) - 1:
            self.game.enemies.append(Enemy(random.randint(0, pyxel.width - 8), random.randint(0, pyxel.height // 2)))

        # Update meteors
        for meteor in self.game.meteors:
            meteor.update()

        # Update fragments
        for fragment in self.game.fragments:
            fragment.update()
        self.game.fragments = [f for f in self.game.fragments if f.lifetime >= 0]

        # Spawn power-ups every 30 seconds (1800 frames at 60 FPS)
        self.game.powerup_timer += 1
        if self.game.powerup_timer >= 180*5:
            self.game.powerups.append(PowerUp())
            self.game.powerup_timer = 0

        # Spawn a giant meteor occasionally
        if pyxel.frame_count % 600 == 0:  # Every 10 seconds at 60 FPS
            self.game.meteors.append(GiantMeteor(random.randint(0, pyxel.width - 16), -16))

        # Update power-ups
        for powerup in self.game.powerups:
            powerup.update()
        self.game.powerups = [p for p in self.game.powerups if p.active]  # Remove off-screen power-ups

        # Collision detection
        self.handle_collisions()

        # Remove inactive power-ups
        self.game.powerups = [p for p in self.game.powerups if p.active]

        # Remove inactive enemies and meteors
        self.game.enemies = [e for e in self.game.enemies if e.active]
        self.game.meteors = [m for m in self.game.meteors if m.active]

        # Update the best score during gameplay
        if self.game.score > self.game.best_score:
            self.game.best_score = self.game.score
    
    # Player movement processing
    def handle_player_movement_and_shooting(self):
        # Update player position based on mouse movement (horizontal movement only)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_start_x, _ = self.game.button.get_mouse_position()

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            current_mouse_x, _ = self.game.button.get_mouse_position()
            delta_x = current_mouse_x - self.mouse_start_x
            self.game.player.x += delta_x
            self.mouse_start_x = current_mouse_x  # Update start position for next frame

        self.game.player.move()

        # Handle continuous shooting
        if (self.game.button.shotPressed and self.shot_cooldown == 0) or self.game.button.shotPushed:
            if self.can_shoot_bullet():
                self.game.bullets.append(Bullet(self.game.player.x + 3, self.game.player.y))
                pyxel.play(0, 0)  # Play bullet firing sound
                self.shot_cooldown = 6  # Set cooldown to 6 frames
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

        # Handle mouse-based shooting
        if self.game.button.is_mouse_left_pressed():
            if self.mouse_shot_cooldown == 0 and self.can_shoot_bullet():
                self.game.bullets.append(Bullet(self.game.player.x + 3, self.game.player.y))
                pyxel.play(0, 0)  # Play bullet firing sound
                self.mouse_shot_cooldown = 6  # Set cooldown to 6 frames
        if self.mouse_shot_cooldown > 0:
            self.mouse_shot_cooldown -= 1

    # Collision detection
    def handle_collisions(self):
        # Check for collisions between bullets and enemies
        for bullet in self.game.bullets:
            for enemy in self.game.enemies:
                if enemy.collides_with(bullet):
                    bullet.active = False
                    enemy.active = False
                    self.game.score += 100
                    self.game.fragments.extend(enemy.explode())  # Trigger explosion
                    enemy.respawn()
                    pyxel.play(1, 1)  # Play enemy explosion sound

                    self.game.enemies_defeated += 1  # Increment defeated enemies count

                    # Add a new meteor for every 3 enemies defeated
                    if self.game.enemies_defeated % 3 == 0:
                        self.game.meteors.append(Meteor())

        # Check for collisions between player and meteors
        for meteor in self.game.meteors:
            if meteor.collides_with(self.game.player):
                self.game.player.active = False
                self.game.game_over = True

        # Check collisions between bullets and meteors
        for meteor in self.game.meteors:
            for bullet in self.game.bullets:
                if bullet.collides_with(meteor):
                    bullet.active = False  # Deactivate the bullet
                    self.game.score += 10
                    pyxel.play(2, 2)  # Play a "ping" sound when bullet hits meteor

        # Check for collisions between bullets and giant meteors
        for meteor in self.game.meteors:
            if isinstance(meteor, GiantMeteor):
                for bullet in self.game.bullets:
                    if bullet.collides_with(meteor):
                        bullet.active = False
                        meteor.health -= 1
                        if meteor.health <= 0:
                            self.game.meteors.extend(meteor.split())  # Add smaller meteors
                            self.game.fragments.extend(meteor.explode())
                            meteor.active = False
                            self.game.score += 100  # Add 100 points for destroying a GiantMeteor
                            pyxel.play(1, 4)  # Play giant meteor explosion sound

        # Check collisions between enemy bullets and player
        for bullet in self.game.enemy_bullets:
            if bullet.collides_with(self.game.player):
                self.game.create_explosion(
                    self.game.player.x + self.game.player.width // 2, self.game.player.y + self.game.player.height // 2
                )
                self.game.state = self.game.exploding_state
                bullet.active = False

        # Check collisions between meteors and player
        for meteor in self.game.meteors:
            if meteor.collides_with(self.game.player):
                self.game.create_explosion(
                    self.game.player.x + self.game.player.width // 2, self.game.player.y + self.game.player.height // 2
                )
                self.game.state = self.game.exploding_state

        # Check for collisions between player and power-ups
        for powerup in self.game.powerups:
            if self.game.player.collides_with(powerup):
                self.game.increase_bullet_limit()  # Increase bullet limit
                powerup.active = False  # Deactivate the power-up
                pyxel.play(3, 3)  # Play power-up sound

    def draw(self):
        pyxel.cls(0)
        for star in self.game.stars:
            star.draw()
        self.game.player.draw()
        for fragment in self.game.fragments:
            fragment.draw()
        for bullet in self.game.bullets:
            bullet.draw()
        for bullet in self.game.enemy_bullets:
            bullet.draw()
        for enemy in self.game.enemies:
            enemy.draw()
        for meteor in self.game.meteors:
            meteor.draw()
        for powerup in self.game.powerups:
            powerup.draw()
        pyxel.text(5, 5, f"Score: {self.game.score}", 7)
        pyxel.text(5, 15, f"Best: {self.game.best_score}", 7)
