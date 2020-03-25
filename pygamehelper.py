#
# helper library to help with pygame games
#

print("DigiLocal pygamehelper.py is running")

import pygame, sys
from pygame.locals import *
import random
import math

display_width = 800
display_height = 600
screenRect = pygame.Rect(0, 0, display_width, display_height)
centreOfScreen = (display_width/2, display_height/2)

centreOfScreenVector = pygame.math.Vector2(centreOfScreen)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
redalt = (150,10,15)
redbright = (250,10,15)
blue =(0,0,160)
dark_green = (54, 102, 22)
green = (0, 128, 0)
yellow = (236, 245, 66)
purple = (255, 0, 255)
yellow = (255, 255, 0)
teal = (0, 255, 255)
colours = [red, blue, green, purple, yellow, teal]
transparentColour = (0,0,0,0)
transparentColor = transparentColour

def getScreenRect():
    return screenRect

class Sprite():

    #
    # width/height - if you plan on using an image, you can omit both of these values. The sprite's height/width will be set automatically - they'll be available in self.boundingRect
    # 
    def __init__(self, x, y, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # init this here to setup an initial value - sometimes when a sprite is added by another sprite at a certain point in the sequence, it won't have had it's moveDone called
        self.boundingRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # to kill a sprite (i.e. remote it from the game) you can either:
        #    1. set self.dead to True
        # or 2. implement a function checkDead in your Sprite subclass, and return a list of sprites which you want to die on that frame of the game
        self.dead = False
        # by default sprites don't check collisions
        self.collisionDetectionEnabled = False
        # edge of screen checker
        self.edgeOfScreenChecker = None
        # angle the sprite is 'facing' i.e. the angle it's image will be rotated to if it has an image
        self.angle = 0

        # Don't overwrite self.imageDrawingHelper if it's already set by a subclass
        if not hasattr(self, "imageDrawingHelper"):
            self.imageDrawingHelper = None

    def setAngle(self, newAngle):
        self.angle = newAngle

    def rotateBy(self, angleChange):
        self.angle += angleChange

    def getLocation(self):
        return (self.x, self.y)

    def moveBy(self, xvel, yvel):
        self.x += xvel
        self.y += yvel

    def moveForward(self, amount):
        (dx, dy) = resolveAngle(self.angle, amount)
        self.x += dx
        self.y += dy

    def move(self):
        pass

    def moveDone(self):
        if self.imageDrawingHelper:
            self.imageDrawingHelper.moveDone()
        else:
            self.boundingRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def isOnScreen(self):
        return self.boundingRect.colliderect(getScreenRect())

    # returns:
    #   2 - completely on screen
    #   1 - touching edge of screen
    #   0 - complete off screen
    # TODO: Returning an int is rather iffy - needs to use an enumerated type, can you do that in Python?
    def isOnScreenEx(self):
        if getScreenRect().contains(self.boundingRect):
            return 2
        return 1 if self.isOnScreen() else 0

    def setBounceOfEdgeOfScreen(self):
        self.edgeOfScreenChecker = BounceSprite_EdgeOfScreenChecker()

    def checkEdgeOfScreen(self):
        if self.edgeOfScreenChecker:
            self.edgeOfScreenChecker.checkEdgeOfScreen(self)

    def bounceOnEdgeOfScreen(self):
        resolveBounce(self)

    def isCollisionDetectionEnabled(self):
        return self.collisionDetectionEnabled

    def checkCollisions(self):
        collidedWithSprites = findCollisions(self)
        if len(collidedWithSprites) > 0:
            self.handleCollisions(collidedWithSprites)
    
    def handleCollisions(self, collidedWithSprites):
        pass

    def draw(self):
        if self.imageDrawingHelper:
            # If there's a drawing delegate, we use it - this can draw a rotated image for example
            self.imageDrawingHelper.draw()
        else:
            # If there's an imageDrawingHelper, we dont draw the white background for this sprite
            # By default our rect starts from x,y and extends by width-height
            pygame.draw.rect(gameDisplay, white, self.boundingRect)

    def getBoundingRect(self):
        return self.boundingRect

    def checkDead(self):
        # Simple way to kill a sprite
        # If you wish to use a more advanced way to kill sprites, then please implement your own checkDead method in your Sprite subclass
        if self.dead:
            return [self]
        return []
    
    def onDeathSpawn(self):
        return []
    
    def drawDebug(self):
        pygame.draw.rect(gameDisplay, red, self.boundingRect, 1)

    # Only works if we have a self.imageDrawingHelper
    def changeCostume(self, costumeIndex):
        if self.imageDrawingHelper:
            self.imageDrawingHelper.changeCostume(costumeIndex)
        else:
            print("changeCostume called with no imageDrawingHelper, costumeIndex: " + str(costumeIndex))

#
# This is reduced in size now and could maybe be deleted
#
class SpriteWithImage(Sprite):
    def __init__(self, x, y, imageFilenameOrFilenamesOrImageHandler):
        super().__init__(x, y)
        self.imageDrawingHelper = SpriteImageDrawingHelper(self, imageFilenameOrFilenamesOrImageHandler)

# 
# Helper class which implements a Sprite with image (or images aka costumes)
# This also can optionally rotate the images
# You can change costume by calling: changeCostume(0) for first costume, etc
#
class SpriteImageDrawingHelper():
    # imageFilenameOrFilenamesOrImageHandler can be either:
    # - an image file name
    # - a list of image file names (different costumes)
    # - a custom ImageHandler
    def __init__(self, sprite, imageFilenameOrFilenamesOrImageHandler):
        super().__init__()

        self.sprite = sprite

        # Create an imageHandler or use the custom one supplied
        if isinstance(imageFilenameOrFilenamesOrImageHandler, ImageHandler):
            self.imageHandler = imageFilenameOrFilenamesOrImageHandler
        else:
            self.imageHandler = ImageHandler(imageFilenameOrFilenamesOrImageHandler)

        # Default to no extra sprite image preparation (drawing) - can be overridden later by the subclass
        self.extraSpriteImagePreparer = None

        # Set the size of the sprite now - not exactly sure what sprite width/height get used for TODO: Maybe we can tidy that up?
        imageSize = self.getSpriteImage().get_size()
        self.sprite.width = imageSize[0]
        self.sprite.height = imageSize[1]

    def changeCostume(self, costumeIndex):
        self.imageHandler.changeCostume(costumeIndex)

    def addExtraSpriteImagePreparer(self, extraSpriteImagePreparer):
        self.extraSpriteImagePreparer = extraSpriteImagePreparer

    def getSpriteImage(self):
        return self.imageHandler.getSpriteImage()

    # prepare the image (from the current costume image)
    # optionally rotate the image
    # update our sprite's bounding box
    def moveDone(self):
        imageToDraw = self.prepareSpriteImage()
        # Optionally rotate the image
        if self.sprite.angle != 0:
            # rotate does counterclockwise rotation, but we want clockwise
            self.imageRotated = pygame.transform.rotate(imageToDraw, -1 * self.sprite.angle)
        else:
            self.imageRotated = imageToDraw
        # Not sure how important sprite.width/height are TODO: Maybe we can tidy that up?
        self.sprite.width = self.imageRotated.get_size()[0]
        self.sprite.height = self.imageRotated.get_size()[1]
        self.sprite.boundingRect = calcBoundingRectCenteredOnXY(self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height)

    def prepareSpriteImage(self):
        result = self.imageHandler.getSpriteImage()
        if self.extraSpriteImagePreparer:
            # copy the current costume as we're about to do some custom drawing onto it
            result = result.copy()
            self.extraSpriteImagePreparer.prepareSpriteImageExtra(result)
        return result

    def draw(self):
        # draw the image, centred on x,y - so that any rotation looks good
        drawImageCentered(self.imageRotated, self.sprite.x, self.sprite.y)


# Loads and contains one or more images to use for a SpriteWithImage
# Basically a list of costumes
class ImageHandler():
    def __init__(self, imageFilenameOrFilenames):
        
        # We are either given one image name or multiple - check which we're given
        if isinstance(imageFilenameOrFilenames, str):
            spriteImageNames = [ imageFilenameOrFilenames ]
        else:
            spriteImageNames = imageFilenameOrFilenames
        
        # Load all the image names and store images
        self.spriteImages = []
        for spriteImageName in spriteImageNames:
            image = pygame.image.load(spriteImageName)
            self.spriteImages.append(image)

        # default to first image
        self.changeCostume(0)

    def getSpriteImage(self):
        return self.spriteImage

    # costumeIndex starts at 0 for the first costume
    def changeCostume(self, costumeIndex):
        # TODO: What if costumeIndex is invalid?
        self.spriteImage = self.spriteImages[costumeIndex]

#
# Has a custom transparent Surface that you can paint a sprite image onto in code e.g. an Asteroid in Asteroids
#
class CustomDrawingImageHandler(ImageHandler):
    def __init__(self, width, height):
        # transparency notes: https://riptutorial.com/pygame/example/23788/transparency
        self.spriteImage = pygame.Surface((width, height), pygame.SRCALPHA)
        self.spriteImage.set_alpha(200)  # 0 is fully transparent and 255 fully opaque.

    def getSpriteImage(self):
        return self.spriteImage


# Will kill the sprite if it goes off screen
# Can be used as a Sprite edgeOfScreenChecker
class KillSprite_EdgeOfScreenChecker():
    def __init__(self):
        pass

    def checkEdgeOfScreen(self, sprite):
        if not sprite.isOnScreen():
            sprite.dead = True

# Will bounce the sprite if it touches the edge of the screen (or if it's completely off screen)
# Can be used as a Sprite edgeOfScreenChecker
# To be bounceable, the Sprite must have a "bounceOnEdgeOfScreen" method
class BounceSprite_EdgeOfScreenChecker():
    def __init__(self):
        self.setModeTouchingEdge()

    def setModeTouchingEdge(self):
        # touching edge
        self.checkForValue = 1

    def setModeCompletelyOffScreen(self):
        # completely off screen
        self.checkForValue = 0

    def checkEdgeOfScreen(self, sprite):
        if sprite.isOnScreenEx() == self.checkForValue:
            # TODO: Determine which edge it is, or provide an easy way for 'bounceOnEdgeOfScreen' to do that
            #  Use calcEdgesHit for this
            #  Maybe it could even be more than one edge, but that is an extreme 'edge case' ;]
            sprite.bounceOnEdgeOfScreen()


def findCollisions(sprite):
    result = []
    spriteBoundingRect = sprite.getBoundingRect()
    for otherSprite in sprites:
        if otherSprite != sprite:
            if spriteBoundingRect.colliderect(otherSprite.getBoundingRect()):
                result.append(otherSprite)
    return result

def calcBoundingRectCenteredOnXY(x, y, width, height):
    topLeftX = x - width / 2
    topLeftY = y - height / 2
    rect = pygame.Rect(topLeftX, topLeftY, width, height)
    return rect

def drawImageCentered(image, x, y):
    halfOfImageWidth = image.get_size()[0] / 2
    halfOfImageHeight = image.get_size()[1] / 2
    topLeft = (x - halfOfImageWidth, y - halfOfImageHeight)
    # draw image
    gameDisplay.blit(image,topLeft)

# Resolve an angle in degress to a dx, dy value
# The result is like a vector - speed is the length of the vector
# An angle of 0 means pointing "North" which equates to a result vector (0,-1) * speed
# As the angle increases, we rotate clockwise around to the right
def resolveAngle(angleInDegrees, speed):
    angleInRadians = math.radians(angleInDegrees)
    dx = round(math.sin(angleInRadians), 10) * speed
    dy = -1 * round(math.cos(angleInRadians), 10) * speed
    return (dx, dy)

# angle (and speed) -> vector (dx,dy tuple)
def angleToVector(angleInDegrees, speed):
    return resolveAngle(angleInDegrees, speed)

# vector (dx,dy tuple) -> angle in degrees
# 0 is North which is (0,-1)
def vectorToAngle(vector):
    return calcAngle(vector[0], vector[1])

# opposite of resolveAngle - get a dx and dy value and find the angle that this direction represents
# returns an angle in degress
def calcAngle(dx, dy):
    if dx == 0:
        dx = 0.0000001
    if dy == 0:
        dy = 0.0000001
    result = round( math.degrees( round( math.atan(dy/dx), 10) ), 3)

    # part adapted from here: https://stackoverflow.com/questions/6247153/angle-from-2d-unit-vector
    if dx < 0 and dy < 0: # quadrant 3
        result = 180 + result
    elif dx < 0: # quadrant 2
        result = 180 + result # it actually substracts
    elif dy < 0: # quadrant 4
        result = 270 + (90 + result) # it actually substracts

    # current angle is CLOCKWISE from East
    # we wish it to be CLOCKWISE from North
    result += 90
    if result >= 360:
        result -= 360

    return result

def addVectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

# Returns a collection of items:
# 1 top edge
# 2 bottom edge
# 3 right edge
# 4 left edge
def calcEdgesHit(sprite):
    screenRect = getScreenRect()
    spriteRect = sprite.getBoundingRect()
    result = []
    # 1 top edge
    if spriteRect.y <= 0:
        result.append(1)
    # 2 bottom edge
    if spriteRect.bottom >= screenRect.bottom:
        result.append(2)
    # 3 left edge
    if spriteRect.x <= 0:
        result.append(3)
    # 4 right edge
    if spriteRect.right >= screenRect.right:
        result.append(4)
    
    return result

# Called when sprite has touched edge of screen
# Must calculate and set the new angle in sprite
def resolveBounce(sprite):
    # get current vector of movement
    (dx, dy) = resolveAngle(sprite.angle, 1)
    #print("initial dx, dy: " + str(dx) + ", " + str(dy))

    # find edge(s) hit
    edgesHit = calcEdgesHit(sprite)
    #print("edges hit: " + str(edgesHit))

    # calc new vector of movement
    if 1 in edgesHit or 2 in edgesHit:
        dy *= -1
    if 3 in edgesHit or 4 in edgesHit:
        dx *= -1
    
    #print("final dx, dy: " + str(dx) + ", " + str(dy))
    # calc new angle
    newAngle = calcAngle(dx, dy)
    #print("angle: " + str(sprite.angle))
    #print("newAngle: " + str(newAngle))
    sprite.setAngle(newAngle)

# Called when sprite has touched edge of screen
# Must calculate and set the new angle in sprite
# Note: sprite must have a 'velocity' property
def resolveBounceWithVelocity(sprite):
    # get current vector of movement
    (dx, dy) = sprite.velocity

    # find edge(s) hit
    edgesHit = calcEdgesHit(sprite)

    # calc new vector of movement
    if 1 in edgesHit or 2 in edgesHit:
        dy *= -1
    if 3 in edgesHit or 4 in edgesHit:
        dx *= -1
    
    sprite.velocity = (dx, dy)

# Call this when the sprite has gone completely off screen on an edge, and you want to move it just offscreen on the opposite edge
# The assumption is that the sprite will keep moving in the same direction and therefore come back onscreen
def wrapSpriteOffEdge(sprite):
    edgesHit = calcEdgesHit(sprite)
    if 1 in edgesHit:
        # top edge
        sprite.moveBy(0, getScreenRect().height + sprite.getBoundingRect().height)
    if 2 in edgesHit:
        # bottom edge
        sprite.moveBy(0, -getScreenRect().height - sprite.getBoundingRect().height)
    if 3 in edgesHit:
        # left edge
        sprite.moveBy(getScreenRect().width + sprite.getBoundingRect().width, 0)
    if 4 in edgesHit:
        # right edge
        sprite.moveBy(-getScreenRect().width - sprite.getBoundingRect().width, 0)

# chooses a random direction
# returns a (dx,dy) vector
def randomDirectionAsVector(size = 1):
    randomAngle = random.randint(0, 360)
    return angleToVector(randomAngle, size)

def randomX():
    return random.randint(1, getScreenRect().width)

def randomY():
    return random.randint(1, getScreenRect().height)

gameDisplay = None
clock = None
defaultFont = None
largeFont = None
hugeFont = None
sprites = []
debug = True
gameTick = 0
# This will be the GameLoop subclass instance - you can use "pygamehelper.game" to use this from anywhere e.g. inside a Sprite's code
game = None

def drawText(text, x, y, font, colour):
    t = font.render(text, True, colour)
    gameDisplay.blit(t, (x, y))

def initPygame():
    print(">>> initPygame")
    
    global gameDisplay
    global clock
    global defaultFont
    global largeFont
    global hugeFont
    pygame.init()
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    print("gameDisplay is now: " + str(gameDisplay))
    clock = pygame.time.Clock()
    defaultFont = pygame.font.SysFont(None, 12)
    largeFont = pygame.font.SysFont(None, 36)
    hugeFont = pygame.font.SysFont(None, 72)
    
    print("<<< initPygame")

def displayClear(backgroundColour):
    gameDisplay.fill(backgroundColour)

def displayUpdate():
    global gameTick
    gameTick += 1
    pygame.display.update()

def addSprite(sprite):
    sprites.append(sprite)

# deprecated name - please use moveAndDrawAllSprites
def drawAndMoveAllSprites():
    moveAndDrawAllSprites()

def drawRect(rect, colour, width=0):
    pygame.draw.rect(gameDisplay, colour, rect, width)

def drawPoint(point, colour):
    drawRect(Rect(point[0],point[1],3,3), colour)

#
# Draws and moves all sprites
# Also asks all sprites whether any sprite is dead, and removes dead sprites from the game
#
def moveAndDrawAllSprites():
    global sprites

    # move
    for sprite in sprites:
        sprite.move()
        # This sets boundingRect so all sprites must have this done before we can check collisions in the next loop
        sprite.moveDone()

    # 'after move' stuff
    allDeads = []
    for sprite in sprites:
        if sprite.isCollisionDetectionEnabled():
            sprite.checkCollisions()
        sprite.checkEdgeOfScreen()

        deadsForMe = sprite.checkDead()
        if deadsForMe != None:
            allDeads.extend(deadsForMe)

    for allDeadItem in allDeads:
        if allDeadItem in sprites:
            sprites.remove(allDeadItem)

    # draw
    for sprite in sprites:
        sprite.draw()
        if debug:
            sprite.drawDebug()

    if debug:
        drawText("gameTick: " + str(gameTick), 10, display_height-30, defaultFont, white)
        drawText("sprites count: " + str(len(sprites)), 10, display_height-20, defaultFont, white)

#
# Class to hold the main game loop logic
# You should subclass this in your game, and provide an "eachFrame" method which will be called on every frame.
# That can spawn new sprites or do other 'global' tasks.
#
class GameLoop():

    def __init__(self):
        global game
        game = self

    # Override this to provide your own code which will run on every frame
    def eachFrame(self):
        pass

    # Override this to handle key presses etc
    def onEvent(self, event):
        pass

    # Call this to start the infinite move-draw loop - that's your game loop
    def runGameLoop(self):
        gameExit=False
        while not gameExit:
            # Handle any key events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.onEvent(event)

            # clear screen area
            displayClear(blue)

            # Perform any global game logic here
            self.eachFrame()

            # display all sprites in the screen area
            moveAndDrawAllSprites()

            # show the screen area on the display
            displayUpdate()
            # make the game run at 60 fps
            clock.tick(60)




print("DigiLocal pygamehelper.py has been included")

