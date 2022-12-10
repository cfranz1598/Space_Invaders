import pygame


class Block(pygame.sprite.Sprite):
	def __init__(self, size, color, x, y):
		# create a building block of the barriers (see shape below)
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft=(x, y))

# Template shape for building the barriers
shape = [
	'  xxx xxx',
	' xxxxxxxxx',
	'xxxxxxxxxxx',
	'xxxxxxxxxxx',
	'xxxxxxxxxxx',
	'xxx     xxx',
	'xx       xx']
