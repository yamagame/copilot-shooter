import pyxel
from .state import State
from obj.bullet import Bullet

class GameStartState(State):
    def __init__(self, game):
        super().__init__(game)
        self.timer = 60  # Countdown timer for the start state

    def can_shoot_bullet(self):
        return len(self.game.bullets) < self.game.bullet_limit

    def start(self):
        self.shot_cooldown = 10  # Cooldown timer for continuous shooting
        self.timer = 60  # Reset timer when entering the state
        return self

    def update(self):
        for star in self.game.stars:
            star.update()  # Update stars
        self.game.player.move()  # Update player movement

        # Handle continuous shooting
        if (self.game.button.shotPressed and self.shot_cooldown == 0) or self.game.button.shotPushed:
            if self.can_shoot_bullet():
                self.game.bullets.append(Bullet(self.game.player.x + 3, self.game.player.y))
                pyxel.play(0, 0)  # Play bullet firing sound
                self.shot_cooldown = 6  # Set cooldown to 6 frames
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

        for bullet in self.game.bullets:
            bullet.update()  # Update bullets
        self.game.bullets = [b for b in self.game.bullets if b.active]  # Remove inactive bullets

        self.timer -= 1
        if self.timer <= 0:
            self.game.state = self.game.playing_state.start()  # Transition to playing state

    def draw(self):
        pyxel.cls(0)
        pyxel.text((pyxel.width - 40) // 2, pyxel.height // 2, "GET READY!", pyxel.frame_count % 16)
        pyxel.text(5, 5, f"SCORE: {self.game.score}", 7)
        pyxel.text(5, 15, f"BEST: {self.game.best_score}", 7)
        for star in self.game.stars:
            star.draw()  # Draw stars
        self.game.player.draw()  # Draw player
        for bullet in self.game.bullets:
            bullet.draw()  # Draw bullets