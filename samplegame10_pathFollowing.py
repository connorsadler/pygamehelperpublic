import pygamehelper
from pygamehelper import *

#
# Path following
# - setups up a Path - a list of points
# - draws that path as lines using PathDrawer sprite
# - follows that path using a sprite
#


# Global init
if __name__ == '__main__':
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
    def __init__(self, path, pathFollowModeAlternate = False):
        super().__init__(200, 0, 10, 10)
        self.path = path
        # pathFollowModeAlternate
        # True - "advanced" mode which means we calc the number of steps to get from the current point to the destination point
        # False - "simple" mode which means we always take 100 steps between points, no matter how far it is
        self.pathFollowModeAlternate = pathFollowModeAlternate

        # TODO: Add 'speed' variable

        # Which point we're heading towards
        self.headingTowardsPointIdx = 0
        self.calcDestinationAndVelocity()
        # Remember the last location so that we can detect if the sprite has been moved by something else, and recalc our velocity
        self.lastLocation = self.getLocation()

    def setPathFollowModeAlternate(self, val):
        self.pathFollowModeAlternate = val
        # Force a recalc on next 'move' call
        self.velocityVector = None

    # Calc how to get from our current x,y to the next point
    def calcDestinationAndVelocity(self):
        # Grab point which we're currently going to head towards
        self.destinationPoint = self.path.getWaypoints()[self.headingTowardsPointIdx]

        # velocityVector is the amount to move on each step along the path to the destination point
        # TODO: How to tell how many steps to take on this leg of the path?
        self.velocityVector = subtractVectors(self.destinationPoint, self.getLocation())
        if self.pathFollowModeAlternate:
            print("alternate/advanced mode")
            numSteps = getVectorSize(self.velocityVector)
        else:
            print("simple mode - fixed 100 steps")
            numSteps = 100
        print("numSteps: " + str(numSteps))
        if numSteps > 0:
            self.velocityVector = scaleVector(self.velocityVector, 1 / numSteps)
        else:
            self.velocityVector = (0, 0)
        print("velocityVector: " + str(self.velocityVector))

    def move(self):
        if self.lastLocation != self.getLocation() or self.velocityVector == None:
            print("Something was changed since we last moved - we'll have to recalc the velocity")
            self.calcDestinationAndVelocity()

        # Take a step along the path
        self.moveBy(self.velocityVector[0], self.velocityVector[1])
        print("new location: " + str(self.getLocation()))
        self.lastLocation = self.getLocation()

        # Check if we're reached the point
        # TODO: This is slightly confusing, to subtract the points as vectors - we should have an 'isVectorEquals' routine, with a tolerance allowed
        check = subtractVectors(self.destinationPoint, self.getLocation())
        print("check: " + str(check))
        if isVectorZero(check, 0.01):
            # We reached a point - 
            print("We reached point: " + str(self.headingTowardsPointIdx))
            # Ensure we're directly on the point now
            self.setLocation(self.destinationPoint)

            # Now head to the next path point
            self.headingTowardsPointIdx += 1
            if self.headingTowardsPointIdx >= self.path.getWaypointCount():
                self.headingTowardsPointIdx = 0

            # Calc velocity to the new destination
            self.calcDestinationAndVelocity()
            print("-> Now heading to point: " + str(self.headingTowardsPointIdx) + " at " + str(self.destinationPoint))
        elif self.isNextToDestination(check):
            # We are right next to destination
            # On the next move we should hit the destination
            print("Next to destination - we should reach it on next move - assuring this")
            self.velocityVector = check

    # If we're less than our velocity away
    # TODO: Check this with negative numbers
    def isNextToDestination(self, check):
        return abs(check[0]) < abs(self.velocityVector[0]) and abs(check[1]) < abs(self.velocityVector[1])

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
        pygamehelper.addSprite(PathFollowSprite(path, True))

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

if __name__ == '__main__':
    pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
