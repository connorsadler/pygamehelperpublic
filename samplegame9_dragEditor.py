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
        worldOrigin_screen = zoomHelper.pointWorldToScreen((0,0))
        drawImage(self.zoomedImage, worldOrigin_screen[0], worldOrigin_screen[1])
        self.drawGrid()

    # Draw grid
    # The grid is based on World coords
    # Must take into account zoom level and pan amount
    def drawGrid(self):
        gridSizeWorld = 250
        gridSizeScreen = zoomHelper.valueWorldToScreen(gridSizeWorld)
        #origin = zoomHelper.getOrigin()
        screenTopLeft_world = zoomHelper.pointScreenToWorld((0,0))
        worldOrigin_screen = zoomHelper.pointWorldToScreen((0,0))
        firstGridPosOffset_world = (screenTopLeft_world[0] % gridSizeWorld, screenTopLeft_world[1] % gridSizeWorld)
        firstGridPosOffset_screen = (zoomHelper.valueWorldToScreen(firstGridPosOffset_world[0]), zoomHelper.valueWorldToScreen(firstGridPosOffset_world[1]))

        # These loops work in SCREEN coords - might be better for them to work in WORLD coords
        # e.g. Easier to tell when we're on axis, or to show a different grid colour every 500 world coords
        #      We wouldn't need the checkEqual hack either
        for x in range(0, screenRect.width + int(gridSizeScreen), int(gridSizeScreen)):
            xAlt = x - firstGridPosOffset_screen[0]
            axis = checkEqual(xAlt, worldOrigin_screen[0])
            width = 3 if axis else 2
            drawLine((xAlt, 0), (xAlt, screenRect.height), red if axis else green, width)
        for y in range(0, screenRect.height + int(gridSizeScreen), int(gridSizeScreen)):
            yAlt = y - firstGridPosOffset_screen[1]
            axis = checkEqual(yAlt, worldOrigin_screen[1])
            width = 3 if axis else 2
            drawLine((0, yAlt), (screenRect.width, yAlt), red if axis else green, width)

    def setZoom(self, zoom):
        self.zoom = zoom
        self.zoomedImage = None

# Hack to allow float numbers which are very nearly equal to be treated as equal
def checkEqual(value1, value2):
    if value1 == value2:
        return True
    if abs(value1-value2) < 0.001:
        return True
    return value1 == value2

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
            self.pan(event)

        # dragging - either drawing a rectangle or moving it around
        if event.type == pygame.MOUSEMOTION or (mouseButtonUpOrDown and event.button == 1):
            self.dragHandling(event)


    def pan(self, event):
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

    def setZoom(self, zoom):
        self.zoom = zoom

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
        # origin is in World coords, to allow panning. This is the world coord which will appear at the top left of the screen
        self.origin = (0, 0)

    def setZoom(self, zoom):
        self.zoom = zoom

    def setOrigin(self, origin):
        print("setOrigin: " + str(origin))
        self.origin = origin

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
            # TODO: Check this calc
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

    def setZoom(self, zoom, clickPositionScreen):
        self.zoom = zoom
        print("Zoom is now: " + str(self.zoom))
        self.backgroundImage.setZoom(zoom)
        self.selectionTool.setZoom(zoom)
        zoomHelper.setZoom(self.zoom)

        clickPositionWorld = zoomHelper.pointScreenToWorld(clickPositionScreen)
        print("zoom at clickPositionScreen: " + str(clickPositionScreen) + ", clickPositionWorld: " + str(clickPositionWorld))
        # TODO: Fix this
        # zoomHelper.setPan((100,100))

    def onClick(self, event):
        # scroll wheel click?
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
                clickPositionScreen = pygame.mouse.get_pos()
                zoomBy = 0.3 if event.button == 4 else -0.3
                self.setZoom(self.zoom + zoomBy, clickPositionScreen)


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