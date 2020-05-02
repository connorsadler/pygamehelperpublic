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
        self.firing = False

    def move(self):
        #self.moveBy(self.velocity[0], self.velocity[1])
        self.moveForward(1.5)
        self.turret.move()
        # always keep turrent pointing to last known mouse position
        self.turret.pointTo(self.pointTurrentTo)

        if self.firing:
            self.fireBullet()

    def moveDone(self):
        super().moveDone()
        self.turret.moveDone()

    def draw(self):
        super().draw()
        self.turret.draw()

    def pointTurretTo(self, point):
        self.pointTurrentTo = point

    def fireBullet(self):
        self.turret.fire()

    def setFiring(self, firing):
        self.firing = firing

    def changeTurret(self, makeLonger):
        self.turret.changeTurret(makeLonger)

class Turret(SpriteWithImage):
    def __init__(self, tank):
        self.turretLength = 100
        super().__init__(0, 0, TurrentImageDrawer(self.turretLength))
        self.tank = tank

        self.gunType = GunTypeA()

    def move(self):
        self.setLocation(self.tank.getLocation())

    def setTurretLength(self, turretLength):
        self.turretLength = turretLength
        imageFilenameOrFilenamesOrImageHandler = TurrentImageDrawer(self.turretLength)
        self.imageDrawingHelper = SpriteImageDrawingHelper(self, imageFilenameOrFilenamesOrImageHandler)

    def changeTurret(self, makeLonger):
        self.setTurretLength(self.turretLength + (10 if makeLonger else -10))

    def draw(self):
        super().draw()

    def getTurretVector(self):
        return angleToVector(self.angle, self.turretLength)

    def fire(self):
        # work out where end of turret is
        turretVector = self.getTurretVector()
        endOfTurret = addVectors((self.tank.x, self.tank.y), turretVector)
        # Spawn bullets facing in the same direction as our turret
        self.gunType.fire(self, endOfTurret)

    def getTurretLengthDividedBy10(self):
        return self.turretLength / 10

class GunType:
    def __init__(self):
        pass

# Wipes from side to side
class GunTypeA(GunType):
    def __init__(self):
        super().__init__()
        self.sprayOffset = 0
        self.sprayOffsetAdder = 1

    def fire(self, turret, endOfTurret):
        self.sprayOffset += self.sprayOffsetAdder
        if self.sprayOffset > 50 or self.sprayOffset < -50:
            self.sprayOffsetAdder = self.sprayOffsetAdder * -1

        tl = turret.getTurretLengthDividedBy10()
        self.gunType = tl % 3
        if self.gunType == 1:
            numBullets = 20
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = random.randint(1, 20)
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + randomnum)
                #bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + self.sprayOffset)
                addSprite(bullet)
        elif self.gunType == 2:
            numBullets = 72
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = 0
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + randomnum)
                addSprite(bullet)
        else:
            numBullets = 6
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = random.randint(1, 20)
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + self.sprayOffset)
                addSprite(bullet)



#
# Draws the look of the turret onto it's internal image
#
class TurrentImageDrawer(CustomDrawingImageHandler):
    def __init__(self, turretLength):
        width = 10
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.tank.setFiring(True)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.tank.setFiring(False)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 4:
            self.tank.changeTurret(True)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 5:
            self.tank.changeTurret(False)
        elif event.type == pygame.MOUSEMOTION:
            mousePosition = pygame.mouse.get_pos()
            self.tank.pointTurretTo(mousePosition)

if __name__ == '__main__':
    #pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
