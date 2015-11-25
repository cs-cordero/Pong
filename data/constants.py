# Constants for Pong Game
import random

# Game Constants
FPS = 60

# Window Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BOUNDARYSIZE = 25

# Paddle Constants
PADDLELENGTH = 75
PADDLETHICKNESS = 10
PLAYER1PADDLEX = BOUNDARYSIZE + 5
PLAYER1PADDLEY = BOUNDARYSIZE + 5
PLAYER1PADDLESPEED = WINDOWHEIGHT / FPS  # should take 1 second to get from the top to the bottom.
PLAYER2PADDLEX = WINDOWWIDTH - BOUNDARYSIZE - PADDLETHICKNESS - 5
PLAYER2PADDLEY = BOUNDARYSIZE + 5
PLAYER2PADDLESPEED = WINDOWHEIGHT / FPS  # should take 1 second to get from the top to the bottom.

# Ball Constants
BALLWIDTH = 15
BALLHEIGHT = 15
BALLX = (WINDOWWIDTH / 2) - (BALLWIDTH/2) # centered ball start
BALLY = random.randint(BOUNDARYSIZE,WINDOWHEIGHT-BOUNDARYSIZE-BALLHEIGHT) # random ball start
BALLSPEEDDEBUG = WINDOWHEIGHT / (FPS / 2)
DIRECTION = (-1,1)
BALLSPEEDX = (WINDOWWIDTH  / (FPS / 0.5))*(DIRECTION[random.randint(0,1)]) # random direction start
BALLSPEEDY = (WINDOWHEIGHT / (FPS / 1.0))*(DIRECTION[random.randint(0,1)]) # random direction start