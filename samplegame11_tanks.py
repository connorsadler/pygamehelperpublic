import pygamehelper
from pygamehelper import *

#
# Tanks
# TODO: Tank
# TODO: Turrent
# TODO: Point Turrent towards mouse pointer
#


# Global init
if __name__ == '__main__':
    pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# An Tank - rotates around and moves
# 
class Tank(SpriteWithImage):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, 'invader.png')  # TODO: Image of a tank!
        self.velocity = velocity
        self.turret = Turret(self)
        self.setBounceOfEdgeOfScreen()

        self.setAngle(90)

    def move(self):
        #self.moveBy(self.velocity[0], self.velocity[1])
        self.moveForward(1.5)
        self.turret.move()
        # always keep turrent pointing to last known mouse position
        self.turret.pointTo(self.pointTurrentTo)

    def moveDone(self):
        super().moveDone()
        self.turret.moveDone()

    def draw(self):
        super().draw()
        self.turret.draw()

    def pointTurretTo(self, point):
        self.pointTurrentTo = point

    def onClick(self, point):
        # Spawn a bullet facing in the same direction as our turret
        bullet = Bullet(self.x, self.y, self.turret.getAngle())
        addSprite(bullet)

class Turret(SpriteWithImage):
    def __init__(self, tank):
        super().__init__(0, 0, TurrentImageDrawer())
        self.tank = tank

    def move(self):
        self.setLocation(self.tank.getLocation())

    def draw(self):
        super().draw()

#
# Draws the look of the turret onto it's internal image
#
class TurrentImageDrawer(CustomDrawingImageHandler):
    def __init__(self):
        width = 10
        turretLength = 50
        height = turretLength * 2
        super().__init__(width, height)

        # Draw our turret 'image'
        # Must point NORTH by default, then will be rotated correctly
        # We only have to do this once at construction time, as long as the sprite's image is set in stone for it's whole lifetime
        imageToDraw = self.getSpriteImage()
        imageToDraw.fill(transparentColour)
        
        pygame.draw.rect(imageToDraw, red, (0,turretLength,10,-turretLength), 0)

class Bullet(Sprite):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 5, 5)
        self.setAngle(angle)
        self.setDieOnEdgeOfScreen()

    def move(self):
        self.moveForward(3)

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
        self.tank = Tank(50, 300, (1,0))
        pygamehelper.addSprite(self.tank)

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
            self.tank.onClick(clickPosition)
        elif event.type == pygame.MOUSEMOTION:
            mousePosition = pygame.mouse.get_pos()
            self.tank.pointTurretTo(mousePosition)

if __name__ == '__main__':
    #pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
