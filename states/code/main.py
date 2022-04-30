'''
	This is, in fact, a decent version of the classic video game 'Space Invaders' from
	the video game in every American bar in the 70s and 80s.  This one is written in 
	Python using the pygame library.  It's not bad.  The only thing really missing is 
	that the aliens don't have the animation where their legs moved and the extra alien
	which flew across the top of the screen doesn't shoot lasers.  I didn't care
	enough to add those enhancements.  I did add code for 'levels' but not the looping.
	That would need to come with menus, ect.  Later.

	** Credit **
	Most of this was written by YouTube handle 'Clear Code':
		YouTube Tutorial: https://www.youtube.com/watch?v=o-6pADy5Mdg&t=3219s
		Clear Code on YouTube: https://www.youtube.com/channel/UCznj32AM2r98hZfTxrRo9bQ
		Original Respository: https://github.com/clear-code-projects/Space-invaders

	My additions are:
		1) Cleaning up the code to more or less PEP8 standards (I prefer tabs to spaces).
		2) Adding substantial comments to the code.
		3) It still only has one level but the infrastructure is there.
		4) Added both a you lose screen and a non-abrupt end of game.
		5) Added some effects when the player gets hit... He flashes red.
		6) There was something with the explosions or the laser sound effects which.
			needed help, but I'll be dipped if I can remember what.
		7) I think I fixed the lives display at the top of the screen.
		8) Changed RGB colors to the newer pygame color names.

	I also kind of removed the original pixelated font which, while more authentic, was
	really hard to read.  Code is there, put it back if you want.

	I was going to pull of the settings variables out and put them in a separate 'settings.py'
	file and fix some naming convensions, but I forgot.  That'll be a must when I add gaming
	menus to it, I suspect.

	This was rewritten and tested on Python 3.9.2 and pygame 2.1.2... So, if it doesn't
	work on your system that's entirely my fault.  Try the original.

	As per usual, any spelling or grammar mistakes are yours to keep.  Don't get them wet,
	don't feed them after midnight.  You've been warned.
'''

import pygame
import sys
from random import choices, choice, randint
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser


class Game:
    def __init__(self, level, lives, score, volumes):

        self.status = 'Continue'  # Win, Lose, Exit
        # Player setup
        player_sprite = Player(
            (screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.live_surf = self.player.sprite.image_ok

        # health and score setup
        self.game_over = False
        self.game_level = level
        # max lives of 5 (display limit)
        self.lives = lives if lives <= 5 else 5
        self.live_x_start_pos = screen_width - \
            (self.live_surf.get_size()[0] * (self.lives) + 40)
        self.score = score
        # self.font = pygame.font.Font('../font/Pixeled.ttf', 35)
        self.font = pygame.font.SysFont(None, 50)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_number = 4
        self.obstacle_x_positions = [
            num * (screen_width / self.obstacle_number) for num in range(self.obstacle_number)]
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=(screen_width / 15), y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8, y_offset=100 + (self.game_level * 20))
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

        # Audio - volume settings are for comfort at my computer
        music = pygame.mixer.Sound('../audio/music.wav')
        music.set_volume(volumes[0]/100)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(volumes[1]/100)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(volumes[2]/100)

    def create_obstacle(self, x_start, y_start, offset_x):
        # Build the obstacles.  They are made of 6x6 blocks so that
        # 	when lasers hit them they can disintegrate piece by piece.
        #   Clever solution to the problem.
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, 'firebrick3', x, y)
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
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        # move the aliens right or left and then move them down and
        #   reverse direction if they hit the side walls.
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        # shift aiens down 'distance' pixels
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        # shoot a laser from a random alien
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        # create 'Extra' alien every 400 800 frames (6.6 - 13.3 seconds)
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

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
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
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
                    self.lives -= 1
                    self.player.sprite.player_hit()

        # block or player collisions with aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.lives = 0

    def display_lives(self):
        # If player gets hit and loses a life, the last life on the left flashed before
        #    going away.  I'm sure this could have been done better.
        if self.player.sprite:
            for live in range(self.lives):
                x = self.live_x_start_pos + \
                    (live * (self.live_surf.get_size()[0] + 10))
                self.live_surf = self.player.sprite.image_ok
                if self.player.sprite.hit and live == self.lives - 1:
                    self.live_surf = choices(
                        [self.player.sprite.image_ok, self.player.sprite.image_hit], weights=(1, 1), k=1)[0]
                screen.blit(self.live_surf, (x, 8))
        else:
            for live in range(self.lives - 1):
                self.live_surf = self.player.sprite.image_ok
                x = self.live_x_start_pos + \
                    (live * (self.live_surf.get_size()[0] + 10))
                screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        # display the score upper left of the screen
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        # if no more aliens, let the player know he won
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won', False, 'white')
            victory_rect = victory_surf.get_rect(
                center=(screen_width / 2, screen_height / 2)
            )
            screen.blit(victory_surf, victory_rect)
            self.status = 'Win'
            self.end_game_pause()

    def loss_message(self):
        # if no more lives, then let the player know he lost
        if self.lives <= 0:
            loss_surf = self.font.render('You lost', False, 'white')
            loss_rect = loss_surf.get_rect(
                center=(screen_width / 2, screen_height / 2)
            )
            screen.blit(loss_surf, loss_rect)
            self.status = 'Lose'
            self.end_game_pause()

    def end_game_pause(self):
        # win or lose, pause for 2.5 seconds (more or less)
        # This gives the game a chance to finish what it was
        # doing, otherwise end of game is a bit abrupt.
        if not self.game_over:
            self.game_over = True
            pygame.time.set_timer(GAMEEND_EVENT, 2500, loops=1)

    def run(self):
        # if game over, stop shooting and let the game finish what
        #   it was doing when play ended.
        if self.game_over:
            self.player.sprite.ready = False

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

        # Draw all the pretty pieces, sprites, whatever
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)

        # display lives, score, and win/loss screen when appropriate
        self.display_lives()
        self.display_score()
        self.victory_message()
        self.loss_message()

        # if self.status == 'Lose': return ('lose', self.level, self.lives, self.score, (7,10,20))
        # if self.status == 'Win':  return ('win', self.level, self.lives, self.score, (7,10,20))
        # if self.status == 'Exit': return ('exit', self.level, self.lives, self.score, (7,10,20))


class CRT:
    # Makes the screen look like the old pixelated video screen.
    # However, this chews up so much CPU it slows down the game
    # significantly and should only be used on higher end CPUs.
    def __init__(self):
        self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(
            self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos),
                             (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game(1, 5, 0, (7, 10, 20))  # level, lives, score, volumes
    # crt = CRT()  # Don't use unless you have a fast CPU

    # set speed at which the aliens can shoot
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 900)

    # give a pause at the end of the game
    # see also: Game.end_game_pause()
    GAMEEND_EVENT = pygame.USEREVENT + 2

    while True:
        # This is the main game loop, however, most of the user input is
        #   handled by the various game objects, specifically,
        #   Player.get_input().
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.end_game_pause()  # creates timer for GAMEEND_EVENT event
            if event.type == GAMEEND_EVENT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER and not game.game_over:
                game.alien_shoot()

        # a dark gray screen to 'paint' on
        screen.fill(('black'))

        # calls all the other process needed to run the game
        game.run()
        # when uncommentd it causes the game display to have lines that make
        #  it look like an old CRT screen.  Also the old style rounded
        #  edges.  However, it chews up a lot of CPU processing for each frame.
        #  Clever really, but kills game performance.
        # crt.draw()

        # move the updated surfaces to the screen
        pygame.display.flip()
        clock.tick(60)
