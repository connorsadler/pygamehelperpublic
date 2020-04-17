import pygamehelper as pygamehelper
import random
from pygamehelper import *

#
# Breakout
#

pygamehelper.initPygame()

# A brick in the wall of bricks
class Block(Sprite):
    def __init__(self, x, y, colour):
        super().__init__(x, y, 50, 20)
        self.colour = colour
        self.collisionDetectionEnabled = True

    def move(self):
        pass

    def handleCollisions(self, collidedWithSprites):
        # TODO
        pass

    def draw(self):
        pygame.draw.rect(pygamehelper.gameDisplay, self.colour, Rect(self.x, self.y, 50, 20), 0)

class Ball(Sprite):
    def __init__(self):
        super().__init__(getScreenRect().width/2, getScreenRect().height-60, 10, 10)
        self.direction = math.pi + math.pi /3 * random.random()
        self.speed = 5
        self.dx = math.sin(self.direction)*self.speed
        self.dy = math.cos(self.direction)*self.speed
        self.r = 10
        self.colour = (0,0,0)

        # This will mean "bounceOnEdgeOfScreen" is called when we hit the edge of the screen
        self.edgeOfScreenChecker = BounceSprite_EdgeOfScreenChecker()
        # This will mean "handleCollisions" is called when we collide with something
        self.collisionDetectionEnabled = True

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(pygamehelper.gameDisplay, self.colour, (int(self.x), int(self.y)), self.r, 0)

    def bounceOnEdgeOfScreen(self):
        if (self.x<=20 and self.dx < 0) or (self.x>=getScreenRect().width - 20 and self.dx > 0):
            self.dx *= -1
        if self.y < 10:
            self.dy *= -1
        # If the ball goes off the bottom, kill it and show 'Get Ready' to spawn a new ball
        if self.y > getScreenRect().height - 20:
            pygamehelper.addSprite(GetReadyMessage())
            self.dead = True

    def handleCollisions(self, collidedWithSprites):
        # Collided with bat or block?
        collidedWithSprite = collidedWithSprites[0]
        if isinstance(collidedWithSprite, Block):
            # Block hit - bounce ball up, and destroy block
            self.dy *= -1
            collidedWithSprite.dead = True
            # TODO: Scoring
            #score += 10
            #if score % 50 == 0:
            #    self.dy*= 1.25
            #    self.dx *= 1.25
        else:
            # Bat hit
            bat = collidedWithSprite
            self.dy *= -1
            if self.x - bat.x < -20 or self.x - bat.x > 20:
                self.dx *= -1
            pass

# Says "Get Ready" for a while, then dies and spawns a new Ball
# TODO: Make this generic
class GetReadyMessage(Sprite):
    def __init__(self):
        super().__init__(getScreenRect().width/2, getScreenRect().height/2, 10, 10)
        self.health = 100
        self.colour = red

    def move(self):
        self.y += 0.5
        self.health -= 1
        if self.health == 0:
            self.dead = True
            pygamehelper.game.spawnBall()

    def draw(self):
        drawText("Get Ready", self.x - 60, self.y, pygamehelper.hugeFont, self.colour)

class Bat(Sprite):
    def __init__(self):
        super().__init__(getScreenRect().width/2, getScreenRect().height-20, 60, 3)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.x > 40:
            self.x -= 10
        if pressed_keys[K_RIGHT] and self.x < getScreenRect().width - 60:
            self.x += 10
        
    def draw(self):
        super().draw()

# Game loop logic
class MyGameLoop(GameLoop):

    def __init__(self):
        super().__init__()

        # Init blocks of different colours
        i = 0
        for y in range(50, 250, 50):
            for x in range(25, 360, 60):
                pygamehelper.addSprite(Block(x, y, colours[i]))
            i += 1

        # Init ball
        self.spawnBall()
        # Init bat
        pygamehelper.addSprite(Bat())

    def spawnBall(self):
        pygamehelper.addSprite(Ball())

# Run game loop
MyGameLoop().runGameLoop()
