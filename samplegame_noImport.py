import pygamehelper, random# as pygamehelper - if you're not renaming it, you don't need to import as...
from pygamehelper import * # - I think you either import (in which case you need the library.function format) or you from library import *
#it didn't look like you were actually using random in pygamehelper, so I think it's better to keep it out as a separate library

#
# Starting point for a pygame game
# Features
# - Easy to use a list of sprites, which gets drawn by a standard routine
# - Easy to create your own sprite classes and add them to the list
# - Easy to allow sprites to die and get removed from the list
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
# An Invader moves across the screen from left to right
# It has a health which ticks down, and when health reaches 0, it dies (disappears)
# When it dies, it drops a bomb first
# 
INVADERWIDTH = 40
INVADERHEIGHT = 20
class Invader(pygamehelper.Sprite):
    def __init__(self, x, y, startingHealth):
        super().__init__(x, y, INVADERWIDTH, INVADERHEIGHT)
        self.health = startingHealth

    def draw(self):
        super().draw() # needed to draw the white rectangle - default "look" for a Sprite
        # Draw health inside Invader rectangle
        pygamehelper.drawText(str(self.health), self.x + 2 , self.y + 2, pygamehelper.defaultFont, pygamehelper.black)

    def move(self):
        self.moveBy(1,0)
        self.health = self.health - 1
        if self.health == 0:
            self.dead = True
            # When an Invader dies, it drops a Bomb
            pygamehelper.addSprite(Bomb(self.x + self.width/2, self.y, 100))

#
# A bomb moves across (left to right) and also drops down the screen
# It has a health which ticks down, and when health reaches 0, it dies (disappears)
#
BOMBWIDTH = 10
BOMBHEIGHT = 10
class Bomb(pygamehelper.Sprite):
    def __init__(self, x, y, startingHealth):
        super().__init__(x, y, BOMBWIDTH, BOMBHEIGHT)
        self.health = startingHealth

    def draw(self):
        super().draw() # needed to draw the white rectangle - default "look" for a Sprite
        # Draw health inside Bomb rectangle
        pygamehelper.drawText(str(self.health), self.x + 2 , self.y + 2, pygamehelper.defaultFont, pygamehelper.black)

    def move(self):
        self.moveBy(1,2)
        self.health = self.health - 1
        if self.health == 0:
            self.dead = True

# TODO: This could/should possibly be a sprite? Maybe an exercise for a bright child or adult
def showIntroBanner():
    messages = [ "Hi there", "Welcome to my game", "Hope you'll enjoy it" ]
    currentMessageIndex = int(pygamehelper.gameTick / 100)
    if currentMessageIndex <= len(messages) - 1: 
        currentMessage = messages[currentMessageIndex]
        bannerY = 200 + pygamehelper.gameTick % 100
        pygamehelper.drawText(currentMessage, 200 , bannerY, pygamehelper.hugeFont, pygamehelper.green)

#
# TODO
# Create any initial instances of your sprites here
#
pygamehelper.addSprite(Invader(20, 20, 100))
pygamehelper.addSprite(Invader(20, 50, 100))
pygamehelper.addSprite(Invader(20, 80, 100))

gameExit=False
while not gameExit:
    #
    # TODO
    # Handle any key events in here - maybe we can make this easier?
    #
    for event in pygame.event.get():
        if event.type == pygamehelper.pygame.QUIT:
            pygamehelper.pygame.quit()
            quit()

    # clear screen area
    pygamehelper.displayClear(pygamehelper.blue)

    # display all sprites in the screen area
    pygamehelper.drawAndMoveAllSprites()

    #
    # TODO
    # Perform any global game logic here
    #

    # Intro message - only shows at the start of the game
    if pygamehelper.gameTick < 1000:
        showIntroBanner()

    # Randomly create some more invaders, at random locations on rows on the left of the screen
    if random.randint(1,1000) < 20:
        newInvaderX = 20
        newInvaderY = 20 * random.randint(1,20)
        newInvaderHealth = 50 + random.randint(1,200)
        pygamehelper.addSprite(Invader(newInvaderX, newInvaderY, newInvaderHealth))


    # show the screen area on the display
    pygamehelper.displayUpdate()
    # make the game run at 60 fps
    pygamehelper.clock.tick(60)

