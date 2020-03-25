import pygamehelper as pygamehelper
import random
from pygamehelper import *

#
# Starting point for a pygame game, with rotating images
# Features
# - Sprite with image and rotation
#
#
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# An Invader - rotates around and moves
# 
class Invader(SpriteWithImage):
    def __init__(self, x, y, velocity, startAngle, angleChangeSpeed, bounceMode):
        super().__init__(x, y, 'invader.png')
        self.velocity = velocity
        self.angle = startAngle
        self.angleChangeSpeed = angleChangeSpeed

        self.collisionDetectionEnabled = True
        self.overlappingAnotherSprite = 0

        # Edge of screen? Kill or bounce - are our two options at present
        if bounceMode == "KillSpriteOnEdgeOfScreen":
            self.edgeOfScreenChecker = KillSprite_EdgeOfScreenChecker()
        else:
            self.edgeOfScreenChecker = BounceSprite_EdgeOfScreenChecker()

    def move(self):
        self.rotateBy(self.angleChangeSpeed)
        self.moveBy(self.velocity[0], self.velocity[1])

        # reset on every frame the flag to say how many sprites we're overlapping
        self.overlappingAnotherSprite = 0

    # Called if BounceSprite_EdgeOfScreenChecker is used
    def bounceOnEdgeOfScreen(self):
        # Bounce off edge of screen
        resolveBounceWithVelocity(self)

    def handleCollisions(self, collidedWithSprites):
        self.overlappingAnotherSprite = len(collidedWithSprites)
        #self.dead = True

    def draw(self):
        super().draw()
        # If we're overlapping another sprite, draw a green border - the thickness depends on how many sprites we're overlapping
        if self.overlappingAnotherSprite > 0:
            pygame.draw.rect(pygamehelper.gameDisplay, green, self.boundingRect, 3 * self.overlappingAnotherSprite)


#
# Keeps track of Rocket's fuel and whether we're boosting i.e. firing our rocket boosters
# Is always either doing nothing, or discharging/boosting, or recharging
# 
class FuelGauge():
    def __init__(self):
        # percentage of fuel left
        self.fuel = 100
        # whether we are discharging fuel or letting it charge up, or doing nothing
        self.fuelChange = -0.5

    def getFuel(self):
        return self.fuel

    def move(self):
        self.fuel += self.fuelChange
        if self.fuelChange < 0:
            if self.fuel <= 0:
                # if fuel drops to 0 then start recharging it, which also stops the boost
                self.fuelChange = 0.5
        else:
            if self.fuel > 100:
                # stop recharging fuel at 100 fuel
                self.fuel = 100
                self.fuelChange = 0

    def isBoosting(self):
        return self.fuelChange < 0

    def hasFuel(self):
        return self.fuel > 0

    def makeBoosting(self):
        self.fuelChange = -0.5

#
# A Rocket ???
# Has two costumes - one normal rocket, and one where the booster is firing
# 
class Rocket(SpriteWithImage):
    def __init__(self, x, y):
        super().__init__(x, y, ['rocket-small.png', 'rocket-small-boosting.png'])
        self.speed = 0.02
        self.angle = 45
        self.angleChange = 0
        self.velocity = (0,0)

        # Bounce when completely off screen
        self.edgeOfScreenChecker = BounceSprite_EdgeOfScreenChecker()
        self.edgeOfScreenChecker.setModeCompletelyOffScreen()

        self.fuelGauge = FuelGauge()
        # TODO: This feels a bit clunky
        self.imageDrawingHelper.addExtraSpriteImagePreparer(self)

    def move(self):
        self.fuelGauge.move()

        # if fuel is discharging then we're boosting, and we should apply a force in the direction of our angle
        if self.fuelGauge.isBoosting():
            (dx, dy) = resolveAngle(self.angle, self.speed)
            self.velocity = addVectors(self.velocity, (dx,dy))

        self.moveBy(self.velocity[0], self.velocity[1])
        # TODO: Maybe we could change angle to try to point to a given spot? Not sure exactly
        self.angle += self.angleChange

        # Which costume should we be?
        if self.fuelGauge.isBoosting():
            self.changeCostume(1)
        else:
            self.changeCostume(0)


    # Called if BounceSprite_EdgeOfScreenChecker is used
    def bounceOnEdgeOfScreen(self):
        self.velocity = (0, 0)
        self.x = centreOfScreen[0]
        self.y = centreOfScreen[1]

    def prepareSpriteImageExtra(self, imageToDraw):
        # draw fuel gauge onto rocket image before rotation
        fuelGaugeColor = red if self.fuelGauge.isBoosting() else green
        pygame.draw.rect(imageToDraw, fuelGaugeColor, (0,0,10,self.fuelGauge.getFuel() * 40 / 100))

    def onKeyPressed(self, event):
        if event.key == pygame.K_SPACE:
            self.fuelGauge.makeBoosting()
        elif event.key == pygame.K_LEFT:
            self.angleChange = -1
        elif event.key == pygame.K_RIGHT:
            self.angleChange = 1

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
        pygamehelper.addSprite(Invader(350, 250, (1,1), 0, 1, "KillSpriteOnEdgeOfScreen"))
        self.rocket = Rocket(150,150)
        pygamehelper.addSprite(self.rocket)
        # Interesting effect if you add another Rocket - they end up overlapping very quickly
        # pygamehelper.addSprite(Rocket(250,350))

    # Override this to handle key presses etc
    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.rocket.onKeyPressed(event)

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        # Randomly create some more invaders, at random locations and angles and speeds etc
        if random.randint(1,1000) < 10:
            self.spawnNewInvader()

    def spawnNewInvader(self):
        newInvaderX = 350
        newInvaderY = 250
        newInvaderXVel = (random.randint(1,30) - 15) / 10
        newInvaderYVel = (random.randint(1,30) - 15) / 10
        newInvaderAngle = random.randint(1,360)
        newInvaderAngleChangeSpeed = (random.randint(1,100) - 50) / 10

        # Some new invaders will Kill/Die on edge of screen, some will Bounce
        bounceMode = "KillSpriteOnEdgeOfScreen" if random.randint(1,10) <= 5 else "BounceSpriteOnEdgeOfScreen"

        newInvader = Invader(newInvaderX, newInvaderY, (newInvaderXVel, newInvaderYVel), newInvaderAngle, newInvaderAngleChangeSpeed, bounceMode)
        pygamehelper.addSprite(newInvader)

# Run game loop
MyGameLoop().runGameLoop()
