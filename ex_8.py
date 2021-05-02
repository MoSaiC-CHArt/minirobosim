#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from IO import Framework, Keys
from world import World, Wall, Ball, Maze
from platforms import *
import numpy as np
import pandas as pd

class MyRover( Rover):
	def __init__(self, world, **vehicle_kws):
		super().__init__(world, **vehicle_kws)

		self.laser_angles = np.linspace(-np.pi/2,+np.pi/2,len(self.laserscan.values))
		# on crée une memoire des lasers à court terme		
		self.laser_data = pd.DataFrame(columns = self.laser_angles)
		self.max_laser_data = 30

		# on ouvre le gripper
		self.gripper.open()
		
	
	def step(self, fw):
		super().step(fw)
		
		# Perception
		#
		# on analyse le laser et on crée une mémoire
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
			ball_features = np.diff( center_data.median() ) > 4
			ball_seen  = np.any(ball_features)
			if ball_seen:
				ball_lasers_idx = np.where( ball_features)
				ball_idx = int(np.median(ball_lasers_idx))
				ball_angle = self.laser_angles[15+ball_idx]
				ball_dist = center_data.median()[ball_angle]
				ball_model = (ball_dist, ball_angle)
				
		# si le capteur de proximité à l'avant capte qu'il y a un objet dans le gripper..
		object_caught = self.front_ir.values[1] < 5.5

		info_string = ''
		info_string = info_string + 'left: ' + str(int(left*10)/10.0)
		info_string = info_string +	', center: ' + str(int(center*10)/10.0)
		info_string = info_string + ', right: ' + str(int(right*10)/10.0)
		info_string = info_string +', ball_seen: ' + str(ball_seen)
		if ball_seen:
			info_string = info_string + ', ( ' + str(ball_model[0]) + ')'
			info_string = info_string + ', ( ' + str(ball_model[1]) + ')'
		if object_caught:
			info_string = info_string + ', object caught' 
			
		fw.DrawText( info_string)
		
		
		# Decision
		# motor_control = [ vitesse linéaire (positif est vers l'avant),
		#					vitesse angulaire (positif est anti-horaire) ]
		#	
		# default behavior: go forward
		motor_control = (+5, 0) 				
		# obstacle à l'avant, gauche libre: tourner à gauche
		if left > center:
			motor_control = (+5, +5)
		# obstacle à l'avant, droite libre: tourner à droite
		elif right > center:
			motor_control = (+5, -5)
		# sinon, si l'obstacle est trop proche de nous, on recule
		if max( left, center, right) < 20:
			motor_control = (-10, 5*np.random.randn()) # on ajoute un peu de bruit pour tourner un peu

		# si le gripper est vide et on perçoit une balle
		if not object_caught and ball_seen:
			self.gripper.open() # on ouvre le gripper
			ball_angle = ball_model[1]
			motor_control = (+5, 5*ball_angle) # on se dirige vers la balle
		else: # autrement, s'il y a un objet dans le gripper, on le ferme
			if object_caught:
				self.gripper.close()	

		# on verifie aussi les capteurs de proximité
		# capteurs à l'avant
		if self.front_ir.values[0] < 6:
			motor_control = (motor_control[0],-10)
		if self.front_ir.values[2] < 6:
			motor_control = (motor_control[0],+10)
		# capteurs à l'arriere
		if self.rear_ir.values[0] < 6:
			motor_control = (motor_control[0],+10)
		if self.rear_ir.values[2] < 6:
			motor_control = (motor_control[0],-10)
		if self.rear_ir.values[1] < 6:
			motor_control = (10,0)
		# ..on utilisera le capteur positionné au centre en avant du rover
		# pour vérifier si on a quelque chose dans le gripper..
		
		
		# Action
		#
		# controle des moteurs
		# on convert les vitesses (linéaire et angulaire) vers les vitesses des deux roues
		v_l = motor_control[0] - motor_control[1]/2
		v_r = motor_control[0] + motor_control[1]/2
		self.tires[0].update_drive( v_l ) # roue gauche		
		self.tires[1].update_drive( v_r )	# roue droite
		
		


if __name__ == "__main__":
	world = World()
	
	world.bodies.append( Wall( world) )	
	world.bodies.append( Wall( world, boundary=[(-30,-30), (-30,+20), (-20,+20), (-20,-30), (-30,-30)] ) )	
	world.bodies.append( Wall( world, boundary=[(+30,+30), (+30,-20), (+20,-20), (+20,+30), (+30,+30)] ) )
	world.bodies.append( Ball( world, position=(10,0)) )

	world.bodies.append( MyRover( world, position=(-50,20), angle=0.0) )
	
	screen = Framework("MySim", world)
	screen.run()
