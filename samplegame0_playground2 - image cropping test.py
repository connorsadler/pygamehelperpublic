import pygamehelper
from pygamehelper import *

#
# Playground for pygame graphics
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# Drawer
# 
class Drawer(Sprite):
    def __init__(self):
        super().__init__(100, 100, 100, 100)

        # this image is 40 x 55
        self.image = pygame.image.load("images/easterEgg_egg.png")
        print("image width/height: " + str(self.image.get_size()))

    def move(self):
        pass

    def draw(self):
        drawRect((100,100, 100,100), white, 2)
        drawImageCentered(self.image, 200,200, None)
        drawImageCentered(self.image, 300,200, Rect(0,0,30,30))
        drawImageCentered(self.image, 400,200, Rect(0,0,40,40))

        drawRect((100,400, 100,100), white, 2)
        drawImage(self.image, 200,400, None)
        drawImage(self.image, 300,400, Rect(0,0,30,30))
        drawImage(self.image, 400,400, Rect(0,0,40,40))

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
        pygamehelper.addSprite(Drawer())

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

# Run game loop
MyGameLoop().runGameLoop()
