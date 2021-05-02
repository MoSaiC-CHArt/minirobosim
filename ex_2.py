#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from IO import Framework, Keys
from world import World, Wall, Ball
from vehicle import Vehicle
from platforms import *
import numpy as np
import matplotlib.pyplot as plt

class MyRover( KeyboardRover):
	def __init__(self, world, **vehicle_kws):
		super().__init__(world, **vehicle_kws)
		
		plt.ion()
		
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
		self.laser_angles = np.linspace(np.pi/2,-np.pi/2,len(self.laserscan.values))
		self.line1, = self.ax.plot(self.laser_angles, self.laserscan.values, 'r-') 
		self.ax.set_ylim(0,50)
	
	
	def step(self, fw):
		super().step(fw)


	def draw(self, fw):
		super().draw(fw)
		
		self.line1.set_ydata( self.laserscan.values)
		self.ax.draw_artist(self.line1)
		self.fig.canvas.blit(self.ax.bbox)


if __name__ == "__main__":
	world = World()
	world.bodies.append( Wall( world) )	
	world.bodies.append( Wall( world, boundary=[(-30,-30), (-30,+20), (-20,+20), (-20,-30), (-30,-30)] ) )	
	world.bodies.append( Wall( world, boundary=[(+30,+30), (+30,-20), (+20,-20), (+20,+30), (+30,+30)] ) )
	world.bodies.append( Ball( world, position=(10,0)) )

	world.bodies.append( MyRover( world, position=(-50,20)) )

	screen = Framework("MySim", world)
	screen.run()
