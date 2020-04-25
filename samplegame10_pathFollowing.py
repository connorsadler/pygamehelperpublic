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

if __name__ == '__main__':
    pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
