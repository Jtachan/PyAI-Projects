import os
import random
import time
from typing import Union

import neat
import pygame

# Dimensions for the game window
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Loaded images with pygame
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    """
    Class which contains all data for the flappy bird to work

    Attributes
    ----------
    PX_SIZE : int
        Pixel size of the bird at the image. It does not correspond with the image size.
    MAX_ROTATION : int
        Maximum value (degrees) of the rotation for the bird.
    ROTATION_VEL : int
        Velocity at which the rotation updates every clock-tick.
    ANIMATION_TIME : int
        Number of clock-ticks before the bird images change among them.
    x_pos : float
        Current X position in which the bird is.
    y_pos : float
        Current Y position in which the bird is.
    tilt : int
        Current rotation (in degrees) to show the bird pointing up or down.
    tick_count : int
        Number of frames that passed since the last time the bird jumped.
    vel : float
        Current vertical velocity of the bird. A negative velocity indicates the bird
        is moving upwards (image coordinates).
    height : float
        Vertical position at which the last jump was performed.
    img_count : int
        Value to find the current image index for performing the flapping animation.
    """

    PX_SIZE = 50
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x_pos: float, y_pos: float):
        """
        Inits the class

        Parameters
        ----------
        x_pos : int
            Horizontal X position in which the bird starts at the game.
        y_pos : int
            Vertical Y position in which the bird starts at the game.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y_pos
        self.img_count = 0
        self.img = BIRD_IMGS[0]

    def jump(self):
        """Makes the bird 'jump' upwards"""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y_pos

    def move(self):
        """Moves the bird in the vertical axis and updates its tilt"""
        self.tick_count += 1

        # Calculate vertical displacement to update the bird's position
        v_displace = min(self.vel * self.tick_count + 1.5 * self.tick_count**2, 16)

        if v_displace < 0:  # Smoothing jumping trajectory
            v_displace -= 2

        self.y_pos = min(self.y_pos + v_displace, WIN_HEIGHT - self.PX_SIZE)

        # Updating tilt of the bird when it is falling from certain point
        if v_displace < 0 or self.y_pos < (self.height + self.PX_SIZE):
            self.tilt = self.MAX_ROTATION
        elif self.tilt > -90:
            # Update rotation in falling motion
            self.tilt -= self.ROTATION_VEL

    def draw(self, window: Union[pygame.Surface, pygame.SurfaceType]):
        """
        Draws the bird on the window, choosing the correct image to draw the bird to
        create the flapping animation.
        The image sequence to follow to make it seen the bird is flapping is:
            [0, 1, 2, 1, 0]
        The bird stops flapping if its nose is pointing down.

        Parameters
        ----------
        window : Surface
            Display where the bird is drawn
        """
        if self.tilt <= -80:
            # Stop animation if the bird is falling too much
            # and reset counter in case the bird jumps again
            self.img = BIRD_IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        else:
            # Update bird images to seem it is flapping the wings
            self.img_count += 1
            if self.img_count < self.ANIMATION_TIME * 3:
                self.img = BIRD_IMGS[self.img_count // self.ANIMATION_TIME]
            elif self.img_count < self.ANIMATION_TIME * 4:
                self.img = BIRD_IMGS[1]
            else:
                self.img = BIRD_IMGS[0]
                self.img_count = 0

        # Rotating the bird image depending on its current tilt
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x_pos, self.y_pos)).center
        )

        # Updating the images at the window
        window.blit(rotated_image, new_rect.topleft)

    @property
    def collision_mask(self) -> pygame.Mask:
        """Mask: Area corresponding to the pixels that contain the bird"""
        return pygame.mask.from_surface(self.img)


class Pipe:
    """
    Controls all physics related to the pipes. Each 'Pipe' composes a set of two pipes
    (top and bottom) with a gap in between for the bird to go through.

    Attributes
    ----------
    GAP : int
        Space among the top and bottom pipes.
    VEL : int
        Velocity at which the pipes move.
    TOP_IMG : Surface
        Image to be used for the top pipe.
    BOT_IMG : Surface
        Image to be used for the bottom pipe.
    x_pos : float
        Current horizontal position of the set of pipes.
    height : float
        Vertical position corresponding to where the top pipe ends.
    top : float
        Vertical position corresponding to where the top pipe is placed.
    bottom : float
        Vertical position corresponding to where the bottom pipe is placed.
    """

    GAP = 200
    VEL = 5
    TOP_IMG = pygame.transform.flip(PIPE_IMG, flip_x=False, flip_y=True)
    BOT_IMG = PIPE_IMG

    def __init__(self, x_pos: float):
        """
        Inits the class. Each set of pipes are initialized at a random height.

        Parameters
        ----------
        x_pos : float
            Initial X position where the pipes start
        """
        self.x_pos = x_pos
        self.height = random.randrange(50, 450)
        self.top = self.height - self.TOP_IMG.get_height()
        self.bottom = self.height + self.GAP
        self.passed = False

    def move(self):
        """Updates the pipes' position moving them to the left"""
        self.x_pos -= self.VEL

    def draw(self, window: Union[pygame.Surface, pygame.SurfaceType]):
        """Draws the top & bottom pipes at the window"""
        window.blit(self.TOP_IMG, (self.x_pos, self.top))
        window.blit(self.BOT_IMG, (self.x_pos, self.bottom))

    def has_collided(self, bird: Bird) -> bool:
        """
        Calculates if the bird collides with any of the pipes. Masks are used to
        obtain a pixel collision, instead of a bounding box collision.
        """
        bird_collision_mask = bird.collision_mask
        top_mask = pygame.mask.from_surface(self.TOP_IMG)
        bottom_mask = pygame.mask.from_surface(self.BOT_IMG)

        top_offset = (self.x_pos - bird.x_pos, self.top - round(bird.y_pos))
        bottom_offset = (self.x_pos - bird.x_pos, self.bottom - round(bird.y_pos))

        top_col_point = bird_collision_mask.overlap(top_mask, top_offset)
        bot_col_point = bird_collision_mask.overlap(bottom_mask, bottom_offset)

        return top_col_point is not None or bot_col_point is not None


class Base:
    """
    Class to control the ground on the screen

    Attributes
    ----------
    VEL : int
        Velocity at which the ground moves. This is the same speed as the used by the
        pipes.
    WIDTH : int
        Width of the image that compose the base.
    y_pos : float
        Vertical position where the ground is placed.
    x_pos_1 : int
        Horizontal position of the first piece of ground.
    x_pos_2 : int
        Horizontal position of the second piece of ground.
    """

    VEL = Pipe.VEL
    WIDTH = BASE_IMG.get_width()

    def __init__(self, y_pos: float):
        """
        Inits the class.

        Parameters
        ----------
        y_pos : float
            Vertical position where the ground is placed
        """
        self.y_pos = y_pos
        self.x_pos_1 = 0
        self.x_pos_2 = self.WIDTH

    def move(self):
        """
        Moves the base to create the feeling the bird is the one moving.
        To create the illusion the path is infinite, two images are placed
        consecutively. When one image exits the screen from the left, its position is
        updated to outside the screen on the right (so it enters the next clock-tick).
        """
        self.x_pos_1 -= self.VEL
        self.x_pos_2 -= self.VEL

        if self.x_pos_1 + self.WIDTH < 0:
            self.x_pos_1 = self.x_pos_2 + self.WIDTH

        if self.x_pos_2 + self.WIDTH < 0:
            self.x_pos_2 = self.x_pos_1 + self.WIDTH

    def draw(self, window: Union[pygame.Surface, pygame.SurfaceType]):
        """Draws the top & bottom pipes at the window"""
        window.blit(BASE_IMG, (self.x_pos_1, self.y_pos))
        window.blit(BASE_IMG, (self.x_pos_2, self.y_pos))


def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()


if __name__ == "__main__":
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)

        draw_window(win, bird)
        bird.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
