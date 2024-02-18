"""Here is contained the class to control the game"""
from __future__ import annotations

from typing import Optional

import _const as cte
import neat
import pygame
from _elements import Base, Bird, Pipe


class GameApp:
    """
    Class to be called to launch the game. It puts together all the logic of all the
    classes.
    """

    def __init__(
        self,
        birds: list[Bird],
        pipes_distance: int,
        nets: Optional[list[neat.nn.FeedForwardNetwork]] = None,
        gens: Optional[list[neat.DefaultGenome]] = None,
    ):
        """
        Inits the game

        Parameters
        ----------
        birds: sequence of Bird
            Instances of the bird that will run on a single run.
        pipes_distance: int
            Horizontal distance (pixels) that separate each pipe.
        nets : list of neat-FeedForwardNetworks, optional
            Networks to learn from the game.
        gens : list of neat-DefaultGenome, optional
            Genomes corresponding to the networks.
        """
        self._window = pygame.display.set_mode((cte.WIN_WIDTH, cte.WIN_HEIGHT))
        self._birds = birds
        self._clock = pygame.time.Clock()
        self._pipes = [Pipe(pipes_distance)]
        self._base = Base()

        self.pipes_distance = pipes_distance
        self.playing = True
        self.score = 0

        if nets is not None and gens is not None:
            self._networks = nets
            self._genomes = gens
        else:
            self._networks, self._genomes = [], []
            self._genomes = []

    def _draw_on_window(self):
        """
        Draws all the elements on the window. Each newly drawn element is drawn on
        top of the others.
        """
        self._window.blit(cte.BG_IMG, (0, 0))

        for pipe in self._pipes:
            pipe.draw(self._window)
        self._base.draw(self._window)

        for bird in self._birds:
            bird.draw(self._window)

        text = cte.STAT_FONT.render(f"Score: {self.score}", 1, cte.WHITE)
        self._window.blit(
            text, (cte.WIN_WIDTH - cte.TEXT_OFFSET - text.get_width(), cte.TEXT_OFFSET)
        )

        pygame.display.update()

    def _update_window_elements(self):
        """Calls the 'move' function of all elements and controls the collisions"""
        add_new_pipe = False
        fail_birds_idx = []

        # Evaluate if the next obstacle pipe is the first (idx = 0) or the second
        # (idx = 1) on the list.
        next_pipe_obstacle_idx = int(
            self._birds[0].x_pos > self._pipes[0].x_pos + Pipe.TOP_IMG.get_width()
        )

        for bird, (_, genome), net in zip(self._birds, self._genomes, self._networks):
            bird.move()
            # Rewarding the bird for staying alive
            genome.fitness += 0.1
            output = net.activate(
                inputs=(
                    bird.y_pos,
                    abs(bird.y_pos - self._pipes[next_pipe_obstacle_idx].height),
                    abs(bird.y_pos - self._pipes[next_pipe_obstacle_idx].bottom),
                )
            )
            if output[0] >= 0.5:
                bird.jump()

        self._base.move()
        for pipe in self._pipes:
            pipe.move()

            for idx, bird in enumerate(self._birds):
                bird.move()

                if pipe.has_collided(bird) or bird.on_the_ground:
                    fail_birds_idx.append(idx)
                    self._genomes[idx][1].fitness -= 1

                if not pipe.passed and pipe.x_pos < bird.x_pos:
                    pipe.passed = True
                    add_new_pipe = True
                    self.score += 1
                    self._genomes[idx][1].fitness += 5

        self._pipes = [p for p in self._pipes if not p.has_exited]
        if add_new_pipe:
            self._pipes.append(Pipe(self.pipes_distance))

        birds, genomes, networks = [], [], []
        for idx, (bird, gen, net) in enumerate(
            zip(self._birds, self._genomes, self._networks)
        ):
            if idx not in fail_birds_idx:
                birds.append(bird)
                genomes.append(gen)
                networks.append(net)

        self._birds = birds
        self._genomes = genomes
        self._networks = networks

    def run(self):
        """Main loop of the game"""
        while self.playing:
            self._clock.tick(cte.TICK_CLOCK)
            self._draw_on_window()
            self._update_window_elements()

            if len(self._birds) == 0:
                self.playing = False
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
