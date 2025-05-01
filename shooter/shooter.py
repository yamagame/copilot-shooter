import pyxel
from obj.player import Player
from obj.enemy import Enemy
from obj.meteor import Meteor
from obj.star import Star
from obj.fragment import Fragment
from state.title_state import TitleState
from state.playing_state import PlayingState
from state.exploding_state import ExplodingState
from state.game_over_state import GameOverState
from button import Button

class ShooterGame:
    def __init__(self):
        pyxel.init(200, 150, title="Copilot-Shooter")
        self.player = Player(90, 130)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = [Enemy(20, 20)]
        self.meteors = [Meteor() for _ in range(5)]
        self.stars = [Star() for _ in range(50)]
        self.fragments = []
        self.score = 0
        self.best_score = 0
        self.game_over_timer = 0
        self.button = Button()
        self.enemies_defeated = 0

        self.setup_sounds()

        self.title_state = TitleState(self)
        self.playing_state = PlayingState(self)
        self.exploding_state = ExplodingState(self)
        self.game_over_state = GameOverState(self)

        self.state = self.title_state

        pyxel.run(self.update, self.draw)

    def setup_sounds(self):
        """Define sound effects for the game."""
        pyxel.sound(0).set(
            "c3e3g3c4", "p", "7", "n", 10
        )
        pyxel.sound(1).set(
            "f3e3d3c3", "p", "7", "n", 10
        )
        pyxel.sound(2).set(
            "f3e3d3", "p", "7", "n", 10
        )

    def reset_game(self):
        """Reset the game state for a new game."""
        self.player = Player(90, 130)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = [Enemy(20, 20)]
        self.meteors = [Meteor() for _ in range(2)]
        self.stars = [Star() for _ in range(50)]
        self.fragments = []
        self.score = 0
        self.game_over_timer = 0
        self.bt_test = False
        self.enemies_defeated = 0

    def create_explosion(self, x, y):
        """Create a large explosion effect at the given position."""
        for _ in range(50):
            self.fragments.append(Fragment(x, y))
        pyxel.play(1, 1)  # Play explosion sound

    def update(self):
        self.button.update()
        self.state.update()

    def draw(self):
        self.state.draw()


# Run the game
ShooterGame()
