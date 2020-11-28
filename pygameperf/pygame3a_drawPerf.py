import pygame
import time

# 
# Uses standard pygame drawing (no sprite stuff) with a list of sprite instances
# 
# Draws 20000 'sprites' (rectangles) each frame
# Runs for 5 seconds
# Then shows how many frames per second we managed to draw
# 

# Example results:

# 
# Connor's Macbook 1 - Tiny sprite rectangles
# --------------------------------------------------
# Settings:
#   Number of sprites:  20000
#   Run for seconds:  5
#   Sprite rectangle size:  1
# Results:
#   Game frames:  267
#   Frames per second:  53.4
# --------------------------------------------------
# 
# Connor's Macbook 2 - Small sprite rectangles
# --------------------------------------------------
# Settings:
#   Number of sprites:  20000
#   Run for seconds:  5
#   Sprite rectangle size:  3
# Results:
#   Game frames:  123
#   Frames per second:  24.6
# --------------------------------------------------
# 
# Connor's Macbook 3 - larger sprite rectangles
# --------------------------------------------------
# Settings:
#   Number of sprites:  20000
#   Run for seconds:  5
#   Sprite rectangle size:  10
# Results:
#   Game frames:  102
#   Frames per second:  20.4
# --------------------------------------------------
# 
# 

RUN_FOR_SECONDS = 5
SPRITE_NUM_COLUMNS = 20
SPRITES_PER_COLUMN = 1000
SPRITE_RECTANGLE_SIZE = 1



pygame.init()
clock = pygame.time.Clock()

# Set up the drawing window
display_width = 1000
display_height = 1000
screen = pygame.display.set_mode([display_width, display_height])

# Run until the user asks to quit
running = True
gameTick = 0

black = (0,0,0)
white = (255,255,255)
defaultFont = pygame.font.SysFont(None, 12)

# build our sprite list - it's just a simple list of rectangles
sprites = []
for x in range(0, SPRITE_NUM_COLUMNS):
    for y in range(0,SPRITES_PER_COLUMN):
        sprites.append([x,y,SPRITE_RECTANGLE_SIZE,SPRITE_RECTANGLE_SIZE])
    
print("Number of sprites: ", len(sprites))

def drawText(text, x, y, font, colour):
    t = font.render(text, True, colour)
    screen.blit(t, (x, y))

startTime = time.time()
print("startTime: ", startTime)
while running:
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw each sprite
    for sprite in sprites:
        pygame.draw.rect(screen, black, sprite, 2)
        # move every sprite right to make the test more interesting to look at
        sprite[0] += 1

    drawText("gameTick: " + str(gameTick), 10, 30, defaultFont, black)
    drawText("sprites count: " + str(len(sprites)), 10, 50, defaultFont, black)

    # Flip the display
    pygame.display.flip()

    clock.tick(100)
    gameTick += 1

    # check if done
    elapsedSeconds = time.time() - startTime
    if (elapsedSeconds) > RUN_FOR_SECONDS:
        running = False

print("--------------------------------------------------")
print("Settings:")
print("  Number of sprites: ", len(sprites))
print("  Run for seconds: ", RUN_FOR_SECONDS)
print("  Sprite rectangle size: ", SPRITE_RECTANGLE_SIZE)
print("Results:")
print("  Game frames: ", gameTick)
print("  Frames per second: ", (gameTick/RUN_FOR_SECONDS))
print("--------------------------------------------------")

# Done! Time to quit.
pygame.quit()

