import pyxel
from .state import State

class TitleState(State):
    def update(self):
        for star in self.game.stars:
            star.update()

        if self.game.button.startPushed or self.game.button.shotPushed:
            self.game.reset_game()
            self.game.state = self.game.game_start_state.start()

    def draw(self):
        pyxel.cls(0)
        for star in self.game.stars:
            star.draw()
        pyxel.text(50, 80, "COPILOT-SHOOTER", pyxel.frame_count % 16)  # Adjusted for new resolution
        pyxel.text(40, 120, "PRESS SPACE TO START", 7)  # Adjusted for new resolution
        pyxel.text(50, 110, f"BEST SCORE: {self.game.best_score}", 7)