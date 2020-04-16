import pygamehelper
from pygamehelper import *

#
# Drag editor
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# SelectionTool
# 
class SelectionTool(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        # The rectangle drawn has a start point and end point - once drawn
        self.dragStartPoint = None
        self.dragEndPoint = None
        # Whether we're drawing out a rectangle by clicking in one corner and dragging and releasing mouse button
        self.dragDrawingRect = False
        # Whether we're moving an existing rectangle
        self.dragMovingRect = False
        self.dragMovingRectOffset = None
        self.dragMovingRectSize = None

    def move(self):
        pass

    def getRectFromPoint(self):
        if self.dragStartPoint != None and self.dragEndPoint != None:
            return rectFromPoints(self.dragStartPoint, self.dragEndPoint)
        else:
            return None

    def draw(self):
        if self.dragStartPoint != None and self.dragEndPoint != None:
            rect = self.getRectFromPoint()
            drawRect(rect, white, 2)
            drawText(str(rect.topleft) + " size " + str(rect.width) + "," + str(rect.height), self.dragStartPoint[0]+3, self.dragStartPoint[1]+3, pygamehelper.mediumFont, white)

    def onClick(self, event):
        clickPosition = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = self.getRectFromPoint()
            if rect != None and rect.collidepoint(clickPosition):
                # Click inside the existing rect to move it around
                self.dragMovingRect = True
                self.dragMovingRectOffset = (clickPosition[0]-self.dragStartPoint[0], clickPosition[1]-self.dragStartPoint[1])
                self.dragMovingRectSize = (rect.width, rect.height)
            else:
                # Click outside any existing rect to draw out a different rect instead
                self.dragDrawingRect = True
                self.dragStartPoint = clickPosition
                self.dragEndPoint = clickPosition
        elif event.type == pygame.MOUSEMOTION:
            if self.dragDrawingRect:
                self.dragEndPoint = clickPosition
            elif self.dragMovingRect:
                self.dragStartPoint = (clickPosition[0] - self.dragMovingRectOffset[0], clickPosition[1] - self.dragMovingRectOffset[1])
                self.dragEndPoint = (self.dragStartPoint[0] + self.dragMovingRectSize[0], self.dragStartPoint[1] + self.dragMovingRectSize[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragDrawingRect = False
            self.dragMovingRect = False


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
        # Create
        self.selectionTool = SelectionTool(50, 50)
        pygamehelper.addSprite(self.selectionTool)

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        pass

    def onEvent(self, event):
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.selectionTool.onClick(event)

pygamehelper.debug = False
#pygamehelper.fps = 2

# Run game loop
MyGameLoop().runGameLoop()
