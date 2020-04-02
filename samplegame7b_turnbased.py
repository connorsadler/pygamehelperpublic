import pygamehelper
from pygamehelper import *
import pygame, math

#
# Starting point for a TURN BASED pygame game
# Shows you how to:
# - keep track of who's turn it is
# - keep score for two players
# - add to the score for the current player
#
# TODO: Possible features to add:
# - countdown timer so each player only has a certain amount of time to play their move
# - some boxes could reduce the other players score rather than increase your score
# - players could start with 200 score and if their score gets to 0 then they lose
#


# Global init
pygamehelper.initPygame()

#
# TODO
# Define any sprites you want in here - Make them subclasses of Sprite or SpriteWithImage
#

#
# GridHelper
# - Manages a group of sprites on a grid
# - Draws the grid
# - Converts rowIdx,columnIndex to screen coords
# 
class GridHelper(Sprite):
    def __init__(self):
        super().__init__(100, 100, 5, 5)
        # The size of each cell
        self.cellSize = 50
        # The number of rows and columns in the grid
        self.numRows = 8
        self.numColumns = 8
        # Which sprites are on the grid
        self.gridPieces = []

    def addGridPiece(self, sprite):
        self.gridPieces.append(sprite)

    def move(self):
        pass

    # Get the top left hand corner of a cell in SCREEN COORDS
    def getCellPoint(self, rowIdx, columnIdx):
        return (self.x + columnIdx * self.cellSize, self.y + rowIdx * self.cellSize)

    # Get the rect of a cell in SCREEN COORDS
    def getCellRect(self, rowIdx, columnIdx):
        cellPoint = self.getCellPoint(rowIdx, columnIdx)
        return pygame.Rect(cellPoint[0], cellPoint[1], self.cellSize - 2, self.cellSize - 2)

    # Is a proposed row,col within the grid bounds?
    def isCellOnGrid(self, rowIdx, columnIdx):
        return rowIdx >= 0 and rowIdx < self.numRows and columnIdx >= 0 and columnIdx < self.numColumns

    def draw(self):
        # Draw the grid
        for y in range(0, self.numRows):
            for x in range(0, self.numColumns):
                cellRect = self.getCellRect(x,y)
                drawRect(cellRect, green)

    def onClick(self):
        pass

    def clearHighlights(self):
        for gridPiece in self.gridPieces:
            gridPiece.clearHighlight()

#
# GridPieceBase
# Exists in a particular cell of a grid
# 
class GridPieceBase(Sprite):
    def __init__(self, gridHelper, rowIdx, columnIdx):
        super().__init__(0, 0, gridHelper.cellSize, gridHelper.cellSize)
        self.gridHelper = gridHelper
        self.gridHelper.addGridPiece(self)
        self.rowIdx = rowIdx
        self.columnIdx = columnIdx
        self.highlight = False

    def move(self):
        cellPoint = self.gridHelper.getCellPoint(self.rowIdx, self.columnIdx)
        self.x = cellPoint[0]
        self.y = cellPoint[1]

    def draw(self):
        if self.highlight:
            drawRect(self.getBoundingRect(), green, 4)

    def onClick(self):
        pass

    def clearHighlight(self):
        self.highlight = False

#
# GridPiece
# Exists in a particular cell of a grid
# 
class GridPiece(GridPieceBase):
    def __init__(self, gridHelper, rowIdx, columnIdx):
        super().__init__(gridHelper, rowIdx, columnIdx)
        self.moveTargets = []
        self.mover = None

    def move(self):
        if self.mover == None:
            super().move()
        else:
            framesLeft = self.mover.moveFrame()
            if not framesLeft:
                # End move animation
                self.mover = None

    def draw(self):
        super().draw()
        drawText("X", self.x + 15, self.y + 12, pygamehelper.largeFont, white)

    def onClick(self):
        print("click")
        # Unhighlight everything else
        self.gridHelper.clearHighlights()
        # Highlight this piece
        self.highlight = not self.highlight
        # Show move targets - these are the spaces this piece can possibly move to
        self.moveTargets = [ ]
        self.addMoveTargetMaybe(self.rowIdx - 1, self.columnIdx)
        self.addMoveTargetMaybe(self.rowIdx - 1, self.columnIdx - 1)
        self.addMoveTargetMaybe(self.rowIdx - 1, self.columnIdx + 1)
        self.addMoveTargetMaybe(self.rowIdx + 1, self.columnIdx)
        self.addMoveTargetMaybe(self.rowIdx + 1, self.columnIdx - 1)
        self.addMoveTargetMaybe(self.rowIdx + 1, self.columnIdx + 1)
        self.addMoveTargetMaybe(self.rowIdx, self.columnIdx - 1)
        self.addMoveTargetMaybe(self.rowIdx, self.columnIdx + 1)

    def addMoveTargetMaybe(self, rowIdx, columnIdx):
        if self.gridHelper.isCellOnGrid(rowIdx, columnIdx):
            moveTarget = MoveTarget(self, self.gridHelper, rowIdx, columnIdx)
            self.moveTargets.append(moveTarget)
            addSprite(moveTarget)

    def clearHighlight(self):
        super().clearHighlight()
        # Also destroy any MoveTargets for this piece
        for moveTarget in self.moveTargets:
            moveTarget.dead = True

    # Complete move by a player
    def movePieceTo(self, moveToRowIdx, moveToColumnIdx):
        self.clearHighlight()

        # animate the move to the new cell screen position
        newCellPoint = self.gridHelper.getCellPoint(moveToRowIdx, moveToColumnIdx)
        self.mover = GridPieceMover(self, newCellPoint[0], newCellPoint[1], 20)
        # set new row/col now for the piece - it's UI will catch up quickly as the move animation takes place
        self.rowIdx = moveToRowIdx
        self.columnIdx = moveToColumnIdx
        game.endTurn()

#
# Animates a move from one grid square to another
#
class GridPieceMover:
    def __init__(self, targetOfMove, moveToX, moveToY, numFrames):
        self.targetOfMove = targetOfMove
        # FROM -> TO
        self.moveFromX = targetOfMove.x
        self.moveFromY = targetOfMove.y
        self.moveToX = moveToX
        self.moveToY = moveToY
        # Amount to move each frame
        self.dx = (self.moveToX - self.moveFromX) / numFrames
        self.dy = (self.moveToY - self.moveFromY) / numFrames
        # Number of frames to move for until we're done
        self.framesLeft = numFrames

    def moveFrame(self):
        self.targetOfMove.moveBy(self.dx, self.dy)
        self.framesLeft = self.framesLeft - 1
        return self.framesLeft > 0

#
# MoveTarget
# Exists in a particular cell of a grid
# Denotes target square for a possible move for a GridPiece
# If clicked, we'll move the original piece to this square
# 
class MoveTarget(GridPieceBase):
    def __init__(self, targetOfMove, gridHelper, rowIdx, columnIdx):
        super().__init__(gridHelper, rowIdx, columnIdx)
        self.highlight = True
        self.targetOfMove = targetOfMove

    def onClick(self):
        print("click move target")
        self.targetOfMove.movePieceTo(self.rowIdx, self.columnIdx)

    def clearHighlight(self):
        # Always highlight move targets
        pass

#
# Scorecard for a player
# We'll create an instance of this per player
#
class PlayerScore():
    def __init__(self):
        self.score = 0
        self.misses = 0

    def registerScore(self, scoreValue):
        self.score += scoreValue

    def registerMiss(self):
        self.misses += 1

#
# Turnkeeper
# Keeps track of who's turn it is currently, and allows the game to move to the next player
# Currently there are only 2 players
# 
class Turnkeeper(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, screenRect.width/2, 10)
        # set to either 1 or 2 depending on who's turn it is
        self.currentPlayerNumber = 1
        # scores for each player
        self.playerScores = {
            1: PlayerScore(),
            2: PlayerScore()
        }

    def move(self):
        pass

    def draw(self):
        # Show who's turn it is
        drawText("Player " + str(self.currentPlayerNumber) + "'s turn", self.x, self.y, pygamehelper.hugeFont, green)
        # Show scores
        self.drawScore(1, 575, 30)
        self.drawScore(2, 575, 50)

    def drawScore(self, playerNumber, x, y):
        scorecard = self.playerScores[playerNumber]
        drawText("Player " + str(playerNumber) + "  score: " + str(scorecard.score) + "  misses: " + str(scorecard.misses), x, y, pygamehelper.mediumFont, white)

    def endTurn(self):
        self.currentPlayerNumber = 2 if self.currentPlayerNumber == 1 else 1
        print("self.currentPlayerNumber is now: " + str(self.currentPlayerNumber))

    # grab the object which holds scores for the current player
    def getCurrentPlayerScore(self):
        return self.playerScores[self.currentPlayerNumber]

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

        # Draws the grid
        self.gridHelper = GridHelper()
        pygamehelper.addSprite(self.gridHelper)
        # Create a couple of boxes which will bounce around
        # pygamehelper.addSprite(Box(20, 20, 110))
        # pygamehelper.addSprite(Box(20, 300, 45))
        # object to keep track of turns
        self.turnKeeper = Turnkeeper(140, 20)
        pygamehelper.addSprite(self.turnKeeper)

        pygamehelper.addSprite(GridPiece(self.gridHelper, 0,0))
        pygamehelper.addSprite(GridPiece(self.gridHelper, 1,1))

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        # spawn a new square at random
        # if random.randint(1,1000) > 975:
        #     pygamehelper.addSprite(Box(randomX()-20, randomY()-20, randomDirection()))
        pass

    def onEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #self.gridHelper.clearHighlights()

            clickPosition = pygame.mouse.get_pos()
            clickedSprites = findSprites(clickPosition)
            if len(clickedSprites) > 0:
                # scoring click
                for clickedSprite in clickedSprites:
                    clickedSprite.onClick()
            # else:
            #     # non-scoring (missing) click
            #     self.turnKeeper.getCurrentPlayerScore().registerMiss()
            
            # ??? end turn on every click, whether they hit anything or not - switch turn to other player
            # game.endTurn()

    def registerScoreForCurrentPlayer(self, scoreValue):
        self.turnKeeper.getCurrentPlayerScore().registerScore(scoreValue)

    def endTurn(self):
        self.turnKeeper.endTurn()

#pygamehelper.debug = False

# Run game loop
game = MyGameLoop()
game.runGameLoop()
