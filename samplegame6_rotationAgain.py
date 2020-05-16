import pygamehelper as pygamehelper
import random
from pygamehelper import *

#
# Rotation again
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
# An Asteroid - rotates around and moves
# Draws onto it's own 'blank' image at construction time
# The sprite's custom image is then rotated each frame by SpriteWithImage code
# 
class Asteroid(SpriteWithImage):
    def __init__(self, x, y, velocity, startAngle, angleChangeSpeed, size):
        super().__init__(x, y, AsteroidImageDrawer(size))
        self.velocity = velocity
        self.angle = startAngle
        self.angleChangeSpeed = angleChangeSpeed

        # size is 3 -> 2 -> 1
        # so a size 3 will split into two size 2's, and a size 2 will split into 2 size 1's
        # a size 1 will not split at all on death
        self.size = size

        self.collisionDetectionEnabled = True
        self.overlappingAnotherSprite = 0

        self.edgeOfScreenChecker = BounceSprite_EdgeOfScreenChecker()
        self.edgeOfScreenChecker.setModeCompletelyOffScreen()

    def move(self):
        self.rotateBy(self.angleChangeSpeed)
        self.moveBy(self.velocity[0], self.velocity[1])

        # randomly see if we want to die
        # TODO: This should be done on bullet hit, rather than random
        if random.randint(1,1000) > 995:
            self.dead = True
            if self.size > 1:
                self.spawnSmallerAsteroidsOnDeath()

        # reset on every frame the flag to say how many sprites we're overlapping
        self.overlappingAnotherSprite = 0

    # Called if BounceSprite_EdgeOfScreenChecker i s used
    def bounceOnEdgeOfScreen(self):
        # Wrap to other edge of screen
        wrapSpriteOffEdge(self)

    def handleCollisions(self, collidedWithSprites):
        self.overlappingAnotherSprite = len(collidedWithSprites)

    def draw(self):
        super().draw()
        # If we're overlapping another sprite, draw a green border - the thickness depends on how many sprites we're overlapping
        if self.overlappingAnotherSprite > 0:
            pygame.draw.rect(pygamehelper.gameDisplay, green, self.getBoundingRect(), 3 * self.overlappingAnotherSprite)

    def spawnSmallerAsteroidsOnDeath(self):
        # new asteroids will be a size smaller
        newSize = self.size - 1
        # new speed: increases as size decreases
        newSpeed = max(3 - newSize, 1)
        # new angle change speed: increases as size decreases
        newAngleChangeSpeed = max((3 - newSize) * 2, 1)
        for i in range(0,2):
            newVelocity = randomDirectionAsVector(newSpeed)
            pygamehelper.addSprite(Asteroid(self.x, self.y, newVelocity, 0, newAngleChangeSpeed, newSize))

#
# Draws the look of an Asteroid onto it's internal image
#
class AsteroidImageDrawer(CustomDrawingImageHandler):
    # size is 3 -> 2 -> 1
    def __init__(self, size):
        width = size * 20
        height = width
        super().__init__(width, height)

        # Draw our Asteroid 'image'
        # We only have to do this once at construction time, as long as the sprite's image is set in stone for it's whole lifetime
        imageToDraw = self.getSpriteImage()
        imageToDraw.fill(transparentColour)
        
        # Draw a random number of points roughly around a circle centered at the centre of the image
        # Each point is a random angle around and a random distance 'out' from the centre of the image towards the edge
        # e.g.
        #   ------------------
        #   |       P1       |
        #   |                |
        #   |            P2  |
        #   |   P5  X        |
        #   |                |
        #   |          P3    |
        #   |    P4          |
        #   ------------------
        #
        points = []
        middlePoint = (width/2, height/2)
        currentAngle = 0
        while currentAngle < 360:
            newPoint = angleToVector(currentAngle, random.randint(5 * size,width/2))
            newPoint = addVectors(middlePoint, newPoint)
            points.append(newPoint)
            currentAngle += random.randint(20, 70)

        # Draw lines between all the points
        pygame.draw.lines(imageToDraw, green, True, points, 3)



#
# The players ship sprite
# Has two costumes - one normal rocket, and one where the booster is firing
# 
class PlayerShip(SpriteWithImage):
    def __init__(self, x, y):
        super().__init__(x, y, ['rocket-small.png', 'rocket-small-boosting.png'])
        self.speed = 0.04
        self.angle = 45
        self.angleChange = 0
        self.velocity = (0,0)

        # Bounce when completely off screen
        self.edgeOfScreenChecker = BounceSprite_EdgeOfScreenChecker()
        self.edgeOfScreenChecker.setModeCompletelyOffScreen()

        self.boosting = False

    def move(self):
        if self.boosting:
            (dx, dy) = resolveAngle(self.angle, self.speed)
            self.velocity = addVectors(self.velocity, (dx,dy))

        self.moveBy(self.velocity[0], self.velocity[1])
        # TODO: Maybe we could change angle to try to point to a given spot? Not sure exactly
        self.angle += self.angleChange

        # Which costume should we be?
        if self.boosting:
            self.changeCostume(1)
        else:
            self.changeCostume(0)

    # Called if BounceSprite_EdgeOfScreenChecker is used
    def bounceOnEdgeOfScreen(self):
        self.velocity = (0, 0)
        self.x = centreOfScreen[0]
        self.y = centreOfScreen[1]

    def onKeyPressed(self, event):
        if event.key == pygame.K_SPACE:
            self.boosting = not self.boosting
        elif event.key == pygame.K_LEFT:
            self.angleChange = -2
        elif event.key == pygame.K_RIGHT:
            self.angleChange = 2

#pygamehelper.debug = False


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
        pygamehelper.addSprite(Asteroid(150, 150, (1,-1), 0, 1, 3))
        pygamehelper.addSprite(Asteroid(250, 450, (1,1), 0, 1, 3))
        pygamehelper.addSprite(Asteroid(350, 450, (1,1), 0, 1, 3))

        self.playerShip = PlayerShip(centreOfScreenVector.x, centreOfScreenVector.y)
        pygamehelper.addSprite(self.playerShip)

    # Override this to handle key presses etc
    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.playerShip.onKeyPressed(event)

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        if random.randint(1,1000) > 995:
            # spawn new large asteroid
            newSpeed = 1
            newVelocity = randomDirectionAsVector(newSpeed)
            pygamehelper.addSprite(Asteroid(randomX(), randomY(), newVelocity, 0, 1, 3))

# Run game loop
MyGameLoop().runGameLoop()
