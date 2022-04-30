# system imports
import pygame
from random import choices

# game imports
from .laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed, cooldown, assets):
        super().__init__()

        # Get player image and hit image
        self.image = assets.retrieve_asset('playerOK')
        self.rect = self.image.get_rect(midbottom=pos)
        self.image_ok = self.image
        self.image_hit = assets.retrieve_asset('playerHIT')

        # set player movement parameters
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.game_over = False
        self.laser_time = 0
        self.laser_cooldown = cooldown
        self.go_right = False
        self.go_left = False
        self.player_shoot = False

        # set up player hit animation
        self.hit = False
        self.hit_animation = 0.15
        self.hit_limit = 15
        self.hit_limit_count = 0

        # Laser setup
        self.lasers = pygame.sprite.Group()
        self.laser_sound = assets.retrieve_asset('pewpew')
        self.laser_sound.set_volume(0.5)

    def get_event(self, event):
        # player can only move right or left but... player must keep
        # going from KEYDOWN to KEYUP.  This is an artifact of the way
        # events are gathered and distributed.  Holding down the key
        # doesn't cause it to just keep doing what the key is for.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.go_right = True
            if event.key == pygame.K_LEFT:
                self.go_left = True
            if event.key == pygame.K_SPACE and self.ready:
                self.player_shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.go_right = False
            if event.key == pygame.K_LEFT:
                self.go_left = False
            if event.key == pygame.K_SPACE:
                self.player_shoot = False

    def move_player(self):
        if self.go_right:
            self.rect.x += self.speed
        if self.go_left:
            self.rect.x -= self.speed

    def constraint(self):
        # stops player from leaving the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        # if 'player shoot' is ordered... and the laser is 'ready' and the
        # game is not over, shoot, then trigger the recharge period
        if self.player_shoot and self.ready and not self.game_over:
            self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
            # This initiates the 'recharge' period for the players shots
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def recharge_laser(self):
        # after firing the laser it takes a moment or two to 'recharge'
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def player_hit(self):
        # Signals to the mainline game that the player has been
        #  hit.  Causes the number of lives to decrease, etc.
        self.hit = True

    def update(self):
        self.image = self.image_ok
        # If hit, flash between blue and red player icon
        #  Before I added this this hits on the player
        #  were kind of not noticable.
        if self.hit:
            self.image = choices(
                [self.image_hit, self.image_ok], weights=[2, 1], k=1)[0]
            self.hit_limit_count += self.hit_animation
            if self.hit_limit_count > self.hit_limit:
                self.hit = False
                self.hit_limit_count = 0

        # all the procedures to move and fight the player
        self.shoot_laser()
        self.move_player()
        self.constraint()
        self.recharge_laser()
        self.lasers.update()
