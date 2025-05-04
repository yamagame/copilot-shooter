import pyxel
from .state import State
from obj.bullet import Bullet

class GameStartState(State):
    def __init__(self, game):
        super().__init__(game)
        self.timer = 60  # Countdown timer for the start state

    def start(self):
        self.timer = 60  # Countdown timer for the start state
        super(GameStartState, self).start()
        return self

    def update(self):
        # Update player position
        self.handle_mouse_movement(self.game.button)
        self.game.player.move()

        for star in self.game.stars:
            star.update()  # Update stars

        for bullet in self.game.bullets:
            bullet.update()  # Update bullets
        self.game.bullets = [b for b in self.game.bullets if b.active]  # Remove inactive bullets

        self.timer -= 1
        if self.timer <= 0:
            self.game.state = self.game.playing_state.start()  # Transition to playing state

    def draw(self):
        pyxel.cls(0)
        pyxel.text((pyxel.width - 40) // 2, pyxel.height // 2, "GET READY!", pyxel.frame_count % 16)
        self.draw_score_and_best()
        for star in self.game.stars:
            star.draw()  # Draw stars
        self.game.player.draw()  # Draw player
        for bullet in self.game.bullets:
            bullet.draw()  # Draw bullets