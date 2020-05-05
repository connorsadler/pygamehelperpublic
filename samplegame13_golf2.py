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

#
# Allows user to drag and draw the shot "line" away from the ball
# This sets the angle and power of the shot
#
class DragAndDropShotChooser(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.dragging = False
        self.dragEndpoint = None

    def move(self):
        pass

    def draw(self):
        super().draw()
        if self.dragEndpoint != None:
            drawLineThick((self.x, self.y + self.height), self.dragEndpoint, red)

    def onClick(self, event):
        self.dragging = True

    def isDragging(self):
        return self.dragging

    def onMouseMove(self, event):
        if self.dragging:
            self.dragEndpoint = pygame.mouse.get_pos()
        
#
# GameLogicController
#
class GameLogicController(Sprite):
    def __init__(self, x, y, ball):
        super().__init__(x, y, screenRect.width, screenRect.height)
        self.ball = ball
        self.numberOfStages = 3
        self.stage = 1
        self.chooser = None

    def move(self):
        pass

    def draw(self):
        if self.stage == 1:
            drawText("Welcome to Golf!", self.x, self.y, pygamehelper.largeFont, blue)
            drawText("Click here to begin", self.x, self.y + 30, pygamehelper.largeFont, blue)
        elif self.stage == 2:
            drawText("Click and drag to choose your shot", self.x, self.y, pygamehelper.largeFont, blue)
        else:
            drawText("Get ready for your shot...", self.x, self.y, pygamehelper.largeFont, blue)

    def onMouseMove(self, event):
        if self.stage == 2:
            self.chooser.onMouseMove(event)

    def onClick(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.stage == 2:
                self.chooser.onClick(event)
                return

            self.nextStage()
            if self.stage == 1:
                if self.chooser != None:
                    self.chooser.dead = True
                    self.chooser = None
            elif self.stage == 2:
                if self.chooser == None:
                    self.chooser = DragAndDropShotChooser(self.ball.x + 10, self.ball.y, 10, 10)
                    addSprite(self.chooser)
            elif self.stage == 3:
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.stage == 2:
                if self.chooser.isDragging():
                    # shot chosen and mouse released
                    self.nextStage()
            

    def nextStage(self):
        self.stage += 1
        if self.stage > self.numberOfStages:
            self.stage = 1


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
        self.ball = Ball(100, 350, 20, 20)
        addSprite(self.ball)
        addSprite(Ground(0, 370))

        self.gameLogicController = GameLogicController(5, 400, self.ball)
        addSprite(self.gameLogicController)

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

    def onEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.gameLogicController.onClick(event)
        elif event.type == pygame.MOUSEMOTION:
            self.gameLogicController.onMouseMove(event)

if __name__ == '__main__':
    pygamehelper.debug = False
    # Run game loop
    MyGameLoop().runGameLoop()
