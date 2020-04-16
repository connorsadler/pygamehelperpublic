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
# Background Image
#
class BackgroundImage(Sprite):
    def __init__(self):
        super().__init__(0, 0, 50, 50)

        spriteImageName = "images/bash2.png"
        spriteImageNameResolved = resolveImageFile(spriteImageName)
        self.image = pygame.image.load(spriteImageNameResolved)
        self.zoom = 1
        self.zoomedImage = None

    def move(self):
        pass

    def draw(self):
        if self.zoomedImage == None:
            self.zoomedImage = pygame.transform.rotozoom(self.image, 0, self.zoom)
        drawImage(self.zoomedImage, 0, 0)

    def setZoom(self, zoom):
        self.zoom = zoom
        self.zoomedImage = None

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

        self.zoom = 1

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
            rectZoomed = zoomHelper.rectWorldToScreen(rect)
            # TODO: Make rect line thicker when you zoom in
            drawRect(rectZoomed, white, 2)
            drawText(str(rect.topleft) + " size " + str(rect.width) + "," + str(rect.height), rectZoomed[0]+3, rectZoomed[1]+3, pygamehelper.mediumFont, white)

    def onClick(self, event):

        # dragging - either drawing a rectangle or moving it around
        if event.type == pygame.MOUSEMOTION or ((event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and event.button == 1):
            self.dragHandling(event)

    # dragging - either drawing a rectangle or moving it around
    def dragHandling(self, event):
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

    def setZoom(self, zoom):
        self.zoom = zoom

class ZoomHelper:
    def __init__(self):
        # "zoom" is the transform from world to screen
        # so if zoom == 1.5 then things are 1.5 times bigger onscreen than in the world
        self.zoom = 1

    def setZoom(self, zoom):
        self.zoom = zoom

    def valueTransform(self, value, transformBy):
        return value * transformBy
    def valueWorldToScreen(self, value):
        return self.valueTransform(value, self.zoom)
    def valueScreenToWorld(self, value):
        return self.valueTransform(value, 1.0 / self.zoom)

    def pointTransform(self, p, transformBy):
        return (p[0] * transformBy, p[1] * transformBy)
    def pointWorldToScreen(self, p):
        return self.pointTransform(p, self.zoom)
    def pointScreenToWorld(self, p):
        return self.pointTransform(p, 1.0 / self.zoom)

    def rectTransform(self, rect, transformBy):
        resultTopLeft = self.pointTransform((rect[0], rect[1]), transformBy)
        resultWidth = self.valueTransform(rect[2], transformBy)
        resultHeight = self.valueTransform(rect[3], transformBy)
        return pygame.Rect(resultTopLeft[0], resultTopLeft[1], resultWidth, resultHeight)
    def rectWorldToScreen(self, rect):
        return self.rectTransform(rect, self.zoom)
    def rectScreenToWorld(self, rect):
        return self.rectTransform(rect, 1.0 / self.zoom)


zoomHelper = ZoomHelper()

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
        self.backgroundImage = BackgroundImage()
        pygamehelper.addSprite(self.backgroundImage)
        self.selectionTool = SelectionTool(50, 50)
        pygamehelper.addSprite(self.selectionTool)

        self.zoom = 1

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
            self.onClick(event)

    def setZoom(self, zoom):
        self.zoom = zoom
        print("Zoom is now: " + str(self.zoom))
        self.backgroundImage.setZoom(zoom)
        self.selectionTool.setZoom(zoom)

        zoomHelper.setZoom(self.zoom)

    def onClick(self, event):
        # scroll wheel click?
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
                zoomBy = 0.3 if event.button == 4 else -0.3
                self.setZoom(self.zoom + zoomBy)


pygamehelper.debug = False
#pygamehelper.fps = 2

# Run game loop
MyGameLoop().runGameLoop()
