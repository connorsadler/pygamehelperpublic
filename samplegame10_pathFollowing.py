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
# An Invader - rotates around and moves
# 
class Invader(SpriteWithImage):
    def __init__(self, x, y, velocity, startAngle, angleChangeSpeed):
        super().__init__(x, y, 'invader.png')
        self.velocity = velocity
        self.angle = startAngle
        self.angleChangeSpeed = angleChangeSpeed

    def move(self):
        
        self.rotateBy(self.angleChangeSpeed)
        
        # If we have a moveHandler we will delegate to that
        # TODO: Should the framework still call 'move' if there is a moveHandler on the Sprite? Might be cleaner if not?
        if self.moveHandler:
            self.moveHandler.move(self)
        else:
            self.moveBy(self.velocity[0], self.velocity[1])

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

        # Tag an existing Invader sprite with a moveHandler
        invader = Invader(20, 20, (1,1), 0, 1)
        PathFollowMoveHandler.installForSprite(invader, path)
        pygamehelper.addSprite(invader)

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
