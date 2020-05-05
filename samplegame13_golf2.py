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

    def onClick(self):
        pass


class Stage:
    def __init__(self, gameLogicController, textMessages):
        self.gameLogicController = gameLogicController
        self.textMessages = textMessages

    def reset(self):
        pass

    def move(self):
        pass

    def draw(self):
        y = self.gameLogicController.y
        for textMessage in self.textMessages:
            drawText(textMessage, self.gameLogicController.x, y, pygamehelper.largeFont, blue)
            y += 30

    def onMouseMove(self, event):
        pass

    def onClick(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # move to next stage by default when a stage is clicked
            return True

class Stage1(Stage):
    def __init__(self, gameLogicController):
        super().__init__(gameLogicController, ["Welcome to Golf!", "Click here to begin"])

    def reset(self):
        # move the ball back to it's initial location
        ball = self.gameLogicController.ball
        ball.setLocation((100, 350))

#
# Allows user to drag and draw the shot "line" away from the ball
# This sets the angle and power of the shot
#
class Stage2(Stage):
    def __init__(self, gameLogicController):
        super().__init__(gameLogicController, ["Click and drag to choose your shot"])
        self.reset()

    def reset(self):
        self.dragging = False
        self.dragEndpoint = None

    def draw(self):
        super().draw()
        if self.dragEndpoint != None:
            ball = self.gameLogicController.ball
            drawLineThick((ball.x, ball.y + ball.height), self.dragEndpoint, red)

    def onClick(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                # shot chosen and mouse released
                return True

        self.dragging = True
        return False

    def isDragging(self):
        return self.dragging

    def onMouseMove(self, event):
        if self.dragging:
            self.dragEndpoint = pygame.mouse.get_pos()

class Stage3(Stage):
    def __init__(self, gameLogicController):
        super().__init__(gameLogicController, ["Get ready for your shot..."])

    def move(self):
        ball = self.gameLogicController.ball
        ball.moveBy(1,1)
#
# GameLogicController
#
class GameLogicController(Sprite):
    def __init__(self, x, y, ball):
        super().__init__(x, y, screenRect.width, screenRect.height)
        self.ball = ball
        self.stages = []
        self.stages.append(Stage1(self))
        self.stages.append(Stage2(self))
        self.stages.append(Stage3(self))
        self.stage = 0

    def move(self):
        self.getCurrentStage().move()

    def getCurrentStage(self):
        return self.stages[self.stage]

    def draw(self):
        self.getCurrentStage().draw()

    def onMouseMove(self, event):
        self.getCurrentStage().onMouseMove(event)

    def onClick(self, event):
        clickResult = self.getCurrentStage().onClick(event)
        if clickResult == True:
            self.nextStage()

    def nextStage(self):
        self.stage += 1
        if self.stage >= len(self.stages):
            self.stage = 0
        self.getCurrentStage().reset()


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
