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
# SelectionHelper - Copied from HighlightDrawer
# TODO: ??? Can be animated i.e. growing and shrinking
#
class SelectionHelper:
    def __init__(self, selectionColour, animated):
        self.selectionColour = selectionColour
        self.counter = 1
        self.animated = animated
        self.selected = False

    def setSelected(self, val):
        self.selected = val
    
    def isSelected(self):
        return self.selected

    # def move(self):
    #     self.counter += 1
    #     if self.counter >= 100:
    #         self.counter = 1

    def draw(self, sprite):
        if self.selected:
            if self.animated:
                # TODO: Need a better algorithm for this growing and shrinking - can experiment in samplegame0_playground.py
                #thickness = max(1, round(self.counter % 60 / 8))
                thickness = round((self.counter / 10) % 5 + 1) * 2
            else:
                thickness = 3
            drawRect(sprite.getBoundingRect(), self.selectionColour, thickness)

    def onClick(self, sprite):
        self.selected = not self.selected

    def reset(self):
        self.counter = 0

#
# Card
# 
class Card(SpriteWithImage):
    def __init__(self, x, y, cardNumber):
        super().__init__(x, y, SpriteSheetImageHandler("images/bash2.png"))
        self.setCostume(cardNumber)
        self.setDrawMode(DrawMode.XY_IS_UPPER_LEFT)
        self.selectionHelper = SelectionHelper(red, False)

    def draw(self):
        drawRect(self.boundingRect, white, 2)
        super().draw()
        self.selectionHelper.draw(self)

    def onClick(self):
        self.selectionHelper.onClick(self)

    def moveTo(self, pos):
        pass

    def isSelected(self):
        return self.selectionHelper.isSelected()
    def setSelected(self, selected):
        self.selectionHelper.setSelected(selected)

#
# Slot
# 
class Slot(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 85, 90)

    def move(self):
        pass

    def draw(self):
        drawRect(self.boundingRect, green, 2)

    def onClick(self):
        # If any cards have been selected, move them to this slot  (exclude if they're already in this slot)
        selectedCards = findSpritesByCondition(lambda sprite : isinstance(sprite, Card) and sprite.isSelected() and not sprite.isOverlapping(self))
        print("selectedCards: " + str(selectedCards))
        # Move them all here
        for selectedCard in selectedCards:
            selectedCard.setSelected(False)
            selectedCard.setLocationAnimated(self.getLocation())

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

        # List of Cards
        addSprite(Card(50, 50, 1))
        addSprite(Card(50, 200, 2))
        # List of Slots to move cards to
        for i in range(5):
            addSprite(Slot(200, 20 + (i * 100)))

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
