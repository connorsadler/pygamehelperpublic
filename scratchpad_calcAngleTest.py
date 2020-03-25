
import math
import pygamehelper
from pygamehelper import *

#
# This is the version of the code internal to this test that I can play around with
# The findings from this have now gone into calcAngle in pygamehelper.py
# TODO: Maybe turn this into a unit test using the Python JUnit equivalent
#

# #
# # opposite of resolveAngle - get a dx and dy value and find the angle that this direction represents
# # returns an angle in degress
# def calcAngleINTERNAL(dx, dy):
#     if dx == 0:
#         dx = 0.0000001
#     if dy == 0:
#         dy = 0.0000001
#     newAngle = round( math.degrees( round( math.atan(dy/dx), 10) ), 3)

#     # part adapted from here: https://stackoverflow.com/questions/6247153/angle-from-2d-unit-vector
#     if dx < 0 and dy < 0: # quadrant 3
#         newAngle = 180 + newAngle
#     elif dx < 0: # quadrant 2
#         newAngle = 180 + newAngle # it actually substracts
#     elif dy < 0: # quadrant 4
#         newAngle = 270 + (90 + newAngle) # it actually substracts

#     # current angle is CLOCKWISE from East
#     # we wish it to be CLOCKWISE from North
#     newAngle = newAngle + 90
#     if newAngle >= 360:
#         newAngle -= 360
        
#     return newAngle

def doCalcAndShow(dx, dy):
    #newAngle = calcAngleINTERNAL(dx, dy)
    newAngle = calcAngle(dx, dy)
    print("dx, dy: " + str(dx) + ", " + str(dy) + "  -> " + str(newAngle))

doCalcAndShow(0,-1)     # North

doCalcAndShow(1,-6)
doCalcAndShow(1,-1)
doCalcAndShow(3,-1)
doCalcAndShow(6,-1)

doCalcAndShow(1,0)     # East

doCalcAndShow(6,1)
doCalcAndShow(3,1)
doCalcAndShow(1,1)
doCalcAndShow(1,6)

doCalcAndShow(0,1)    # South

doCalcAndShow(-1,6)
doCalcAndShow(-1,1)
doCalcAndShow(-3,1)

doCalcAndShow(-1,0)    # West

doCalcAndShow(-3,-1)
doCalcAndShow(-1,-1)
doCalcAndShow(-1,-6)

doCalcAndShow(0,-1)     # North again