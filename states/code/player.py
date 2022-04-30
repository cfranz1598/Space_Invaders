import pygame
from laser import Laser
from random import choices


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, constraint, speed):
		super().__init__()

		# Get player image and hit image
		self.image = pygame.image.load(
			'../graphics/player_ok.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=pos)
		self.image_ok = self.image
		self.image_hit = pygame.image.load(
			'../graphics/player_hit.png').convert_alpha()

		# set player movement parameters
		self.speed = speed
		self.max_x_constraint = constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 400

		# set up player hit animation
		self.hit = False
		self.hit_animation = 0.15
		self.hit_limit = 15
		self.hit_limit_count = 0

		# Laser setup
		self.lasers = pygame.sprite.Group()
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)

	def get_input(self):
		keys = pygame.key.get_pressed()

		# player can only gor right or left
		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		#  Player shoots at the aliens, there is a pause between shots
		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			# This initiates the 'recharge' period for the players shots
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	def recharge(self):
		# after firing the laser it takes a moment or two to 'recharge'
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		# stops player from leaving the screen
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint

	def shoot_laser(self):
		# 'Fires' the laser from the center of the Player
		self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

	def player_hit(self):
		# Signals to the maneline game that the player has been
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
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()
