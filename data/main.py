import sys
import os
import pygame as pg
from . import constants as c
from . import colors
from pygame.locals import *

pg.init()
DISPLAYSURF = pg.display.set_mode((c.WINDOWWIDTH,c.WINDOWHEIGHT))
pg.display.set_caption('Pong')
fpsClock = pg.time.Clock()

def player1Controls(p1paddleY, gameStatus, key):
  # for debugging
  if gameStatus == 'DEBUG':
    if key[pg.K_w]:
      if c.BALLY > c.BOUNDARYSIZE: c.BALLY = max(c.BALLY - c.BALLSPEED, c.BOUNDARYSIZE)
      else: c.BALLY = c.BOUNDARYSIZE
    elif key[pg.K_s]:
      if c.BALLY < c.WINDOWHEIGHT - c.BALLHEIGHT - c.BOUNDARYSIZE: c.BALLY = min(c.BALLY + c.BALLSPEED, c.WINDOWHEIGHT - c.BALLHEIGHT - c.BOUNDARYSIZE)
      else: c.BALLY = c.WINDOWHEIGHT - c.BALLHEIGHT - c.BOUNDARYSIZE
    elif key[pg.K_a]:
      if c.BALLX > c.BOUNDARYSIZE: c.BALLX = max(c.BALLX - c.BALLSPEED, c.BOUNDARYSIZE)
      else: c.BALLX = c.BOUNDARYSIZE
    elif key[pg.K_d]:
      if c.BALLX < c.WINDOWWIDTH - c.BALLWIDTH - c.BOUNDARYSIZE: c.BALLX = min(c.BALLX + c.BALLSPEED, c.WINDOWWIDTH - c.BALLWIDTH - c.BOUNDARYSIZE)
      else: c.BALLX = c.WINDOWWIDTH - c.BALLWIDTH - c.BOUNDARYSIZE

  # player controls
  if key[pg.K_UP] or key[pg.K_LEFT]:
    if p1paddleY > c.BOUNDARYSIZE: return max(p1paddleY - c.PLAYER1PADDLESPEED, c.BOUNDARYSIZE)
    else: return c.BOUNDARYSIZE
  elif key[pg.K_DOWN] or key[pg.K_RIGHT]:
    if p1paddleY < c.WINDOWHEIGHT - c.PADDLELENGTH - c.BOUNDARYSIZE: return min(p1paddleY + c.PLAYER1PADDLESPEED, c.WINDOWHEIGHT - c.PADDLELENGTH - c.BOUNDARYSIZE)
    else: return c.WINDOWHEIGHT - c.PADDLELENGTH - c.BOUNDARYSIZE
  else: return p1paddleY
  

def computerAI(ballY, p2paddleY):
  if ballY + c.BALLHEIGHT/2 > p2paddleY + c.PADDLELENGTH/2:
    if p2paddleY < c.WINDOWHEIGHT - c.PADDLELENGTH - c.BOUNDARYSIZE: return min(p2paddleY + c.PLAYER2PADDLESPEED, c.WINDOWHEIGHT - c.PADDLELENGTH - c.BOUNDARYSIZE)
    else: return c.WINDOWHEIGHT - c.PADDLELENGTH - c.BOUNDARYSIZE
  elif ballY + c.BALLHEIGHT/2 < p2paddleY + c.PADDLELENGTH/2:
    if p2paddleY > c.BOUNDARYSIZE: return max(p2paddleY - c.PLAYER2PADDLESPEED, c.BOUNDARYSIZE)
    else: return c.BOUNDARYSIZE
  else: return ballY

def main(gameStatus):
  while True: # main game loop
    DISPLAYSURF.fill(colors.black)
  
    # set player paddle location
    player1Rect = pg.Rect(c.PLAYER1PADDLEX,c.PLAYER1PADDLEY,c.PADDLETHICKNESS,c.PADDLELENGTH)
    player2Rect = pg.Rect(c.PLAYER2PADDLEX,c.PLAYER2PADDLEY,c.PADDLETHICKNESS,c.PADDLELENGTH)
    ball = pg.Rect(c.BALLX, c.BALLY, c.BALLWIDTH, c.BALLHEIGHT)
    pg.draw.rect(DISPLAYSURF, colors.white, player1Rect)
    pg.draw.rect(DISPLAYSURF, colors.white, player2Rect)
    pg.draw.rect(DISPLAYSURF, colors.white, ball)
  
    pressed = pg.key.get_pressed()
    c.PLAYER1PADDLEY = player1Controls(c.PLAYER1PADDLEY, gameStatus, pressed) 
    c.PLAYER2PADDLEY = computerAI(c.BALLY, c.PLAYER2PADDLEY)
  
    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
    pg.display.update()
    fpsClock.tick(c.FPS)