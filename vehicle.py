#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from Box2D import b2
from Box2D import (b2Body, b2World, b2Vec2)
import numpy as np

"""
Vehicle based on Chris Campbell's tutorial from iforce2d.net:
http://www.iforce2d.net/b2dtut/top-down-car
"""
class Tire():

	def __init__(self, car, max_forward_speed=50.0,
				 max_backward_speed=-25, max_drive_force=150,
				 turn_torque=15, max_lateral_impulse=3,
				 dimensions=(0.5, 1.25), density=1.0,
				 position=(0, 0), angle=0.0):

		world = car.b2body.world

		self.current_traction = 1
		self.turn_torque = turn_torque
		self.max_forward_speed = max_forward_speed
		self.max_backward_speed = max_backward_speed
		self.max_drive_force = max_drive_force
		self.max_lateral_impulse = max_lateral_impulse
		self.ground_areas = []

		self.body = world.CreateDynamicBody(position=position, angle=angle)
		self.body.CreatePolygonFixture(box=dimensions, density=density)
		self.body.userData = {'obj': self}

	@property
	def forward_velocity(self):
		body = self.body
		current_normal = body.GetWorldVector((0, 1))
		return current_normal.dot(body.linearVelocity) * current_normal

	@property
	def lateral_velocity(self):
		body = self.body

		right_normal = body.GetWorldVector((1, 0))
		return right_normal.dot(body.linearVelocity) * right_normal

	def update_friction(self):
		impulse = -self.lateral_velocity * self.body.mass
		if impulse.length > self.max_lateral_impulse:
			impulse *= self.max_lateral_impulse / impulse.length

		self.body.ApplyLinearImpulse(self.current_traction * impulse,
									 self.body.worldCenter, True)

		aimp = 0.1 * self.current_traction * \
			self.body.inertia * -self.body.angularVelocity
		self.body.ApplyAngularImpulse(aimp, True)

		current_forward_normal = self.forward_velocity
		current_forward_speed = current_forward_normal.Normalize()

		drag_force_magnitude = -2 * current_forward_speed
		self.body.ApplyForce(self.current_traction * drag_force_magnitude * current_forward_normal,
							 self.body.worldCenter, True)

	def update_drive(self, desired_speed):
		# find the current speed in the forward direction
		current_forward_normal = self.body.GetWorldVector((0, 1))
		current_speed = self.forward_velocity.dot(current_forward_normal)

		# apply necessary force
		force = 0.0
		if desired_speed > current_speed:
			force = self.max_drive_force
		elif desired_speed < current_speed:
			force = -self.max_drive_force
		else:
			return

		self.body.ApplyForce(self.current_traction * force * current_forward_normal,
							 self.body.worldCenter, True)


class Vehicle():
	__default_vertices = [(1.5, 0.0),
				(3.0, 2.5),
				(2.8, 5.5),
				(1.0, 9.0),
				(-1.0, 9.0),
				(-2.8, 5.5),
				(-3.0, 2.5),
				(-1.5, 0.0),
				]

	__default_tires_anchors = [
					(-4., 3.5),
					(+4., 3.5)
					]

	def __init__(self, world, vertices=None,
				 tires_anchors=None, density=1, position=(0, 0), angle=0.0,
				 **tire_kws):
		
		self.vertices = vertices
		if self.vertices is None:
			self.vertices = Vehicle.__default_vertices
		self.world = world

		self.b2body = world.b2world.CreateDynamicBody(position=position, angle=angle)
		self.b2body.CreatePolygonFixture(vertices=self.vertices, density=density)
		self.b2body.userData = {'obj': self}

		self.tires_anchors = tires_anchors
		if self.tires_anchors is None:
			self.tires_anchors = Vehicle.__default_tires_anchors

		self.tires = [Tire(self,
							 position=self.b2body.transform * self.tires_anchors[i],
							 angle=angle,
							 **tire_kws) for i in range(len(self.tires_anchors))]


		joints = self.joints = []
		for tire, anchor in zip(self.tires, self.tires_anchors):
			j = world.b2world.CreateRevoluteJoint(bodyA=self.b2body,
										  bodyB=tire.body,
										  localAnchorA=anchor,
										  # center of tire
										  localAnchorB=(0, 0),
										  enableMotor=False,
										  maxMotorTorque=1000,
										  enableLimit=True,
										  lowerAngle=0,
										  upperAngle=0,
										  )


			joints.append(j)
			
	def step(self, fw):
		for tire in self.tires:
			tire.update_friction()
			

	def draw(self, fw):
		transform = self.b2body.transform
		vertices = [transform * v for v in self.vertices]

		fw.DrawPolygon( vertices, (255, 255, 255, 255))
		
		for tire in self.tires:
			for fixture in tire.body.fixtures:
				transform = tire.body.transform
				vertices = [transform * v for v in fixture.shape.vertices]
				fw.DrawPolygon( vertices, (255, 255, 255, 255))


				
