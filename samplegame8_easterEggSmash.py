import pygamehelper
from pygamehelper import *

#
# Easter egg smasher
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# Hole
# 
class Hole(SpriteWithImage):
    def __init__(self, x, y):
        super().__init__(x, y, "images/easterEgg_hole.png")
        self.egg = None

    def move(self):
        if self.egg == None:
            if random.randint(1,10000) > 9950:
                self.egg = Egg(self.x, self.y - 5, self)
                pygamehelper.addSprite(self.egg)

    def eggDied(self):
        # my egg has died so I can now create another egg when I want to
        self.egg = None

    def onClick(self):
        pass

#
# Egg
# 
class Egg(SpriteWithImage):
    def __init__(self, x, y, owningHole):
        super().__init__(x, y, "images/easterEgg_egg.png")
        self.startingy = y
        self.poppingUp = True
        self.owningHole = owningHole

    def move(self):
        if self.poppingUp:
            self.y = self.y - 0.5
            if self.y <= self.startingy - 30:
                self.poppingUp = False
        else:
            self.y = self.y + 0.5
            if self.y == self.startingy:
                self.die()

        self.clipArea = Rect(0,0, self.width, 2 * (self.startingy - self.y))

    def die(self):
        self.dead = True
        self.owningHole.eggDied()

    def onClick(self):
        self.die()

#
# Hammer
# 
class Hammer(SpriteWithImage):
    def __init__(self, x, y):
        super().__init__(x, y, "images/easterEgg_hammer.png")
        # angle will go from -20 to +20 to show hammer wobbling around
        self.angle = 0
        self.angleChange = 1

    def move(self):
        self.angle += self.angleChange
        if self.angle > 20 or self.angle < -20:
            self.angleChange = self.angleChange * -1

    def onClick(self):
        pass

    def moveTo(self, pos):
        self.x = pos[0] + 20
        self.y = pos[1] + 20

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
        # Create a couple of holes
        pygamehelper.addSprite(Hole(50, 50))
        pygamehelper.addSprite(Hole(150, 150))
        pygamehelper.addSprite(Hole(250, 250))

        self.hammer = Hammer(400, 400)
        pygamehelper.addSprite(self.hammer)

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

    def onEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()
            clickedSprites = findSprites(clickPosition)
            if len(clickedSprites) > 0:
                for clickedSprite in clickedSprites:
                    clickedSprite.onClick()
            else:
                pass
        elif event.type == pygame.MOUSEMOTION:
            mousePosition = pygame.mouse.get_pos()
            self.hammer.moveTo(mousePosition)


pygamehelper.debug = False

# Run game loop
MyGameLoop().runGameLoop()
