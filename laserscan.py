#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from Box2D import (b2Vec2, b2RayCastCallback, b2_pi)
import math
import numpy as np

"""
Laser based on:
https://ncase.me/sight-and-light/
"""
		
class Laser(b2RayCastCallback):
	
	def __init__(self, vehicle, position = (0,0), range = (1, 10), angle = 0.0, **kwargs):
		b2RayCastCallback.__init__(self, **kwargs)
		self.vehicle = vehicle
		self.position = position
		self.range = range
		self.angle = angle
		self.value = range[1]
		self.fixture = None
		self.hit = None
		self.hit_point = None
		self.normal = None



	def ReportFixture(self, fixture, point, normal, fraction):
		self.hit = True
		self.fixture = fixture
		self.hit_point = b2Vec2(point)
		self.normal = b2Vec2(normal)
		return fraction

	def get_emitter_pos(self):
		emitter_pos = b2Vec2(self.position)
		emitter_pos_t = self.vehicle.b2body.transform * emitter_pos
		return emitter_pos_t
		
	def get_ray(self):
		emitter_pos = b2Vec2(self.position)
		
		ray_p1 = emitter_pos + self.range[0] * b2Vec2( math.cos(self.angle), math.sin(self.angle)  )
		ray_p2 = emitter_pos + self.range[1] * b2Vec2( math.cos(self.angle), math.sin(self.angle)  )
		
		ray_p1_t = self.vehicle.b2body.transform * ray_p1
		ray_p2_t = self.vehicle.b2body.transform * ray_p2

		return (ray_p1_t, ray_p2_t)

	def step(self, fw):
		emitter_pos = self.get_emitter_pos()
		ray = self.get_ray()
		self.vehicle.world.b2world.RayCast(self, ray[0], ray[1])
		
		if self.hit:
			self.value = np.linalg.norm( self.hit_point - emitter_pos)
		else:
			self.value = self.range[1]
		
	def draw(self, fw):
		ray = self.get_ray()

		if self.hit:
			fw.DrawEdge( ray[0], self.hit_point, (128,128,255, 128) )
			fw.DrawCircle( self.hit_point, 0.5, (255,0,0,255) )
		else:
			fw.DrawEdge( ray[0], ray[1], (128,128,255, 128) )


class LaserScan():

	def __init__(self, vehicle, position = (0,5), range = (8,30), angle_range = (0, +b2_pi), n_sensors = 5 ):
		self.array = []
		self.values = []
		self.angles = np.linspace( angle_range[0], angle_range[1], n_sensors )
		self.n_sensors = 5

		for angle in self.angles:
			laser = Laser(vehicle, position, range, angle)
			self.array.append(laser)
			self.values.append(range[1])
			
	def step(self, fw):
		for idx, laser in enumerate(self.array):
			laser.hit = False
			laser.step(fw)
			self.values[idx] = laser.value

			
	def draw(self, fw, show_emitter = True):
		if(show_emitter):
			emitter_pos = self.array[0].get_emitter_pos()
			fw.DrawCircle( emitter_pos, 1.5, (0,0,255,255) )
		for laser in self.array:
			laser.draw(fw)
