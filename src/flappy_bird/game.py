"""Here is contained the class to control the game"""
import _const as cte
import pygame
from _elements import Base, Bird, Pipe


class GameApp:
    """
    Class to be called to launch the game. It puts together all the logic of all the
    classes.
    """

    def __init__(self, bird: Bird, pipes_distance: int, base: Base):
        """
        Inits the game

        Parameters
        ----------
        bird: Bird
            Instance of the bird.
        pipes_distance: int
            Horizontal distance (pixels) that separate each pipe.
        base: Base
            Instance of a base.
        """
        self._window = pygame.display.set_mode((cte.WIN_WIDTH, cte.WIN_HEIGHT))
        self._bird = bird
        self._clock = pygame.time.Clock()
        self._pipes = [Pipe(pipes_distance)]
        self._base = base

        self.pipes_distance = pipes_distance
        self.playing = True
        self.score = 0

    def _draw_on_window(self):
        """
        Draws all the elements on the window. Each newly drawn element is drawn on
        top of the others.
        """
        self._window.blit(cte.BG_IMG, (0, 0))

        for pipe in self._pipes:
            pipe.draw(self._window)
        self._base.draw(self._window)
        self._bird.draw(self._window)

        text = cte.STAT_FONT.render(f"Score: {self.score}", 1, cte.WHITE)
        self._window.blit(text, (cte.WIN_WIDTH - 10 - text.get_width(), 10))

        pygame.display.update()

    def _update_window_elements(self):
        """Calls the 'move' function of all elements and controls the collisions"""
        if not self._bird.on_the_ground:
            # self._bird.move()
            self._base.move()

            add_new_pipe = False
            for pipe in self._pipes:
                pipe.move()
                if pipe.has_collided(self._bird):
                    ...

                if not pipe.passed and pipe.x_pos < self._bird.x_pos:
                    pipe.passed = True
                    add_new_pipe = True
                    self.score += 1

            self._pipes = [p for p in self._pipes if not p.has_exited]
            if add_new_pipe:
                self._pipes.append(Pipe(self.pipes_distance))

    def run(self):
        """Main loop of the game"""
        while self.playing:
            self._clock.tick(30)
            self._draw_on_window()
            self._update_window_elements()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False

        pygame.quit()


if __name__ == "__main__":
    GameApp(
        bird=Bird(),
        base=Base(),
        pipes_distance=600,
    ).run()
