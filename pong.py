# Coded by Christopher Sabater Cordero, Washington DC

import sys
import os
import pygame as pg
from data.constants import *
from data.colors import *
from pygame.locals import *

pg.init()
DISPLAYSURF = pg.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pg.display.set_caption('Hello World!')
fpsClock = pg.time.Clock()

while True: # main game loop
  DISPLAYSURF.fill(black)
  # set player paddle location
  playerRect = pg.Rect(PLAYERPADDLEX,PLAYERPADDLEY,PADDLETHICKNESS,PADDLELENGTH)
  pg.draw.rect(DISPLAYSURF, white, playerRect)
  
  for event in pg.event.get():
    if event.type == QUIT:
      pg.quit()
      sys.exit()
    pressed = pg.key.get_pressed()
    if pressed[pg.K_UP] or pressed[pg.K_LEFT]:
      if PLAYERPADDLEY > 10:
        PLAYERPADDLEY -= 1
    elif pressed[pg.K_DOWN] or pressed[pg.K_RIGHT]:
      if PLAYERPADDLEY < WINDOWHEIGHT - PADDLELENGTH - 10:
        PLAYERPADDLEY += 1  
  pg.display.update()
  fpsClock.tick(FPS)