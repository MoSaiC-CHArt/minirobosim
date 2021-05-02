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

class MyRover( Rover):
	def __init__(self, world, **vehicle_kws):
		super().__init__(world, **vehicle_kws)
		
	
	def step(self, fw):
		super().step(fw)
		
		# Perception
		#
		# on analyse le laser
		laser_data = np.array(self.laserscan.values)
				
		right  = laser_data[  :15].mean()
		center = laser_data[15:30].mean()
		left   = laser_data[30:  ].mean()
		
		fw.DrawText('left: ' + str(int(left*10)/10.0)
					+ ', center: ' + str(int(center*10)/10.0)
					+ ', right: ' + str(int(right*10)/10.0))
		
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

	world.bodies.append( MyRover( world, position=(0,0)) )
	world.bodies.append( KeyboardRover( world, position=(-50,20)) )

	screen = Framework("MySim", world)
	screen.run()
