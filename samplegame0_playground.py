import pygamehelper
from pygamehelper import *

#
# Playground
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# TODO
# 
class LineDrawer(Sprite):
    def __init__(self, functionFromXCoordToYCoord):
        super().__init__(30, getScreenRect().centery, 20, 20)
        self.points = []
        self.lineAngle = 0
        self.xcoord = 0
        self.functionFromXCoordToYCoord = functionFromXCoordToYCoord

    def move(self):
        ycoord = self.functionFromXCoordToYCoord(self.xcoord)
        self.xcoord += 1
        self.points.append((self.xcoord, ycoord))

    def draw(self):
        # Draw axes
        drawLine((self.x - 1000,self.y),(self.x + 1000,self.y), white)
        drawLine((self.x,self.y - 1000),(self.x, self.y + 1000), white)

        # Draw all points on each frame
        for point in self.points:
            pointFlipped = flipYCoord(point)
            pointScreen = addVectors((self.x, self.y), pointFlipped)
            drawPoint(pointScreen, white)


def functionFromXCoordToYCoord(x):
    y = x * x * 0.01
    return y

#
# Game loop logic
#
class MyGameLoop(GameLoop):

    def __init__(self):
        super().__init__()
        #
        # TODO
        # Create any initial instances of your sprites here
        #
        pygamehelper.addSprite(LineDrawer(functionFromXCoordToYCoord))

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

# Run game loop
MyGameLoop().runGameLoop()
