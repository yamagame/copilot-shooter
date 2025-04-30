import pyxel
from .state import State

class ExplodingState(State):
    def update(self):
        # Update starts
        for star in self.game.stars:
            star.update()

        # Update fragments
        for fragment in self.game.fragments:
            fragment.update()
        self.game.fragments = [f for f in self.game.fragments if f.lifetime >= 0]

        if not self.game.fragments:  # If no fragments remain, transition to GAME_OVER
            self.game.state = self.game.game_over_state

        # Update bullets
        for bullet in self.game.bullets:
            bullet.update()
        self.game.bullets = [b for b in self.game.bullets if b.active]

        # Update enemy_bullets
        for bullet in self.game.enemy_bullets:
            bullet.update()

        # Update enemies
        for enemy in self.game.enemies:
            enemy.update(self.game.bullets, self.game.player.x, self.game.player.y)

        # Update meteors
        for meteor in self.game.meteors:
            meteor.update()



    def draw(self):
        pyxel.cls(0)
        for star in self.game.stars:
            star.draw()
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
        pyxel.text(5, 5, f"Score: {self.game.score}", 7)
        pyxel.text(5, 15, f"Best: {self.game.best_score}", 7)
