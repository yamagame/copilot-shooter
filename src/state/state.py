import pyxel
from obj.bullet import Bullet

class State:
    def __init__(self, game):
        self.game = game

    def start(self):
        return self

    def reset_cooldown(self):
        self.game.shot_cooldown = 0  # Cooldown timer for continuous shooting

    def update(self):
        pass

    def draw(self):
        pass

    def can_shoot_bullet(self):
        return len(self.game.bullets) < self.game.bullet_limit

    # Update player position based on mouse movement (horizontal movement only)
    def handle_mouse_movement(self, button):
        if button.mousePressed:
            current_mouse_x, _ = button.get_mouse_position()
            delta_x = current_mouse_x - button.mouse_start_x
            self.game.player.x += delta_x
            button.mouse_start_x = current_mouse_x  # Update start position for next frame

        # Handle continuous shooting
        if (button.shotPressed and self.game.shot_cooldown == 0) or button.shotPushed:
            if self.can_shoot_bullet():
                self.game.bullets.append(Bullet(self.game.player.x + 3, self.game.player.y))
                pyxel.play(0, 0)  # Play bullet firing sound
                self.game.shot_cooldown = 6  # Set cooldown to 6 frames
        if self.game.shot_cooldown > 0:
            self.game.shot_cooldown -= 1

    def draw_score_and_best(self):
        pyxel.text(5, 5, f"SCORE: {self.game.score}", 7)
        pyxel.text(5, 15, f"BEST: {self.game.best_score}", 7)
