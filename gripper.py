#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
import Box2D
from Box2D import (b2Vec2, b2RayCastCallback, b2RayCastInput, b2RayCastOutput, b2_pi)
import math
import numpy as np
from vehicle import Vehicle


class Gripper:

	__ax = 0.5
	__l = 4.8
	__ls = 3
	__w = 2
	__ws = 0.5
	__s = 0.01
	__default__claw = [	[(-__ax,0), (-__w,__ws), (-__w,__l-__ls), (-__ax, __l), (-__w-__s,__l-__ls), (-__w-__s,__ws), (-__ax,0)],
						[(+__ax,0), (+__w,__ws), (+__w,__l-__ls), (+__ax, __l), (+__w-__s,__l-__ls), (+__w-__s,__ws), (+__ax,0)] ]


	def __init__(self, vehicle, claws=None,
			  position=(0,8.5), angle=0.0, density=0.01, friction=0.001):
		self.vehicle = vehicle
		self.b2bodies = []
		self.b2joints = []
		
		self.claws = claws
		if self.claws is None:
			self.claws = Gripper.__default__claw
		
		pos_t =  self.vehicle.b2body.transform * b2Vec2(position)
		angle_t = self.vehicle.b2body.angle + angle
		
		
		for vertices in self.claws:
			b = self.vehicle.world.b2world.CreateDynamicBody(position=pos_t, angle=angle_t)
			b.CreatePolygonFixture(vertices=vertices, density=density, friction=friction)

			j = self.vehicle.world.b2world.CreateRevoluteJoint( bodyA=vehicle.b2body,
															bodyB=b,
															localAnchorA=b2Vec2(position)+vertices[0],
															# center of tire
															localAnchorB=(0, 0),
															enableMotor=True,
															maxMotorTorque=1000,
															enableLimit=True,
															lowerAngle=-b2_pi*1/8,
															upperAngle=+b2_pi*1/8,
															collideConnected = True
															)

			j.frequencyHz = 0.0
			j.dampingRatio = 0.0

			self.b2bodies.append(b)
			self.b2joints.append(j)

			

	def step(self, fw):
		pass

		
	def draw(self, fw):
		for i, vertices in enumerate(self.claws):
			transform = self.b2bodies[i].transform
			vertices = [transform * v for v in vertices]
			fw.DrawPolygon( vertices, (255, 255, 255, 255))

			
	def open(self):
		self.b2joints[0].motorSpeed = +0.5
		self.b2joints[1].motorSpeed = -0.5

		
	def close(self):
		self.b2joints[0].motorSpeed = -0.5
		self.b2joints[1].motorSpeed = +0.5

	def get_angle(self):
		return (self.b2joints[1].angle)
	
	

		
