# Constants for Pong Game
import random

# Game Constants
FPS = 60

# Window Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BOUNDARYSIZE = 25

# Paddle Constants
PADDLELENGTH = 100
PADDLETHICKNESS = 8
PADDLESPEED = WINDOWHEIGHT / FPS  # should take 1 second to get from the top to the bottom.

# Ball Constants
BALLWIDTH = 15
BALLHEIGHT = 15

BALLSPEEDDEBUG = WINDOWHEIGHT / (FPS / 2)

DIRECTION = (-1,1)
BALLSPEEDX = WINDOWWIDTH  / (FPS / 0.5)
BALLSPEEDY = WINDOWHEIGHT / (FPS / 1.0)

VOLLEYCOUNT = 0

PLAYERONESCORE = 0
PLAYERTWOSCORE = 0