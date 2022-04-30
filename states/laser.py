import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        # create a laser shot at 'pos' and 'speed' determines
        #   both speed and direction.
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        # destroy the laser bean if it goes above or below the screen
        # by 50 pixels.  This means that the entire laser bold is off the
        # screen before the sprite is 'killed'.
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        # move the beam, 'self.speed' determines verticle speed and direction
        self.rect.y += self.speed
        self.destroy()
