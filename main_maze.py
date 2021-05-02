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
		
	
	def step(self, fw):
		super().step(fw)

		
		


if __name__ == "__main__":
	world = World()
	
	world.bodies.append( Maze(world) )
	world.bodies.append( MyRover( world, position=(+90,-50)) )
	world.bodies.append( Ball( world, position=(-30,-30)) )
	
	screen = Framework("MySim", world)
	screen.PPM = 3.5
	screen.run()
