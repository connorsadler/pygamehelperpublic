
#from pygamehelper import *
#import pygamehelper as pygamehelper
from pygamehelper import *
import pygamehelper as pygamehelper

print("Testing calling imported function without import qualifier")
initPygame()

print("Testing using imported color: " + str(red))

# This NEVER works
print("Testing using imported gameDisplay variable (no qualifier): " + str(gameDisplay))
# This always works - it needs the module prefix
print("Testing using imported gameDisplay variable (with qualifier): " + str(pygamehelper.gameDisplay))