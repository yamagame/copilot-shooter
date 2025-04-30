import pyxel
from .state import State
from obj.bullet import Bullet
from obj.meteor import Meteor

class PlayingState(State):
    def update(self):
        # Update stars
        for star in self.game.stars:
            star.update()

        self.game.player.move()

        if self.game.button.shotPushed:
            self.game.bullets.append(Bullet(self.game.player.x + 3, self.game.player.y))
            pyxel.play(0, 0)

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

                  # Add a new meteor if the count is less than 100
                  if len(self.meteors) < 100:
                      self.meteors.append(Meteor())

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
        pyxel.text(5, 5, f"Score: {self.game.score}", 7)
        pyxel.text(5, 15, f"Best: {self.game.best_score}", 7)
