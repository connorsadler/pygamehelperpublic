import pygamehelper
from pygamehelper import *

#
# Draw circle
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
class CircleDrawer(Sprite):
    def __init__(self):
        super().__init__(getScreenRect().centerx, getScreenRect().centery, 20, 20)
        self.points = []
        self.lineAngle = 0

    def move(self):
        if self.lineAngle < 360:
            # add a new point around the circle, at lineAngle
            newPoint = angleToVector(self.lineAngle, 100)
            self.points.append(newPoint)
            # move new point around the circle so the next point is drawn in the next location round the circle
            self.lineAngle += 1
        else:
            # move the entire set of points down the screen
            self.moveBy(1,1)


    def draw(self):
        # Draw all points on each frame
        for point in self.points:
            # Each point is on a circle with centre 0,0 - so to draw relative to our sprite, we adjust the point by our sprite's x,y coords
            newPoint = addVectors(point, self.getLocation())
            drawPoint(newPoint, white)

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
        # Create a couple of boxes which will bounce around
        pygamehelper.addSprite(CircleDrawer())

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

# Run game loop
MyGameLoop().runGameLoop()
