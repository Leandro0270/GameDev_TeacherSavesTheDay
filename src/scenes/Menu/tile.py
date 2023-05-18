import pygame 
from Level1Settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,tileType):
		super().__init__(groups)
		self.tileType = tileType
		if(self.tileType == 'x'):
			self.image = pygame.image.load('wall.png')
		if(self.tileType == 'H'):
			self.image = pygame.image.load('horizontalWall.png')
		self.rect = self.image.get_rect(topleft = pos)