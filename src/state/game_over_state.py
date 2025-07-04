import pyxel
from .state import State

class GameOverState(State):
    def update(self):
        for star in self.game.stars:
            star.update()

        self.game.game_over_timer += 1
        if self.game.game_over_timer > 180:  # Wait for 3 seconds (180 frames at 60 FPS)
            self.game.state = self.game.title_state

        if pyxel.btnp(pyxel.KEY_R) or any(
            pyxel.btnp(button)
            for button in [
                pyxel.KEY_SPACE,
                pyxel.GAMEPAD1_BUTTON_A,
                pyxel.GAMEPAD1_BUTTON_B,
                pyxel.GAMEPAD1_BUTTON_X,
                pyxel.GAMEPAD1_BUTTON_Y,
            ]
        ):
            self.game.state = self.game.title_state

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.game.state = self.game.title_state
            self.game.reset_game()

    def draw(self):
        pyxel.cls(0)
        for star in self.game.stars:
            star.draw()
        pyxel.text(65, 80, "GAME OVER", 8)  # Adjusted for new resolution
        pyxel.text(45, 120, "PRESS R TO RESTART", 7)  # Adjusted for new resolution
        pyxel.text(5, 5, f"Score: {self.game.score}", 7)
        pyxel.text(5, 15, f"Best: {self.game.best_score}", 7)
