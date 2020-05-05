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
        ground = self.gameLogicController.ground
        ball.setLocation((100, ground.y - ball.height - 1))

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
        self.dragEndPoint = None

        ball = self.gameLogicController.ball
        self.dragStartPoint = (ball.x, ball.y + ball.height)

    def draw(self):
        super().draw()
        if self.dragEndPoint != None:
            drawLineThick(self.dragStartPoint, self.dragEndPoint, red)

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
            self.dragEndPoint = pygame.mouse.get_pos()
    
    def getChosenShotVector(self):
        if self.dragEndPoint == None:
            return (10, -30)
        result = subtractVectors(self.dragEndPoint, self.dragStartPoint)
        # If they dragged down the screen, take that as the drag point spring back towards the ball and hitting it up the screen
        if result[1] > 0:
            result = inverseVector(result)
        return result

class Stage3(Stage):
    def __init__(self, gameLogicController):
        super().__init__(gameLogicController, ["Here is your shot!"])
        self.moveVector = None

    def reset(self):
        self.chosenShotVector = self.gameLogicController.getChosenShotVector()
        self.moveVector = scaleVector(self.chosenShotVector, 0.03)

    def move(self):
        ball = self.gameLogicController.ball
        ball.moveByVector(self.moveVector)
        self.moveVector = (self.moveVector[0], self.moveVector[1] + 0.07)
        # Stop it moving past ground level!
        ground = self.gameLogicController.ground
        if ball.y >= ground.y - ball.height:
            ball.y = ground.y - ball.height
            self.moveVector = (self.moveVector[0] * 0.8, self.moveVector[1] * -0.6)
        # Once ball stops moving, move to next stage of game
        if isVectorZero(self.moveVector, 0.1):
            self.moveVector = (0, 0)
            self.gameLogicController.nextStage()

class Stage4(Stage):
    def __init__(self, gameLogicController):
        super().__init__(gameLogicController, ["Good Shot! Well Played", "Click to play again"])

#
# GameLogicController
#
class GameLogicController(Sprite):
    def __init__(self, x, y, ball, ground):
        super().__init__(x, y, screenRect.width, screenRect.height)
        self.ball = ball
        self.ground = ground
        self.stages = []
        self.stages.append(Stage1(self))
        self.stages.append(Stage2(self))
        self.stages.append(Stage3(self))
        self.stages.append(Stage4(self))
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

    def getStage(self, classname):
        for stage in self.stages:
            if isinstance(stage, classname):
                return stage
        return None

    def getChosenShotVector(self):
        return self.getStage(Stage2).getChosenShotVector()

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
        self.ground = Ground(0, 370)
        addSprite(self.ground)

        self.gameLogicController = GameLogicController(5, 400, self.ball, self.ground)
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
