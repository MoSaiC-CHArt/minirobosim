#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from IO import Framework, Keys
from world import World, Wall, Ball
from vehicle import Vehicle

class MyVehicle(Vehicle):
	def __init__(self, world, **vehicle_kws):
		super().__init__(world, **vehicle_kws)
		
		self.last_control = None
		self.last_control_time = None
		
		self.states = [	# control, time, next_state
						( (10,10), 1.5, 1),
						( (14,2), 1, 0)
						#,
						#( (10,10), 1.5, 3),
						#( (2,14), 1, 0)
						]
		self.current_state = None

	def step(self, fw):
		super().step(fw)
		
		if not self.last_control:
			self.current_state = 0
			self.last_control = self.states[self.current_state][0] # <- 0: control
			self.last_control_time = fw.time
			
		if (fw.time - self.last_control_time) > self.states[self.current_state][1]: # <- 1: time
			#self.current_state = (self.current_state +1) % len(self.states)
			self.current_state = self.states[self.current_state][2] # <- 2: next state
			self.last_control = self.states[self.current_state][0] # <- 0: control
			self.last_control_time = fw.time

		self.tires[0].update_drive( self.last_control[0])				
		self.tires[1].update_drive( self.last_control[1])


if __name__ == "__main__":
	world = World()
	world.bodies.append( Wall( world) )
	world.bodies.append( MyVehicle( world) )
	
	screen = Framework("MySim", world)
	screen.run()
