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
		self.laser_angles = np.linspace(-np.pi/2,+np.pi/2,len(self.laserscan.values))
		self.line1, = self.ax.plot(self.laser_angles, self.laserscan.values, 'r-') 
		self.ax.set_ylim(0,50)
	
	
	def step(self, fw):
		super().step(fw)
		
		laser_data = np.array(self.laserscan.values)

		right_angles = self.laser_angles[:15]
		print('r', right_angles)
		central_angles = self.laser_angles[15:30]
		print('c', central_angles)
		left_angles = self.laser_angles[30:]
		print('l', left_angles)
		

		right  = laser_data[  :15].mean()
		center = laser_data[15:30].mean()
		left   = laser_data[30:  ].mean()

		
		fw.DrawText('left: ' + str(int(left*10)/10.0)
					+ ', center: ' + str(int(center*10)/10.0)
					+ ', right: ' + str(int(right*10)/10.0))


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

	world.bodies.append( MyRover( world, position=(-50,20)) )

	screen = Framework("MySim", world)
	screen.run()
