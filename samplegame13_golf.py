import pygamehelper
from pygamehelper import *

#
# Animated Cards
# Something like allowing cards to be placed - like Magic the Gathering or Epic Card Game
#


# Global init
if __name__ == '__main__':
    pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# Ball
# 
class Ball(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def draw(self):
        drawRect(self.boundingRect, white, 2)
        super().draw()

    def onClick(self):
        pass

#
# Ground
# 
class Ground(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, screenRect.width, screenRect.height)

    def draw(self):
        drawRect(self.boundingRect, green)
        # super().draw()

    def onClick(self):
        pass


class AngleChooser(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.angle = 0
        self.angleChange = 1
        self.length = 50
        self.lengthChange = 0

    def move(self):
        self.angle += self.angleChange
        if self.angle > 90 or self.angle < 0:
            self.angleChange = self.angleChange * -1
        
        self.length += self.lengthChange
        if self.length > 150 or self.length < 50:
            self.lengthChange = self.lengthChange * -1

    def draw(self):
        super().draw()
        lineVector = angleToVector(self.angle, self.length)
        drawLineThick((self.x, self.y + self.height), (self.x + lineVector[0], self.y + self.height + lineVector[1]), red)

    def startAngleChange(self):
        self.angleChange = 2
    def stopAngleChange(self):
        self.angleChange = 0

    def startLengthChange(self):
        self.lengthChange = 2
    def stopLengthChange(self):
        self.lengthChange = 0

#
# GameLogicController
#
class GameLogicController(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, screenRect.width, screenRect.height)
        self.numberOfStages = 3
        self.stage = 1
        self.angleChooser = None

    def move(self):
        pass

    def draw(self):
        if self.stage == 1:
            drawText("Welcome to Golf!", self.x, self.y, pygamehelper.largeFont, blue)
            drawText("Click here to begin", self.x, self.y + 30, pygamehelper.largeFont, blue)
        elif self.stage == 2:
            drawText("Choose your shot angle", self.x, self.y, pygamehelper.largeFont, blue)
        else:
            drawText("Choose your shot strength", self.x, self.y, pygamehelper.largeFont, blue)

    def onClick(self):

        self.stage += 1
        if self.stage > self.numberOfStages:
            self.stage = 1

        if self.stage == 1:
            if self.angleChooser != None:
                self.angleChooser.dead = True
                self.angleChooser = None
        elif self.stage == 2:
            if self.angleChooser == None:
                self.angleChooser = AngleChooser(100, 100, 100, 100)
                addSprite(self.angleChooser)
            self.angleChooser.startAngleChange()
        elif self.stage == 3:
            self.angleChooser.stopAngleChange()
            self.angleChooser.startLengthChange()


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

        # Sprites
        addSprite(Ball(50, 350, 20, 20))
        addSprite(Ground(0, 370))

        addSprite(GameLogicController(5, 400))

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
                #self.gridHelper.clearHighlights()
                pass


if __name__ == '__main__':
    pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
