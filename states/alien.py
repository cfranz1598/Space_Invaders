import pygame
from random import choices


class Alien(pygame.sprite.Sprite):
    def __init__(self, value, x, y, image):
        # This istantiates the aliens.  There are three kinds by color.
        #  Each color has a value when destroyed by the player.
        super().__init__()
        # setup alien image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.value = value

    def update(self, direction):
        # positive direction goes right negative goes left
        self.rect.x += direction


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width, image):
        # This instantiates that alien that occasionally fly's across the screen
        #   I dislike the name 'Extra' but can't think of anything else concise.
        super().__init__()
        self.image = image

        # entering from the right or left?
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        # positive speed goes right negative goes left
        self.rect.x += self.speed
