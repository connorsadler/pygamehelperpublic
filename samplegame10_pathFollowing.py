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
# Path - a list of points
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
        self.calcDestinationAndVelocity()

    # Calc how to get from our current x,y to the next point
    def calcDestinationAndVelocity(self):
        # Grab point which we're currently going to head towards
        self.destinationPoint = self.path.getWaypoints()[self.headingTowardsPointIdx]

        # velocityVector is the amount to move on each step along the path to the destination point
        # TODO: How to tell how many steps to take on this leg of the path?
        self.velocityVector = subtractVectors(self.destinationPoint, self.getLocation())
        self.velocityVector = scaleVector(self.velocityVector, 0.01)

    def move(self):
        # Take a step along the path
        self.moveBy(self.velocityVector[0], self.velocityVector[1])

        # Check if we're reached the point
        # TODO: This is slightly confusing, to subtract the points as vectors - we should have an 'isVectorEquals' routine, with a tolerance allowed
        check = subtractVectors(self.destinationPoint, self.getLocation())
        if isVectorZero(check, 0.01):
            # We reached a point - now head to the next one
            print("We reached point: " + str(self.headingTowardsPointIdx))
            self.headingTowardsPointIdx += 1
            if self.headingTowardsPointIdx >= self.path.getWaypointCount():
                self.headingTowardsPointIdx = 0

            # Calc velocity to the new destination
            self.calcDestinationAndVelocity()
            print("-> Now heading to point: " + str(self.headingTowardsPointIdx) + " at " + str(self.destinationPoint))

    def draw(self):
        super().draw()


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
