import pygamehelper
from pygamehelper import *

#
# Path following
# - setups up a Path - a list of points
# - draws that path as lines using PathDrawer sprite
# - follows that path using a sprite
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
#
#
class Path(Sprite):
    def __init__(self):
        self.waypoints = []

    def addWaypoint(self, x, y):
        point = (x, y)
        self.waypoints.append(point)

    def getWaypoints(self):
        return self.waypoints

    def getWaypointCount(self):
        return len(self.waypoints)

#
# PathDrawer
# 
class PathDrawer(Sprite):
    def __init__(self, path):
        super().__init__(100, 100, 100, 100)
        self.path = path

    def move(self):
        pass

    def draw(self):
        #super().draw()
        previous = None
        for waypoint in self.path.getWaypoints():
            if previous != None:
                drawLine(previous, waypoint, red, 2)
            previous = waypoint

#
# PathFollowSprite
# 
class PathFollowSprite(Sprite):
    def __init__(self, path):
        super().__init__(200, 0, 10, 10)
        self.path = path
        # Which point we're heading towards
        self.headingTowardsPointIdx = 0
        self.velocityVector = None
        self.nextPoint = None

    def move(self):
        if self.velocityVector == None:
            # Calc how to get from our x,y to the next point
            self.setNextPoint()
            self.velocityVector = subtractVectors(self.nextPoint, self.getLocation())
            # TODO: How to tell how many steps to take on this leg of the path?
            self.velocityVector = scaleVector(self.velocityVector, 0.01)

        self.moveBy(self.velocityVector[0], self.velocityVector[1])

        # Check if we're reached the point
        # TODO: This is slightly confusing, to subtract the points as vectors - we should have an 'isVectorEquals' routine, with a tolerance allowed
        check = subtractVectors(self.nextPoint, self.getLocation())
        if isVectorZero(check, 0.01):
            # We reached a point - now head to the next one
            print("We reached point: " + str(self.headingTowardsPointIdx))
            self.headingTowardsPointIdx += 1
            if self.headingTowardsPointIdx >= self.path.getWaypointCount():
                self.headingTowardsPointIdx = 0
            print("-> Now heading to point: " + str(self.headingTowardsPointIdx))
            # Clear out our velocity so it'll be recalculated on the next move call
            self.velocityVector = None

    def setNextPoint(self):
        self.nextPoint = self.path.getWaypoints()[self.headingTowardsPointIdx]

    def draw(self):
        super().draw()
        #drawRect((100,100, 100,100), white, 2)


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
        # Setup a path to draw and follow
        path = Path()
        path.addWaypoint(0, 0)
        path.addWaypoint(50, 50)
        path.addWaypoint(300, 50)
        path.addWaypoint(400, 175)
        path.addWaypoint(400, 300)
        path.addWaypoint(50, 300)
        path.addWaypoint(50, 50)
        # PathDrawer will draw the path as lines
        pygamehelper.addSprite(PathDrawer(path))
        # PathFollowSprite will move along the path
        pygamehelper.addSprite(PathFollowSprite(path))

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

pygamehelper.debug = False
# Run game loop
MyGameLoop().runGameLoop()
