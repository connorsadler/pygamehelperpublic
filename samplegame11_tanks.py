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
        super().__init__(x, y, 'images/Tanks/PNG/Tanks/tankBlue.png')
        self.velocity = velocity
        self.turret = Turret(self)
        self.tracks = Tracks(self)
        self.setBounceOfEdgeOfScreen()

        self.setAngle(90)
        self.firing = False

        # used to tell which offset of tracks image to use
        self.moveCounter = 1

    def move(self):
        #self.moveBy(self.velocity[0], self.velocity[1])
        self.moveForward(1.5)
        self.moveCounter += 1
        self.tracks.move()
        self.turret.move()
        # always keep turrent pointing to last known mouse position
        self.turret.pointTo(self.pointTurrentTo)

        if self.firing:
            self.fireBullet()

    def moveDone(self):
        super().moveDone()
        self.tracks.setAngle(self.getAngle())
        self.tracks.clipArea = Rect(self.moveCounter % 16,0, self.tracks.width, self.tracks.height)
        self.tracks.moveDone()
        self.turret.moveDone()

    def draw(self):
        super().draw()
        self.tracks.draw()
        self.turret.draw()

    def pointTurretTo(self, point):
        self.pointTurrentTo = point

    def fireBullet(self):
        self.turret.fire(self.pointTurrentTo)

    def setFiring(self, firing):
        self.firing = firing
        self.turret.reset()

    def changeTurret(self, makeLonger):
        self.turret.changeTurret(makeLonger)

class Tracks(SpriteWithImage):
    def __init__(self, tank):
        super().__init__(0, 0, 'images/Tanks/PNG/Tanks/tracksSmall_75.png')
        self.tank = tank
        
    def move(self):
        self.setLocation(self.tank.getLocation())


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
        drawText(str(self.gunType.gunType), 10, 10, pygamehelper.largeFont, red)

    def getTurretVector(self):
        return angleToVector(self.angle, self.turretLength)

    def fire(self, towardsPoint):
        # work out where end of turret is
        turretVector = self.getTurretVector()
        endOfTurret = addVectors((self.tank.x, self.tank.y), turretVector)
        # Spawn bullets facing in the same direction as our turret
        self.gunType.fire(self, endOfTurret, towardsPoint)

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
        self.bulletNum = 20

        self.NUMBER_OF_GUN_TYPES = 10

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
        self.bulletNum = 20

    def fire(self, turret, endOfTurret, towardsPoint):
        self.sprayOffset += self.sprayOffsetAdder
        if self.sprayOffset > 50 or self.sprayOffset < -50:
            self.sprayOffsetAdder = self.sprayOffsetAdder * -1
        
        self.sprayAccel += 0.05
        self.sprayOffset2 += self.sprayAccel



        if self.gunType == 0:
            # shotgun with randomness
          numBullets = 20
          halfBullets = numBullets / 2
          for i in range(numBullets):
              randomnum = random.randint(1, 20)
              bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + randomnum)
              addSprite(bullet)
        elif self.gunType == 1:
            # circle sprays outwards
            numBullets = 72
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = 0
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + randomnum)
                addSprite(bullet)
        elif self.gunType == 2:
            # spiral - speeds up rotation, bullets run out after a bit
            numBullets = 20 - int(self.sprayOffset2 / 40)
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = 0
                #bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (20 * (i - halfBullets)) + randomnum + (self.sprayOffset2 * 2) * (self.sprayAccel / 100))
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (20 * (i - halfBullets)) + randomnum + self.sprayOffset2)
                addSprite(bullet)
        elif self.gunType == 3:
            # electro ray
            numBullets = 15
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = random.randint(1, 3)
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (15 * (i - halfBullets)) + randomnum)
                addSprite(bullet)
        elif self.gunType == 4:
            # circle pattern heads towards target
            numBullets = 15
            angleStep = 2 * math.pi / numBullets
            angle = 0
            #angle = math.radians(self.sprayOffset2 % 360)
            radius = 50
            #radius = 50 - int(self.sprayOffset2 / 50)
            for i in range(numBullets):
                randomnum = 0
                dx = radius * math.sin(angle)
                dy = radius * math.cos(angle)
                bullet = Bullet(endOfTurret[0] + dx, endOfTurret[1] + dy, turret.getAngle())
                addSprite(bullet)
                angle += angleStep
        elif self.gunType == 5:
            # arc gun
            numBullets = 15
            arcAngle = math.pi
            angleStep = arcAngle / numBullets
            angle = math.radians(turret.getAngle()) + math.pi
            radius = 50 - int(self.sprayOffset2 / 50)
            for i in range(numBullets+1):
                dx = radius * math.cos(angle)
                dy = radius * math.sin(angle)
                bullet = Bullet(endOfTurret[0] + dx, endOfTurret[1] + dy, turret.getAngle())
                addSprite(bullet)
                angle += angleStep
        elif self.gunType == 6:
            # reverse arc, bullets converge on the clicked point
            numBullets = 10
            arcAngle = math.pi
            angleStep = arcAngle / numBullets
            angle = math.radians(turret.getAngle())
            #radius = 50 - int(self.sprayOffset2 / 50)
            radius = 100
            for i in range(numBullets+1):
                dx = radius * math.cos(angle)
                dy = radius * math.sin(angle)
                bulletStartX = endOfTurret[0] + dx
                bulletStartY = endOfTurret[1] + dy
                # each bullet travels at a different angle, to get from it's start point to the clicked destination point
                bulletTravelVector = subtractVectors(towardsPoint, (bulletStartX, bulletStartY))
                bulletTravelAngle = vectorToAngle(bulletTravelVector)
                bullet = Bullet(bulletStartX, bulletStartY, bulletTravelAngle)
                addSprite(bullet)
                angle += angleStep
        elif self.gunType == 7:
            # reverse arc, delayed firing sequence
            addSprite(Gun7FireHandler(endOfTurret, turret.getAngle(), towardsPoint))
        elif self.gunType == 8:
            # Matty's Gun! Sonic pulse gun with reset
            self.bulletNum = self.bulletNum - 1
            halfBullets = self.bulletNum / 2
            for i in range(self.bulletNum):
              bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)))
              addSprite(bullet)
            # reset number of bullets so it fires in waves when you hold mouse button down
            if self.bulletNum == 0:
                self.bulletNum = 20
        else:
            # wavey hosepipe
            numBullets = 6
            halfBullets = numBullets / 2
            for i in range(numBullets):
                randomnum = random.randint(1, 20)
                bullet = Bullet(endOfTurret[0], endOfTurret[1], turret.getAngle() + (5 * (i - halfBullets)) + self.sprayOffset)
                addSprite(bullet)

# turret experiment
class Gun7FireHandler_v0(Sprite):
    def __init__(self, endOfTurret, turretAngle, towardsPoint):
        super().__init__(endOfTurret[0], endOfTurret[1], 5, 5)
        self.endOfTurret = endOfTurret
        self.turretAngle = turretAngle
        self.towardsPoint = towardsPoint

        self.tick = 0

    def move(self):
        self.tick += 1
        if self.tick % 30 == 0:
            bullet = Bullet(self.endOfTurret[0], self.endOfTurret[1], self.turretAngle)
            addSprite(bullet)

# delayed firing sequence
class Gun7FireHandler(Sprite):
    def __init__(self, endOfTurret, turretAngle, towardsPoint):
        super().__init__(endOfTurret[0], endOfTurret[1], 5, 5)

        self.tick = 0
        self.bullets = []   # bullets initially created, not added to screen yet
        self.bullets2 = []  # bullets added to screen but not moving yet

        # reverse arc, bullets converge on the clicked point
        # create all bullets up front
        # BUT do NOT add them to the screen yet - they will be added on a delay
        # THEN once all added they will be fired forwards together
        numBullets = 20
        arcAngle = math.pi
        angleStep = arcAngle / numBullets
        angle = math.radians(turretAngle)
        #radius = 50 - int(self.sprayOffset2 / 50)
        radius = 50
        for i in range(numBullets+1):
            dx = radius * math.cos(angle)
            dy = radius * math.sin(angle)
            bulletStartX = endOfTurret[0] + dx
            bulletStartY = endOfTurret[1] + dy
            # each bullet travels at a different angle, to get from it's start point to the clicked destination point
            bulletTravelVector = subtractVectors(towardsPoint, (bulletStartX, bulletStartY))
            bulletTravelAngle = vectorToAngle(bulletTravelVector)
            #initialSpeed = 0.3
            #initialSpeed = -1
            #initialSpeed = -0.3 * random.randint(2, 6)
            initialSpeed = -0.3 * i
            bullet = Bullet(bulletStartX, bulletStartY, bulletTravelAngle, initialSpeed)
            self.bullets.append(bullet)
            angle += angleStep

    def move(self):
        self.tick += 1
        if self.tick % 3 == 0:
            if len(self.bullets) > 0:
                bullet = self.bullets.pop(0)
                addSprite(bullet)
                self.bullets2.append(bullet)
            else:
                # start all bullets moving
                for bullet in self.bullets2:
                    bullet.setSpeed(6)
                # stop this firing sequence
                self.dead = True

    def draw(self):
        #super().draw()
        pass

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
    def __init__(self, x, y, angle, speed = 3):
        super().__init__(x, y, 5, 5)
        self.setAngle(angle)
        self.setDieOnEdgeOfScreen()
        self.speed = speed

    def move(self):
        self.moveForward(self.speed)

    def draw(self):
        #super().draw()
        drawRect(self.boundingRect, red, 2)

    def setSpeed(self, speed):
        self.speed = speed

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
    pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
