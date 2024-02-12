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
    x_pos : int
        Current X position in which the bird is.
    y_pos : int
        Current Y position in which the bird is.
    tilt : int
        Current rotation (in degrees) to show the bird pointing up or down.
    vel : float
        Current vertical velocity of the bird. A negative velocity indicates the bird
        is moving upwards (image coordinates).
    tick_count : int
        Number of frames that passed since the last time the bird jumped.
    """

    PX_SIZE = 50
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x_pos: int, y_pos: int):
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
        """Moves the bird in the vertical axis"""
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

    def get_collision_mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.img)


class Pipe:
    """
    Controls all physics related to the pipes
    """
    GAP = 200
    VEL = 5

    TOP_IMG = pygame.transform.flip(PIPE_IMG, flip_x=False, flip_y=True)
    BOT_IMG = PIPE_IMG

    def __init__(self, x_pos: int):
        self.x_pos = x_pos
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.passed = False

    def set_random_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.TOP_IMG.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Updates the pipes' position moving them to the left"""
        self.x_pos -= self.VEL

    def draw(self, window: Union[pygame.Surface, pygame.SurfaceType]):
        """Draws the top & bottom pipes at the window"""
        window.blit(self.TOP_IMG, (self.x_pos, self.top))
        window.blit(self.BOT_IMG, (self.x_pos, self.bottom))

    def has_collided(self, bird: Bird) -> bool:
        """
        Calculates if the bird collides with any of the pipes. Masks are used to obtain
        a pixel collision, instead of a bounding box collision.
        """
        bird_collision_mask = bird.get_collision_mask()
        top_mask = pygame.mask.from_surface(self.TOP_IMG)
        bottom_mask = pygame.mask.from_surface(self.BOT_IMG)

        top_offset = (self.x_pos - bird.x_pos, self.top - round(bird.y_pos))
        bottom_offset = (self.x_pos - bird.x_pos, self.bottom - round(bird.y_pos))

        top_col_point = bird_collision_mask.overlap(top_mask, top_offset)
        bot_col_point = bird_collision_mask.overlap(bottom_mask, bottom_offset)

        return top_col_point is not None or bot_col_point is not None


class Base:
    """Class to control the ground on the screen"""
    VEL = Pipe.VEL
    WIDTH = BASE_IMG.get_width()

    def __init__(self, y_pos: int):
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


if __name__ == '__main__':
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

