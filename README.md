# MiniRoboSim
Minimal 2D robot simulator based on Box2D library

## Dependencies
  -   PyGame : https://github.com/pygame/pygame
  -   PyBox2D : https://github.com/pybox2d/pybox2d
Compatible with Python 3.11.7, PyGame 2.2.0 (SDL 2.28.5), PyBox2D 2.3.8

## Example of usage with Conda environment:
_Environment creation_ \
 (base) $ conda create -n myrobotenv python=3.11 pygame=2.2 pybox2d=2.3 numpy pandas matplotlib

_Environment activation_ \
 (base) $ conda activate myrobotenv

_Starting the exemple n. 2_ \
 (myrobotenv) $ python ex_2.py

_Reverting to the base environment_ \
 (myrobotenv) $ conda deactivate \
 (base) $
