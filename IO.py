#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
import pygame
from pygame.locals import (QUIT, KEYDOWN, KEYUP)
import numpy as np


class Keys():
	pass

keys = [s for s in dir(pygame.locals) if s.startswith('K_')]
for key in keys:
	value = getattr(pygame.locals, key)
	setattr(Keys, key, value)
#print(keys)


class Framework():

	TARGET_FPS = 60
	PPM = 5.0 # vs 10.0
	TIMESTEP = 1.0 / TARGET_FPS
	VEL_ITERS, POS_ITERS = 10, 10
	SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
	SCREEN_OFFSETX, SCREEN_OFFSETY = SCREEN_WIDTH * 1.0 / 2.0, SCREEN_HEIGHT * 2.0 / 3
		
	name = 'None'
	description = ''
	caption = ''
	running = False
	description = ''
	
	world = None
	start_time = None
	time = None
	fps = 0.0

	def __init__( self, name, world, description = ''):
		self.name = name
		self.description = description

		# Pygame Initialization
		print('Initializing pygame framework...')
		pygame.init()
		
		self.caption = "Simple Simulation - " + self.name
		pygame.display.set_caption(self.caption)

		# Screen and debug draw
		self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
		self.font = pygame.font.Font(None, 15)

		# Keep track of the pressed keys
		self.pressed_keys = set()
		
		# Link the screen to a world
		self.world = world
		
		
	def run( self):
		if not self.running: self.start_time = pygame.time.get_ticks()

		self.running = True
		clock = pygame.time.Clock()
		
		while self.running:
			self.time = (pygame.time.get_ticks() - self.start_time) * 0.001

			# Check for keyboard events
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == Keys.K_ESCAPE):
					self.running = False
				elif event.type == KEYDOWN:
					self.Keyboard(event.key)
				elif event.type == KEYUP:
					self.KeyboardUp(event.key)
					
			# Initialise drawing surface
			self.screen.fill((0, 0, 0))
			self.textLine = 15

			# Draw the name
			self.DrawText(self.name, (127, 127, 255))
			#self.DrawText(str(self.fps), (127, 127, 255))

			# Draw a description
			if self.description:
				for s in self.description.split('\n'):
					self.DrawText(s, (127, 255, 127))
					
			# Run the world, step by step...
			if self.world:
				self.world.step(self)
				self.world.draw(self)
				
			# Updating drawing surface
			pygame.display.flip()
			clock.tick(self.TARGET_FPS)
			self.fps = clock.get_fps()

					
		# Destroy the world...
		if self.world:
			self.world.contactListener = None
			self.world.destructionListener = None
			self.world.renderer = None

			
			
	# Keyboard events
	def Keyboard(self, key):
		self.pressed_keys.add(key)

	def KeyboardUp(self, key):
		self.pressed_keys.remove(key)
		
	# Drawing primitives
	def DrawText(self, str, color=(229, 153, 153, 255)):
		self.screen.blit(self.font.render( str, True, color), (5, self.textLine))
		self.textLine += 15
		
	def fix_vertices(self, vertices):
		return [(int(self.SCREEN_OFFSETX + v[0]), int(self.SCREEN_OFFSETY - v[1])) for v in vertices]

	def DrawPolygon(self, vertices, color):
		vertices = self.fix_vertices([np.array(v) * self.PPM for v in vertices])
		pygame.draw.polygon(self.screen, color, vertices, 1)

	def DrawCircle(self, position, radius, color):
		position = self.fix_vertices([np.array(position) * self.PPM])[0]
		pygame.draw.circle(self.screen, color, position, int(radius * self.PPM))

	def DrawEdge(self, vertex1, vertex2, color):
		vertices = self.fix_vertices([np.array(vertex1) * self.PPM, np.array(vertex2) * self.PPM])
		pygame.draw.line(self.screen, color, vertices[0], vertices[1])






