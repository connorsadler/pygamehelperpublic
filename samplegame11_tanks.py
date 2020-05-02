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
        self.turret.reset()

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
        self.gunType.changeGunType(1 if makeLonger else -1)

    def draw(self):
        super().draw()
        drawText(str(self.gunType.gunType), 10, 10, pygamehelper.smallFont, red)

    def getTurretVector(self):
        return angleToVector(self.angle, self.turretLength)

    def fire(self):
        # work out where end of turret is
        turretVector = self.getTurretVector()
        endOfTurret = addVectors((self.tank.x, self.tank.y), turretVector)
        # Spawn bullets facing in the same direction as our turret
        self.gunType.fire(self, endOfTurret)

    # Called on first click/unclick of button - to "start shooting" and reset any fuel or variables or accel etc in the shot pattern
    def reset(self):
        self.gunType.reset()

class GunType:
    def __init__(self):
        pass

# TODO: Refactor into different types?
class GunTypeA(GunType):
    def __init__(self):
        super().__init__()
        self.sprayOffset = 0
        self.sprayOffsetAdder = 1
        self.sprayAccel = 1
        self.sprayOffset2 = 0
        self.gunType = 0

        self.NUMBER_OF_GUN_TYPES = 6

    def changeGunType(self, changeBy):
        self.gunType += changeBy
        if self.gunType == self.NUMBER_OF_GUN_TYPES:
            self.gunType = 0
        elif self.gunType < 0:
            self.gunType = self.NUMBER_OF_GUN_TYPES - 1

    def reset(self):
        print("reset")
        self.sprayAccel = 1
        self.sprayOffset2 = 0

    def fire(self, turret, endOfTurret):
        self.sprayOffset += self.sprayOffsetAdder
        if self.sprayOffset > 50 or self.sprayOffset < -50:
            self.sprayOffsetAdder = self.sprayOffsetAdder * -1
        
        self.sprayAccel += 0.05
        self.sprayOffset2 += self.sprayAccel

        if self.gunType == 0:
            numBullets = 20
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = random.randint(1, 20)
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + randomnum)
                addSprite(bullet)
        elif self.gunType == 1:
            numBullets = 72
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = 0
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + randomnum)
                addSprite(bullet)
        elif self.gunType == 2:
            numBullets = 20 - int(self.sprayOffset2 / 40)
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = 0
                #bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (20 * (i - halfBullets)) + randomnum + (self.sprayOffset2 * 2) * (self.sprayAccel / 100))
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (20 * (i - halfBullets)) + randomnum + self.sprayOffset2)
                addSprite(bullet)
        elif self.gunType == 3:
            numBullets = 15
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = random.randint(1, 3)
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (15 * (i - halfBullets)) + randomnum)
                addSprite(bullet)
        elif self.gunType == 4:
            numBullets = 20
            angleStep = 2 * math.pi / numBullets
            angle = 0
            radius = 50
            for i in range(numBullets):
                randomnum = 0
                dx = radius * math.sin(angle)
                dy = radius * math.cos(angle)
                bullet = Bullet(endOfTurret[0] + dx, endOfTurret[1] + dy, turret.getAngle())
                addSprite(bullet)
                angle += angleStep
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
