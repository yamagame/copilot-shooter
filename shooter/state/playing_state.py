import pyxel
from .state import State
from obj.bullet import Bullet
from obj.meteor import Meteor
from obj.powerup import PowerUp

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)

    def can_shoot_bullet(self):
        return len(self.game.bullets) < 2

    def update(self):
        # Update stars
        for star in self.game.stars:
            star.update()

        self.game.player.move()

        if self.game.button.shotPushed and self.can_shoot_bullet():
            self.game.bullets.append(Bullet(self.game.player.x + 3, self.game.player.y))
            pyxel.play(0, 0)  # Play bullet firing sound

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

        # Update meteors
        for meteor in self.game.meteors:
            meteor.update()

        # Spawn power-ups every 30 seconds (1800 frames at 60 FPS)
        self.game.powerup_timer += 1
        if self.game.powerup_timer >= 180*5:
            self.game.powerups.append(PowerUp())
            self.game.powerup_timer = 0

        # Update power-ups
        for powerup in self.game.powerups:
            powerup.update()
        self.game.powerups = [p for p in self.game.powerups if p.active]  # Remove off-screen power-ups

        # Check for collisions between bullets and enemies
        for bullet in self.game.bullets:
            for enemy in self.game.enemies:
              if bullet.collides_with(enemy):
                  bullet.active = False
                  enemy.active = False
                  self.game.score += 100
                  enemy.explode()  # Trigger explosion
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
                if (
                    meteor.x < bullet.x < meteor.x + meteor.width
                    and meteor.y < bullet.y < meteor.y + meteor.height
                ):
                    bullet.active = False  # Deactivate the bullet
                    self.game.score += 10
                    pyxel.play(2, 2)  # Play a "ping" sound when bullet hits meteor

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

        # Remove inactive enemies and meteors
        self.game.enemies = [e for e in self.game.enemies if e.active]
        self.game.meteors = [m for m in self.game.meteors if m.active]

        # Update the best score during gameplay
        if self.game.score > self.game.best_score:
            self.game.best_score = self.game.score

    def draw(self):
        pyxel.cls(0)
        for star in self.game.stars:
            star.draw()
        self.game.player.draw()
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
