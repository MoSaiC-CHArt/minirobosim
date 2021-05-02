#!/usr/bin/env python
# -*- coding: utf-8 -*-	
"""
@author: Salvatore Anzalone
@organization: CHArt - Université Paris 8
"""
from IO import Keys
from vehicle import Vehicle
from laserscan import LaserScan
from gripper import Gripper
from Box2D import b2_pi
	

class KeyboardVehicle(Vehicle):
	def __init__( self, world, **vehicle_kws):
		super().__init__( world, **vehicle_kws)
				
	def step(self, fw):
		super().step(fw)

		# check keys
		if Keys.K_UP in fw.pressed_keys:
			for tire in self.tires[0:2]:
				tire.update_drive(tire.max_forward_speed)				
				
		if Keys.K_DOWN in fw.pressed_keys:
			for tire in self.tires[0:2]:
				tire.update_drive(tire.max_backward_speed)
				
		# rear wheels steering control
		if Keys.K_LEFT in fw.pressed_keys:
			self.tires[1].update_drive(self.tires[1].max_forward_speed/2.0)
		if Keys.K_RIGHT in fw.pressed_keys:
			self.tires[0].update_drive(self.tires[0].max_forward_speed/2.0)


class LaserScanVehicle(Vehicle):
	laserscan = None
	
	def __init__( self, world, show_profile=False, **vehicle_kws,):
		super().__init__( world, **vehicle_kws)
		
		self.laserscan = LaserScan(self, n_sensors = 45)
		
	def step(self, fw):
		super().step(fw)
		self.laserscan.step(fw)

	def draw(self, fw):
		super().draw(fw)
		self.laserscan.draw(fw)


class LaserKeyboardVehicle( LaserScanVehicle, KeyboardVehicle):
	def __init__( self, world, show_profile=False, **vehicle_kws,):
		super().__init__( world, show_profile, **vehicle_kws)


class GripperVehicle(Vehicle):
	gripper = None
	
	def __init__( self, world, **vehicle_kws):
		super().__init__(world, **vehicle_kws)
		self.gripper = Gripper(self)
		
	def step(self, fw):
		super().step(fw)
		self.gripper.step(fw)

	def draw(self, fw):
		super().draw(fw)
		self.gripper.draw(fw)


class GripperKeyboardVehicle( GripperVehicle, KeyboardVehicle):
	def __init__( self, world, **vehicle_kws,):
		super().__init__( world, **vehicle_kws)
		
	def step(self, fw):
		super().step(fw)

		if Keys.K_o in fw.pressed_keys:
			self.gripper.open()

		if Keys.K_c in fw.pressed_keys:
			self.gripper.close()


class irVehicle( Vehicle):
	frontal_ir = None
	rear_ir = None
	def __init__( self, world, **vehicle_kws,):
		super().__init__( world, **vehicle_kws)
		self.front_ir = LaserScan(self, position=(0,6),
											range = (3,6),
											angle_range = (1/4*b2_pi, 3/4*b2_pi),
											n_sensors = 3)

		self.rear_ir = LaserScan(self, position=(0,2.6),
										range = (3,6),
										angle_range = (5/4*b2_pi, 7/4*b2_pi),
										n_sensors = 3)

	def step(self, fw):
		super().step(fw)
		self.front_ir.step(fw)
		self.rear_ir.step(fw)
		
	def draw(self, fw):
		self.front_ir.draw(fw, False)
		self.rear_ir.draw(fw, False)
		super().draw(fw)


class irKeyboardVehicle( irVehicle, KeyboardVehicle):
	def __init__( self, world, **vehicle_kws,):
		super().__init__( world, **vehicle_kws)
		
	
class Rover( LaserScanVehicle, GripperVehicle, irVehicle ):
	def __init__( self, world, **vehicle_kws,):
		super().__init__( world, **vehicle_kws)
		

class KeyboardRover( LaserKeyboardVehicle, GripperKeyboardVehicle, irKeyboardVehicle ):
	def __init__( self, world, show_profile=False, **vehicle_kws,):
		super().__init__( world, **vehicle_kws)


