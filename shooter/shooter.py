import pyxel
from player import Player
from bullet import Bullet
from enemy import Enemy
from enemy_bullet import EnemyBullet
from meteor import Meteor
from star import Star  # Import the Star class
from fragment import Fragment


class ShooterGame:
    def __init__(self):
        pyxel.init(200, 150, title="Copilot-Shooter")  # Update the title
        self.game_state = "TITLE"  # TITLE, PLAYING, GAME_OVER, EXPLODING
        self.player = Player(90, 130)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = [Enemy(20, 20)]
        self.meteors = [Meteor() for _ in range(5)]  # Initialize 5 meteors
        self.stars = [Star() for _ in range(50)]  # Initialize 50 stars
        self.fragments = []  # List to store fragments
        self.score = 0
        self.best_score = 0  # Variable to store the best score
        self.game_over_timer = 0  # Timer to track time in GAME_OVER state

        # Define sound effects
        self.setup_sounds()

        pyxel.run(self.update, self.draw)

    def setup_sounds(self):
        """Define sound effects for the game."""
        # Bullet firing sound
        pyxel.sound(0).set(
            "c3e3g3c4", "p", "7", "n", 10
        )
        # Enemy explosion sound
        pyxel.sound(1).set(
            "f3e3d3c3", "p", "7", "n", 10
        )

    def reset_game(self):
        """Reset the game state for a new game."""
        self.player = Player(90, 130)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = [Enemy(20, 20)]
        self.meteors = [Meteor() for _ in range(5)]  # Reset meteors
        self.stars = [Star() for _ in range(50)]  # Reset stars
        self.fragments = []  # Reset fragments
        self.score = 0
        self.game_over_timer = 0  # Reset the game over timer
        self.game_state = "PLAYING"

    def create_explosion(self, x, y):
        """Create a large explosion effect at the given position."""
        for _ in range(50):  # Generate 50 fragments for the explosion
            # Reuse the Fragment class for explosion fragments
            self.fragments.append(Fragment(x, y))
        pyxel.play(1, 1)  # Play explosion sound

    def update(self):
        if self.game_state == "TITLE":
            # Update stars
            for star in self.stars:
                star.update()

            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()

        elif self.game_state == "PLAYING":
            # Update stars
            for star in self.stars:
                star.update()

            # Update fragments
            for fragment in self.fragments:
                fragment.update()
            self.fragments = [f for f in self.fragments if f.lifetime >= 0]

            # Update player
            self.player.move()

            # Shooting bullets
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.bullets.append(Bullet(self.player.x + 3, self.player.y))
                pyxel.play(0, 0)  # Play bullet firing sound

            # Update bullets
            for bullet in self.bullets:
                bullet.update()
            self.bullets = [b for b in self.bullets if b.active]

            # Update enemy bullets
            for bullet in self.enemy_bullets:
                bullet.update()
            self.enemy_bullets = [b for b in self.enemy_bullets if b.active]

            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.enemy_bullets, self.player.x, self.player.y)

            # Update meteors
            for meteor in self.meteors:
                meteor.update()

            # Check collisions
            for enemy in self.enemies:
                if enemy.alive:
                    for bullet in self.bullets:
                        if (
                            enemy.x < bullet.x < enemy.x + enemy.width
                            and enemy.y < bullet.y < enemy.y + enemy.height
                        ):
                            enemy.alive = False
                            bullet.active = False
                            self.score += 10
                            enemy.explode()  # Trigger explosion
                            pyxel.play(1, 1)  # Play enemy explosion sound
                            enemy.respawn()  # Respawn the enemy

                            # Add a new meteor if the count is less than 100
                            if len(self.meteors) < 100:
                                self.meteors.append(Meteor())

            # Check collisions between bullets and meteors
            for meteor in self.meteors:
                for bullet in self.bullets:
                    if (
                        meteor.x < bullet.x < meteor.x + meteor.width
                        and meteor.y < bullet.y < meteor.y + meteor.height
                    ):
                        bullet.active = False  # Deactivate the bullet

            # Check collisions between enemy bullets and player
            for bullet in self.enemy_bullets:
                if (
                    self.player.x < bullet.x < self.player.x + self.player.width
                    and self.player.y < bullet.y < self.player.y + self.player.height
                ):
                    self.create_explosion(
                        self.player.x + self.player.width // 2, self.player.y + self.player.height // 2
                    )
                    self.game_state = "EXPLODING"

            # Check collisions between meteors and player
            for meteor in self.meteors:
                if (
                    self.player.x < meteor.x < self.player.x + self.player.width
                    and self.player.y < meteor.y < self.player.y + meteor.height
                ):
                    self.create_explosion(
                        self.player.x + self.player.width // 2, self.player.y + self.player.height // 2
                    )
                    self.game_state = "EXPLODING"

            # Update the best score during gameplay
            if self.score > self.best_score:
                self.best_score = self.score

        elif self.game_state == "EXPLODING":
            # Update stars
            for star in self.stars:
                star.update()

            # Wait for all fragments to disappear before transitioning to GAME_OVER
            for fragment in self.fragments:
                fragment.update()
            self.fragments = [f for f in self.fragments if f.lifetime >= 0]
            if not self.fragments:  # If no fragments remain, transition to GAME_OVER
                self.game_state = "GAME_OVER"

            # Update enemy             # Update bullets
            for bullet in self.bullets:
                bullet.update()

            for bullet in self.enemy_bullets:
                bullet.update()
            self.enemy_bullets = [b for b in self.enemy_bullets if b.active]

            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.enemy_bullets, self.player.x, self.player.y)

            # Update meteors
            for meteor in self.meteors:
                meteor.update()

        elif self.game_state == "GAME_OVER":
            # Update stars
            for star in self.stars:
                star.update()

            # Update the best score
            if self.score > self.best_score:
                self.best_score = self.score

            # Increment the game over timer
            self.game_over_timer += 1
            # Wait for 3 seconds (180 frames at 60 FPS)
            if self.game_over_timer > 180:
                self.game_state = "TITLE"

            if pyxel.btnp(pyxel.KEY_R):
                self.game_state = "TITLE"

    def draw(self):
        pyxel.cls(0)

        # Draw stars
        for star in self.stars:
            star.draw()

        # Draw fragments
        for fragment in self.fragments:
            fragment.draw()

        if self.game_state == "TITLE":
            pyxel.text(70, 60, "SHOOTER GAME", pyxel.frame_count % 16)
            pyxel.text(50, 90, "PRESS SPACE TO START", 7)
            pyxel.text(50, 110, f"BEST SCORE: {self.best_score}", 7)

        elif self.game_state == "PLAYING":
            # Draw player
            self.player.draw()

            # Draw bullets
            for bullet in self.bullets:
                bullet.draw()

            # Draw enemy bullets
            for bullet in self.enemy_bullets:
                bullet.draw()

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw()

            # Draw meteors
            for meteor in self.meteors:
                meteor.draw()

            # Draw score
            pyxel.text(5, 5, f"Score: {self.score}", 7)

            # Draw best score
            pyxel.text(5, 15, f"Best: {self.best_score}", 7)

        elif self.game_state == "EXPLODING":
            # Do not draw the player in EXPLODING state
            # Draw bullets
            for bullet in self.bullets:
                bullet.draw()

            # Draw enemy bullets
            for bullet in self.enemy_bullets:
                bullet.draw()

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw()

            # Draw meteors
            for meteor in self.meteors:
                meteor.draw()

            # Draw score
            pyxel.text(5, 5, f"Score: {self.score}", 7)

        elif self.game_state == "GAME_OVER":
            pyxel.text(70, 60, "GAME OVER", 8)
            pyxel.text(50, 90, "PRESS R TO RESTART", 7)
            pyxel.text(50, 110, f"BEST SCORE: {self.best_score}", 7)


# Run the game
ShooterGame()
