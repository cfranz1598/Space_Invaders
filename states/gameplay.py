"""
	This is, in fact, a decent version of the classic video game "Space Invaders" from
	the video game in every American bar in the 70s and 80s.  The wikipedia article
    about the original arcade game is: https://en.wikipedia.org/wiki/Space_Invaders and
    a game players guide: https://www.classicgaming.cc/classics/space-invaders/play-guide

    This one is written in Python using the pygame library.  It"s not bad.  It is simplified
    as, you'll note the original had 5 rows of 11 alien and fast, slow, and wiggly lasers plus
    the aliens sped up as there became fewer and fewer of them.

    In this version the alien animations is missing, the extra alien across the top doesn't
    shoot, the aliens don't speed up, and the aliens only shoot the same lasers the player
    does.


	** Credit **
	Most of this was written by YouTube handle "Clear Code":
		YouTube Tutorial: https://www.youtube.com/watch?v=o-6pADy5Mdg&t=3219s
		Clear Code on YouTube: https://www.youtube.com/channel/UCznj32AM2r98hZfTxrRo9bQ
		Original Respository: https://github.com/clear-code-projects/Space-invaders

	My additions are:
		1) Cleaning up the code to more or less PEP8 standards (I prefer tabs to spaces).
		2) Adding substantial comments to the code.
		3) Added game level logic so it playes till you die.
		4) Added both a you lose screen and a non-abrupt end of game.
		5) Added some effects when the player gets hit... He flashes red.
		6) There was something with the explosions or the laser sound effects which.
			needed help, but I"ll be dipped if I can remember what.
		7) I think I fixed the lives display at the top of the screen.
		8) Changed RGB colors to the newer pygame color names.

	I also kind of removed the original pixelated font which, while more authentic, was
	really hard to read.  Code is there, put it back if you want.

	I was going to pull of the settings variables out and put them in a separate "settings.py"
	file and fix some naming convensions, but I forgot.  That"ll be a must when I add gaming
	menus to it, I suspect.

	This was rewritten and tested on Python 3.9.2 and pygame 2.1.2... So, if it doesn"t
	work on your system that"s entirely my fault.  Try the original.

	As per usual, any spelling or grammar mistakes are yours to keep.  Don"t get them wet,
	don"t feed them after midnight.  You"ve been warned.
"""

# system imports
import pygame
from random import choices, choice, randint
# game state management import
from .base import BaseState

# game import
from .player import Player
from .obstacle import *
from .alien import Alien, Extra
from .laser import Laser

# events needed
ALIENLASER = pygame.USEREVENT + 1
GAMEEND_EVENT = pygame.USEREVENT + 2


class GamePlay(BaseState):
    def __init__(self, game_assets):
        super(GamePlay, self).__init__(game_assets)
        self.next_state = "MENU"
        self.status = "lose"

    def create_obstacle(self, x_start, y_start, offset_x):
        # Build the obstacles.  They are made of 6x6 blocks so that
        # 	when lasers hit them they can disintegrate piece by piece.
        #   Clever solution to the problem.
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Block(self.block_size, "firebrick3", x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        # lay out the obstacles across the screen
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        # make rows and columns of aliens - what fun
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                # first (top) row is yellow aliens, rows two and three are
                #   green aliens, the rest are the red aliens.
                if row_index == 0:
                    alien_sprite = Alien(
                        300, x, y, self.game_assets.retrieve_asset("alien/yellow"))
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien(
                        200, x, y, self.game_assets.retrieve_asset("alien/green"))
                else:
                    alien_sprite = Alien(
                        100, x, y, self.game_assets.retrieve_asset("alien/red"))
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        # move the aliens right or left and then move them down and
        #   reverse direction if they hit the side walls.
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= self.screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        # shift aiens down "distance" pixels
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance
                if alien.rect.x >= self.screen_height + 20:
                    self.persist["lives"] = 0

    def alien_shoot(self):
        # shoot a laser from a random alien
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,
                                 6, self.screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        # create "Extra" alien every 400 800 frames (6.6 - 13.3 seconds)
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(
                ["right", "left"]), self.screen_width, self.game_assets.retrieve_asset("extra")))
            self.extra_spawn_time = randint(
                self.persist["espeed"][0], self.persist["espeed"][1])

    def collision_checks(self):
        # This procedures check for collisions between the lasers and either
        #   the aliens, the player, or the blocks.

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(
                    laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.persist["score"] += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    # The value of hitting the extra varies randomly between 500 and 1000
                    self.persist["score"] += choices(
                        [500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000], k=1)[0]
                    laser.kill()
                    self.explosion_sound.play()

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions with lasers
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # player collision with lasers
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.persist["lives"] -= 1
                    self.player.sprite.player_hit()

        # block or player collisions with aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                # collide with an alien, it's game over
                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.persist["lives"] = 0

    def display_lives(self):
        # If player gets hit and loses a life, the last life on the left flashed before
        #    going away.  I"m sure this could have been done better.
        if self.player.sprite.hit:
            for live in range(self.persist["lives"]):
                x = self.live_x_start_pos + \
                    (live * (self.live_surf.get_size()[0] + 10))
                self.live_surf = self.player.sprite.image_ok
                if self.player.sprite.hit and live == self.persist["lives"] - 1:
                    self.live_surf = choices(
                        [self.player.sprite.image_ok, self.player.sprite.image_hit], weights=(1, 1), k=1)[0]
                self.screen.blit(self.live_surf, (x, 8))
        else:
            for live in range(self.persist["lives"] - 1):
                self.live_surf = self.player.sprite.image_ok
                x = self.live_x_start_pos + \
                    (live * (self.live_surf.get_size()[0] + 10))
                self.screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        # display the score upper left of the screen
        score_surf = self.font.render(
            f"score: {self.persist['score']}", False, "white")
        score_rect = score_surf.get_rect(topleft=(10, 10))
        self.screen.blit(score_surf, score_rect)

    def victory_message(self):
        # if no more aliens, let the player know he won
        if not self.aliens.sprites():
            victory_surf = self.font.render("You won", False, "white")
            victory_rect = victory_surf.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2)
            )
            self.screen.blit(victory_surf, victory_rect)
            self.status = "win"
            self.end_game_pause()

    def loss_message(self):
        # if no more lives, then let the player know he lost
        if self.persist["lives"] <= 0:
            loss_surf = self.font.render("You lost", False, "white")
            loss_rect = loss_surf.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2)
            )
            self.screen.blit(loss_surf, loss_rect)
            self.status = "lose"
            self.end_game_pause()

    def end_game_pause(self):
        # win or lose, pause for 2.5 seconds (more or less)
        # This gives the game a chance to finish what it was
        # doing, otherwise end of game is a bit abrupt.
        if not self.game_over:
            self.game_over = True
            self.player.sprite.game_over = True
            pygame.time.set_timer(GAMEEND_EVENT, 3000, loops=1)

    def startup(self, persistent):
        # this is run every time a state is started
        # ie it's run on state change in "game.py"
        self.persist = persistent

        # Player setup
        player_sprite = Player(
            (self.screen_width / 2, self.screen_height),
            self.screen_width,
            self.persist["plspeed"],
            self.persist["pspeed"],
            self.game_assets)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.live_surf = self.player.sprite.image_ok

        self.status = "continue"
        # if lives is 0 then we lost the game and are starting over
        if self.persist["lives"] <= 0:
            self.persist["lives"] = 5
            self.persist["level"] = 1

        # I"m sure it"s useful somehow.
        self.game_over = False

        # max lives of 5 (display limit)
        self.live_x_start_pos = self.screen_rect.right - \
            (self.live_surf.get_size()[0] * (self.persist["lives"]) + 40)

        # self.font = pygame.font.Font("../font/Pixeled.ttf", 35)
        self.font = self.game_assets.retrieve_asset("sysfont50")

        # Obstacle setup
        self.shape = shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_number = 4
        self.obstacle_x_positions = [
            num * (self.screen_width / self.obstacle_number) for num in range(self.obstacle_number)]
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=(self.screen_width / 15), y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8, y_offset=100 +
                         (self.persist["level"] * 20))
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

        # Audio - volume settings are for comfort at my computer
        self.laser_sound = self.game_assets.retrieve_asset("pewpew")
        self.laser_sound.set_volume(self.persist['vpewpew']/100)
        self.explosion_sound = self.game_assets.retrieve_asset("boom")
        self.explosion_sound.set_volume(self.persist['vboom']/100)

        # set speed at which the aliens can shoot
        pygame.time.set_timer(ALIENLASER, self.persist["aspeed"])

    def get_event(self, event):
        self.player.sprite.get_event(event)
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == ALIENLASER and not self.game_over:
            self.alien_shoot()
        if event.type == GAMEEND_EVENT:
            self.done = True
            if self.status == "lose":
                self.next_state = "GAMEOVER"
            else:
                self.next_state = "GAMELEVEL"

    def update(self, dt):
        # if game over, stop shooting and let the game finish what
        #   it was doing when play ended.
        if self.game_over:
            self.player.sprite.game_over = True

        # Run updates on player, laser, aliens, etc.
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()
        self.aliens.update(self.alien_direction)

        # check for hitting the walls or collisions
        #   with lasers and stuff
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

    def draw(self, surface):
        self.screen.fill((30, 30, 30))

        # Draw all the pretty pieces, sprites, whatever
        self.player.sprite.lasers.draw(surface)
        self.player.draw(surface)
        self.blocks.draw(surface)
        self.aliens.draw(surface)
        self.alien_lasers.draw(surface)
        self.extra.draw(surface)

        # display lives, score, and win/loss screen when appropriate
        self.display_score()
        self.victory_message()
        self.loss_message()
        self.display_lives()

        pygame.display.update()
