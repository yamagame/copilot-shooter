import pyxel
from .state import State

class TitleState(State):
    def update(self):
        for star in self.game.stars:
            star.update()

        if self.game.button.startPushed or self.game.button.shotPushed:
            self.game.reset_game()
            self.game.state = self.game.playing_state.start()

    def draw(self):
        pyxel.cls(0)
        for star in self.game.stars:
            star.draw()
        pyxel.text(70, 60, "COPILOT-SHOOTER", pyxel.frame_count % 16)
        pyxel.text(50, 90, "PRESS SPACE TO START", 7)
        pyxel.text(50, 110, f"BEST SCORE: {self.game.best_score}", 7)