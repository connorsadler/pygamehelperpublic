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
# A Box moves around the screen
# and bounces
# It has a scoreValue which is what you'll score if you click on it
# 
class Box(Sprite):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 70, 70)
        self.angle = angle
        self.setBounceOfEdgeOfScreen()
        self.scoreValue = random.randint(1, 100)

    def move(self):
        self.moveForward(1)

    def draw(self):
        super().draw() # draws a white rectangle for this sprite
        drawText(str(self.scoreValue), self.x + 20, self.y + 20, pygamehelper.largeFont, red)

    def onClick(self):
        game.registerScoreForCurrentPlayer(self.scoreValue)
        self.dead = True

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

        # Create a couple of boxes which will bounce around
        pygamehelper.addSprite(Box(20, 20, 110))
        pygamehelper.addSprite(Box(20, 300, 45))
        # object to keep track of turns
        self.turnKeeper = Turnkeeper(140, 20)
        pygamehelper.addSprite(self.turnKeeper)

    #
    # TODO
    # This gets called on every frame, before any sprites have been moved or drawn
    # Perform any global game logic here
    #
    def eachFrame(self):
        # spawn a new square at random
        if random.randint(1,1000) > 975:
            pygamehelper.addSprite(Box(randomX()-20, randomY()-20, randomDirection()))

    def onEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()
            clickedSprites = findSprites(clickPosition)
            if len(clickedSprites) > 0:
                # scoring click
                for clickedSprite in clickedSprites:
                    clickedSprite.onClick()
            else:
                # non-scoring (missing) click
                self.turnKeeper.getCurrentPlayerScore().registerMiss()
            # end turn on every click, whether they hit anything or not - switch turn to other player
            game.endTurn()

    def registerScoreForCurrentPlayer(self, scoreValue):
        self.turnKeeper.getCurrentPlayerScore().registerScore(scoreValue)

    def endTurn(self):
        self.turnKeeper.endTurn()

pygamehelper.debug = False

# Run game loop
game = MyGameLoop()
game.runGameLoop()
