#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from Box2D import b2
from Box2D import (b2CircleShape, b2FixtureDef, b2Vec2)
import numpy as np

class World():
	VEL_ITERS, POS_ITERS = 10, 10
	
	def __init__( self, gravity = (0,0)):
		self.b2world = b2.world()
		self.bodies = []
		self.b2world.gravity = gravity
		

	def step( self, fw):
		for body in self.bodies:
			body.step(fw)

		self.b2world.Step(fw.TIMESTEP, self.VEL_ITERS, self.POS_ITERS)
		self.b2world.ClearForces()
		

	def draw( self, fw):
		for body in self.bodies:
			body.draw(fw)


class Wall():
	__default_boundary = [(-70, -50),
							(-70, +50),
							(+70, +50),
							(+70, -50),
							(-70, -50)]
	
	def __init__(self, world, boundary = None):		
		self.world = world
		
		self.boundary = boundary
		if self.boundary is None:
			self.boundary = Wall.__default_boundary
		
		self.b2body = world.b2world.CreateStaticBody(position=(0, 20))
		self.b2body.CreateEdgeChain( self.boundary)
		

	def step(self, fw):
		pass

	def draw(self, fw):
		vertices = [self.b2body.transform * v for v in self.boundary]

		fw.DrawPolygon( vertices, (255, 255, 255, 255))


class Ball():
	def __init__(self, world, position = (0,0), radius = 1, density=0.01, friction=0.1):		
		self.world = world
		self.radius = radius
		
		
		self.b2body = world.b2world.CreateDynamicBody(
						fixtures=b2FixtureDef(
							shape=b2CircleShape(radius=self.radius),
							density=density),
						bullet=False,
						position=position) 
		

	def step(self, fw):
		pass

	def draw(self, fw):
		fw.DrawCircle( self.b2body.position, self.radius, (0, 255, 0, 255))
	

class Maze():
	__default_boundaries = [
					[(51,-50),(51,-9),(49,-9),(49,-50),(51,-50)],
					[(-11,-50),(-11,-29),(29,-29),(29,-9),(31,-9),(31,-31),(-9,-31),(-9,-50),(-11,-50)],
					[(-11,50),(-11,29),(11,29),(11,31),(-9,31),(-9,50),(-11,50)],
					[(-31,50),(-31,31),(-51,31),(-51,29),(-29,29),(-29,50),(-31,50)],
					[(-31,-50),(-31,-31),(-51,-31),(-51,-29),(-31,-29),(-31,-9),(-11,-9),(-11,9),(-49,9),(-49,-11),(-51,-11),(-51,11),(49,11),(49,29),(29,29),(29,31),(51,31),(51,9),(-9,9),(-9,-9),(11,-9),(11,-11),(-29,-11),(-29,-50) ],

					[(-70,-50),(-70,+50),(+70,+50),(+70,-50),(-70,-50)]
					]
	
	
	def __init__(self, world, boundaries = None):		
		self.world = world
		self.scale_ratio = 1.5

		
		self.boundaries = boundaries
		if self.boundaries is None:
			self.boundaries = Maze.__default_boundaries
		
		for w_i, wall in enumerate(self.boundaries):
			self.boundaries[w_i] = (np.array(wall)*self.scale_ratio).astype(int).tolist()
			
		self.start_line = [b2Vec2(self.boundaries[5][3])+b2Vec2([-19,+25])*self.scale_ratio,
							b2Vec2(self.boundaries[5][3])+b2Vec2([0,+25])*self.scale_ratio]
		self.end_line = [self.boundaries[4][5],
							b2Vec2(self.boundaries[4][5])+b2Vec2([0,17])*self.scale_ratio ]
		
		self.b2body = world.b2world.CreateStaticBody(position=(0, 20))
		for boundary in self.boundaries:
			self.b2body.CreateEdgeChain( boundary )		

	def step(self, fw):
		pass

	def draw(self, fw):
		transform = self.b2body.transform
		for boundary in self.boundaries:
			vertices = [transform * v for v in boundary]
			fw.DrawPolygon( vertices, (255, 255, 255, 255))
			

		vertices = [transform * v for v in self.start_line]
		fw.DrawPolygon( vertices, (0, 255, 128, 255))
		
		
		vertices = [transform * v for v in self.end_line]
		fw.DrawPolygon( vertices, (0, 255, 0, 255))


			