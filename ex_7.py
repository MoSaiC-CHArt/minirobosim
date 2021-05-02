#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from IO import Framework, Keys
from world import World, Wall, Ball
from platforms import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MyRover( KeyboardRover):
	def __init__(self, world, **vehicle_kws):
		super().__init__(world, **vehicle_kws)
		
		self.laser_angles = np.linspace(-np.pi/2,+np.pi/2,len(self.laserscan.values))
		# on crée une memoire à court terme
		self.laser_data = pd.DataFrame(columns = self.laser_angles)
		self.max_laser_data = 30
		
		plt.ion()
		
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
		self.line1, = self.ax.plot(self.laser_angles, self.laserscan.values, 'r-') 
		self.ax.set_ylim(0,50)
		
		self.gripper.open()
	
	
	def step(self, fw):
		super().step(fw)
		
		# on ajoute les nouvelles perceptions
		self.laser_data.loc[fw.time] = self.laserscan.values
		# on garde juste le N dernieres perceptions
		if(len(self.laser_data) > self.max_laser_data):
			self.laser_data.drop( self.laser_data.index[0], inplace=True)

		right_data = self.laser_data[self.laser_angles[  :15]]
		center_data = self.laser_data[self.laser_angles[15:30]]
		left_data = self.laser_data[self.laser_angles[30:  ]]

		right  = right_data.mean().mean()
		center = center_data.mean().mean()
		left   = left_data.mean().mean()
				
		# si le tableau est plein,
		# on utilise les lectures laser pour vérifier la presence de la balle
		ball_seen  = False
		ball_model = None
		if(len(self.laser_data) == self.max_laser_data):
			ball_features = np.diff( center_data.median() ) > 2
			ball_seen  = np.any(ball_features)
			if ball_seen:
				ball_lasers_idx = np.where( ball_features)
				ball_idx = int(np.median(ball_lasers_idx))
				ball_angle = self.laser_angles[15+ball_idx]
				ball_dist = center_data.median()[ball_angle]
				ball_model = (ball_dist, ball_angle)

		info_string = ''
		info_string = info_string + 'left: ' + str(int(left*10)/10.0)
		info_string = info_string +	', center: ' + str(int(center*10)/10.0)
		info_string = info_string + ', right: ' + str(int(right*10)/10.0)
		info_string = info_string +', ball_seen: ' + str(ball_seen)
		if ball_seen:
			info_string = info_string + ', ( ' + str(ball_model[0]) + ')'
			info_string = info_string + ', ( ' + str(ball_model[1]) + ')'
		fw.DrawText( info_string)



	def draw(self, fw):
		super().draw(fw)
		
		self.line1.set_ydata( self.laserscan.values )
		self.ax.draw_artist(self.line1)
		self.fig.canvas.blit(self.ax.bbox)
		
		


if __name__ == "__main__":
	world = World()
	world.bodies.append( Wall( world) )	
	world.bodies.append( Wall( world, boundary=[(-30,-30), (-30,+20), (-20,+20), (-20,-30), (-30,-30)] ) )	
	world.bodies.append( Wall( world, boundary=[(+30,+30), (+30,-20), (+20,-20), (+20,+30), (+30,+30)] ) )
	world.bodies.append( Ball( world, position=(10,0)) )

	world.bodies.append( MyRover( world, position=(0,60), angle=-np.pi) )

	screen = Framework("MySim", world)
	screen.run()
