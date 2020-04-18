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
        # The image to draw is cached in zoomedImage - it could be zoomed in or out
        self.zoomedImage = None

    def move(self):
        pass

    def draw(self):
        if self.zoomedImage == None:
            self.zoomedImage = pygame.transform.rotozoom(self.image, 0, zoomHelper.getZoom())
        worldOrigin_screen = zoomHelper.pointWorldToScreen((0,0))
        drawImage(self.zoomedImage, worldOrigin_screen[0], worldOrigin_screen[1])
        self.drawGrid()

    # Draw grid
    # The grid is based on World coords
    # Must take into account zoom level and pan amount
    # TODO: Move this elsewhere... maybe into ZoomHelper even?
    def drawGrid(self):
        gridSizeWorld = 250
        gridSizeScreen = zoomHelper.valueWorldToScreen(gridSizeWorld)

        screenTopLeft_world = zoomHelper.pointScreenToWorld((0,0))
        # Calc world coord of first grid point we wish to draw onscreen
        screenTopLeft_world_snappedToGrid = (int(screenTopLeft_world[0] / gridSizeWorld) * gridSizeWorld, int(screenTopLeft_world[1] / gridSizeWorld) * gridSizeWorld)
        # Calc equivalent screen coord
        screenTopLeft_screen_snappedToGrid = zoomHelper.pointWorldToScreen(screenTopLeft_world_snappedToGrid)
        # print("screenTopLeft_world: " + str(screenTopLeft_world))
        # print("screenTopLeft_world_snappedToGrid: " + str(screenTopLeft_world_snappedToGrid))
        # print("screenTopLeft_screen_snappedToGrid: " + str(screenTopLeft_screen_snappedToGrid))

        # Draw
        # Step across the x axis, drawing vertical lines
        self.drawGrid_oneDirection(True, gridSizeWorld, gridSizeScreen, getScreenRect().width, screenTopLeft_world_snappedToGrid[0], screenTopLeft_screen_snappedToGrid[0])
        # Step up the y axis, drawing horizontal lines
        self.drawGrid_oneDirection(False, gridSizeWorld, gridSizeScreen, getScreenRect().height, screenTopLeft_world_snappedToGrid[1], screenTopLeft_screen_snappedToGrid[1])
        
    def drawGrid_oneDirection(self, across, gridSizeWorld, gridSizeScreen, screenSizeScreen, screenTopLeft_world_snappedToGrid, screenTopLeft_screen_snappedToGrid):
        numGridCellsToDraw_across = int(screenSizeScreen / gridSizeScreen) + 1
        # if we're going 'across' then 'currentpos' is an x coord
        # if we're going 'down' then 'currentpos' is a y coord
        currentpos_world = screenTopLeft_world_snappedToGrid
        currentpos_screen = screenTopLeft_screen_snappedToGrid
        for x in range(0, numGridCellsToDraw_across):
            axis = (currentpos_world == 0)
            width = (3 if axis else 2)
            if across:
                drawLine((currentpos_screen, 0), (currentpos_screen, screenRect.height), red if axis else green, width)
            else:
                drawLine((0, currentpos_screen), (screenRect.width, currentpos_screen), red if axis else green, width)
            # Move world and screen along - keeping track of both avoids any rounding issues when checking if we're on the axis
            currentpos_world += gridSizeWorld
            currentpos_screen += gridSizeScreen

    def onZoomChanged(self):
        # Zoom has changed - recreate the zoomed image on next 'draw'
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

        # panning
        self.panning = False
        self.panningStartClickPositionScreen = None
        self.panningStartOrigin = None

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
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("button: " + str(event.button))

        mouseButtonUpOrDown = (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP)

        # right click to pan
        if (self.panning and event.type == pygame.MOUSEMOTION) or (mouseButtonUpOrDown and event.button == 3):
            self.panHandling(event)

        # dragging - either drawing a rectangle or moving it around
        if ((self.dragDrawingRect or self.dragMovingRect) and event.type == pygame.MOUSEMOTION) or (mouseButtonUpOrDown and event.button == 1):
            self.dragHandling(event)


    def panHandling(self, event):
        clickPositionScreen = pygame.mouse.get_pos()
        clickPositionWorld = zoomHelper.pointScreenToWorld(clickPositionScreen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("pan start")
            self.panning = True
            self.panningStartClickPositionScreen = clickPositionScreen
            self.panningStartOrigin = zoomHelper.getOrigin()
            print("self.panningStartClickPositionScreen: " + str(self.panningStartClickPositionScreen))
        elif event.type == pygame.MOUSEMOTION:
            print("panning - setting origin")
            diffBetweenCurrentMousePosAndStartPanPos_screen = (clickPositionScreen[0] - self.panningStartClickPositionScreen[0], clickPositionScreen[1] - self.panningStartClickPositionScreen[1])
            print("diffBetweenCurrentMousePosAndStartPanPos_screen: " + str(diffBetweenCurrentMousePosAndStartPanPos_screen))
            diff_world = (zoomHelper.valueScreenToWorld(diffBetweenCurrentMousePosAndStartPanPos_screen[0]), zoomHelper.valueScreenToWorld(diffBetweenCurrentMousePosAndStartPanPos_screen[1]))
            zoomHelper.setOrigin((self.panningStartOrigin[0] - diff_world[0], self.panningStartOrigin[1] - diff_world[1]))
        elif event.type == pygame.MOUSEBUTTONUP:
            print("pan end")
            self.panning = False
            self.panningStartClickPositionScreen = None
            self.panningStartOrigin = None

    # dragging - either drawing a rectangle or moving it around
    def dragHandling(self, event):
        # Find where user clicked in the WORLD coordinate space
        clickPositionScreen = pygame.mouse.get_pos()
        clickPosition = zoomHelper.pointScreenToWorld(clickPositionScreen)

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
# ZoomHelper
# Helps with zooming - does the mapping from world to screen coordinates and vice versa
# All our coords such as rectangles etc will be in WORLD coords, and they will be mapped to different
# screen coords depending on the zoom level
# TODO: Move to pygamehelper.py!
# 
class ZoomHelper:
    def __init__(self):
        # "zoom" is the transform from world to screen
        # so if zoom == 1.5 then things are 1.5 times bigger onscreen than in the world
        self.zoom = 1
        self.zoomStep = 1
        # origin is in World coords, to allow panning. This is the world coord which will appear at the top left of the screen
        self.origin = (-50, -50)

        # Allow registration of listeners which will be informed when zoom changes
        # Each listener must implement: onZoomChanged()
        self.zoomChangedListeners = []

    def setZoom(self, zoom, zoomStep):
        self.zoom = zoom
        self.zoomStep = zoomStep
        # Inform any listeners
        for zoomChangedListener in self.zoomChangedListeners:
            zoomChangedListener.onZoomChanged()
    
    def getZoom(self):
        return self.zoom

    def addZoomChangedListener(self, listener):
        self.zoomChangedListeners.append(listener)

    def setOrigin(self, origin):
        #print("setOrigin: " + str(origin))
        self.origin = origin

    def panByWorld(self, vectorWorld):
        self.setOrigin((self.origin[0] + vectorWorld[0], self.origin[1] + vectorWorld[1]))

    def getOrigin(self):
        return self.origin

    def valueTransform(self, value, worldToScreen):
        transformBy = self.zoom if worldToScreen else 1.0 / self.zoom
        return value * transformBy
    def valueWorldToScreen(self, value):
        return self.valueTransform(value, True)
    def valueScreenToWorld(self, value):
        return self.valueTransform(value, False)

    def pointTransform(self, p, worldToScreen):
        if worldToScreen:
            # world -> screen
            transformBy = self.zoom
            offsetx = self.origin[0]
            offsety = self.origin[1]
            return ((p[0] - offsetx) * transformBy, (p[1] - offsety) * transformBy)
        else:
            # screen -> world
            transformBy = 1.0 / self.zoom
            offsetx = self.origin[0]
            offsety = self.origin[1]
            return (p[0] * transformBy + offsetx, p[1] * transformBy + offsety)

    def pointWorldToScreen(self, p):
        return self.pointTransform(p, True)
    def pointScreenToWorld(self, p):
        return self.pointTransform(p, False)

    def rectTransform(self, rect, worldToScreen):
        resultTopLeft = self.pointTransform((rect[0], rect[1]), worldToScreen)
        resultWidth = self.valueTransform(rect[2], worldToScreen)
        resultHeight = self.valueTransform(rect[3], worldToScreen)
        return pygame.Rect(resultTopLeft[0], resultTopLeft[1], resultWidth, resultHeight)
    def rectWorldToScreen(self, rect):
        return self.rectTransform(rect, True)
    def rectScreenToWorld(self, rect):
        return self.rectTransform(rect, False)

    # Zoom in or out
    # Will probably pan aswell in order to keep the clicked World position at a constant Screen position
    def changeZoom(self, zoomIn, clickPositionScreen):
        clickPositionWorld_beforeZoom = self.pointScreenToWorld(clickPositionScreen)

        #zoomAmount = self.calcZoomAmount()
        zoomAmount = 0.3
        newZoom = self.zoom + (zoomAmount * (1 if zoomIn else -1))
        newZoomStep = self.zoomStep + (1 if zoomIn else -1)
        #newZoom = self.calcNewZoom(newZoomStep)

        # Single 'zoom' variable is held in zoomHelper
        self.setZoom(newZoom, newZoomStep)
        print("Zoom is now: " + str(self.zoom) + " / step: " + str(self.zoomStep))

        # After the zoom, we want the clickPositionScreen to resolve to the same clickPositionWorld as before the zoom
        # This means we zoom in on the point that the cursor is over when we use the scroll wheel
        clickPositionWorld_afterZoom = self.pointScreenToWorld(clickPositionScreen)
        print("zoom at clickPositionScreen: " + str(clickPositionScreen))
        print("  clickPositionWorld_beforeZoom: " + str(clickPositionWorld_beforeZoom))
        print("  clickPositionWorld_afterZoom: " + str(clickPositionWorld_afterZoom))
        panByWorld = (clickPositionWorld_beforeZoom[0] - clickPositionWorld_afterZoom[0], clickPositionWorld_beforeZoom[1] - clickPositionWorld_afterZoom[1])
        print("  panByWorld: " + str(panByWorld))
        self.panByWorld(panByWorld)

    # TODO: Figure this out
    # def calcNewZoom(self, newZoomStep):
        # if newZoomStep == 1:
        #     return 1
        # if newZoomStep <= 0:
        #     stepsBelow1 = 1 - newZoomStep
        #     return 0.7 + pow(0.8, stepsBelow1)
        # return newZoomStep * 3 * 0.3

    # TODO: Figure this out
    # we currently always use 0.3
    # now we observe:
    # - we need a lower amount if zoom < 1 - we don't want zoom to reach 0
    # - we need a higher amount if zoom > ???
    #def calcZoomAmount(self):
        # return 0.3
        # if self.zoomStep < 1:
        #     return 0.1
        # elif self.zoomStep > 4:
        #     return 3.0
        # else:
        #     return 0.3


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
        # Create sprites
        self.backgroundImage = BackgroundImage()
        pygamehelper.addSprite(self.backgroundImage)
        # Needs to know when zoom level is changed
        zoomHelper.addZoomChangedListener(self.backgroundImage)

        self.selectionTool = SelectionTool(50, 50)
        pygamehelper.addSprite(self.selectionTool)

        # Intro message
        # TODO: Allow multi line strings
        pygamehelper.addSprite(SpriteWithText(30, 30, 200, 30, "Welcome to my editor example", pygamehelper.largeFont, pygamehelper.white).withTimeout(200))
        pygamehelper.addSprite(SpriteWithText(30, 60, 200, 30, "- Left click and drag to draw a rectangle", pygamehelper.largeFont, pygamehelper.white).withTimeout(220))
        pygamehelper.addSprite(SpriteWithText(30, 90, 200, 30, "- Left click inside the rectangle and drag it to move it", pygamehelper.largeFont, pygamehelper.white).withTimeout(240))
        pygamehelper.addSprite(SpriteWithText(30, 120, 200, 30, "- Right click and drag to pan around", pygamehelper.largeFont, pygamehelper.white).withTimeout(260))
        pygamehelper.addSprite(SpriteWithText(30, 150, 200, 30, "- Mouse wheel to zoom in and out", pygamehelper.largeFont, pygamehelper.white).withTimeout(280))

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

    def onClick(self, event):
        # scroll wheel click?
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
                clickPositionScreen = pygame.mouse.get_pos()
                zoomIn = (event.button == 4)
                zoomHelper.changeZoom(zoomIn, clickPositionScreen)


pygamehelper.debug = False
#pygamehelper.fps = 2

# Run game loop
MyGameLoop().runGameLoop()


# Test for pointScreenToWorld then reverse pointWorldToScreen
# zoomHelper.setOrigin((500,500))
# zoomHelper.setZoom(2)
# clickPointScreen = (100,100)
# print("clickPointScreen: " + str(clickPointScreen))
# clickPointWorld = zoomHelper.pointScreenToWorld(clickPointScreen)
# print("clickPointWorld: " + str(clickPointWorld))
# clickPointScreen2 = zoomHelper.pointWorldToScreen(clickPointWorld)
# print("clickPointScreen2: " + str(clickPointScreen2))