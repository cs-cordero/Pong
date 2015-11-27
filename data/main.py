import sys
import os
import pygame as pg
from pygame.locals import *
import random
from . import constants as c
from . import colors
from pygame.locals import *


class Ball:
  def __init__(self,startposx,startposy,color):
    self.width  = c.BALLWIDTH
    self.height = c.BALLHEIGHT
    self.dx = c.BALLSPEEDX * c.DIRECTION[random.randint(0,1)]
    self.dy = c.BALLSPEEDY * c.DIRECTION[random.randint(0,1)]
    self.color = color
    self.ball = pg.Rect(startposx,startposy,self.width,self.height)

  def move(self):
    global GamePoint
    self.ball.left += self.dx
    self.ball.top += self.dy
    # paddle collision
    for paddle in PADDLESLIST:
      if self.ball.colliderect(paddle.paddle):
        # allow complicated 'spin' hits
        if paddle.humanid == 'HUMAN1':
          GameBall.ball.left = paddle.paddle.right + 1
        elif paddle.humanid == 'HUMAN2' or paddle.humanid == 'AI':
          GameBall.ball.right = paddle.paddle.left - 1  
        if paddle.humanid == 'HUMAN1' or paddle.humanid == 'HUMAN2':
          if (paddle.dy > 0 and self.dy >= 0) or (paddle.dy < 0 and self.dy <= 0):  # paddle moving with ball in same direction
            print 'Nice!'
            self.dy += 2 * self.dy / abs(self.dy)  # increase speed
          elif (paddle.dy > 0 and self.dy <= 0) or (paddle.dy < 0 and self.dy >= 0):  # paddle moving against ball in opposite direction
            print 'Great job!'
            self.dy = self.dy * -1 # hit ball in opposite direction
          elif paddle.dy == 0:  # paddle is stationary
            pass # ball continues moving in same direction with no change to speed
        self.dx = self.dx * -1
        c.VOLLEYCOUNT += 1
        if c.VOLLEYCOUNT == 8:
          c.VOLLEYCOUNT = 0
          self.dx = self.dx * 1.2 # when volleycount reaches 8 (or four hits each player, increase speed by 20%)
          self.dy = self.dy * 1.2 # when volleycount reaches 8 (or four hits each player, increase speed by 20%)

    # game board collision
    if (self.ball.top <= GAMEZONE.top):
      self.ball.top = GAMEZONE.top + 1
      self.dy = self.dy * -1
    elif (self.ball.bottom >= GAMEZONE.bottom):
      self.ball.bottom = GAMEZONE.bottom - 1
      self.dy = self.dy * -1
    elif self.ball.left <= GAMEZONE.left:
      self.dx = 0
      self.dy = 0
      self.color = colors.red
      GamePoint = False
      c.PLAYERTWOSCORE += 1
    elif self.ball.right >= GAMEZONE.right:
      self.dx = 0
      self.dy = 0
      self.color = colors.green
      GamePoint = False
      c.PLAYERONESCORE += 1
      #self.dx = self.dx * -1  # One Player Game

class Paddle:
  def __init__(self, startposx, startposy, humanid):
    self.width  = c.PADDLETHICKNESS
    self.height = c.PADDLELENGTH
    self.speed  = c.PADDLESPEED
    self.paddle = pg.Rect(startposx,startposy,self.width,self.height)
    self.humanid = humanid
    self.dy = 0
    PADDLESLIST.append(self)

  def move(self,dy):
    self.dy = dy
    self.paddle.top += self.speed * self.dy

    # check for collision
    if self.paddle.top < GAMEZONE.top: self.paddle.top = GAMEZONE.top
    if self.paddle.bottom > GAMEZONE.bottom: self.paddle.bottom = GAMEZONE.bottom

  def moveAI(self):
    global GameBall
    if GameBall.ball.centery < self.paddle.centery - 2: self.dy = -1  # game ball is above the AI player
    elif GameBall.ball.centery > self.paddle.centery + 2: self.dy = 1 # game ball is below the AI player
    else: self.dy = 0
    self.paddle.top += self.speed * self.dy

    # check for collision
    if self.paddle.top < GAMEZONE.top: self.paddle.top = GAMEZONE.top
    if self.paddle.bottom > GAMEZONE.bottom: self.paddle.bottom = GAMEZONE.bottom

# initialize game
pg.init()
DISPLAYSURF = pg.display.set_mode((c.WINDOWWIDTH,c.WINDOWHEIGHT))
FPSCLOCK = pg.time.Clock()
pg.display.set_caption('Pong!')


def startGame():
  DISPLAYSURF.fill(colors.black)
  GenerateText('First to 7 points wins!', GAMEZONE.centerx, GAMEZONE.centery)
  pg.display.update()
  pg.time.wait(1000)
  DISPLAYSURF.fill(colors.black)
  GenerateText('3', GAMEZONE.centerx, GAMEZONE.centery)
  pg.display.update()
  pg.time.wait(1000)
  DISPLAYSURF.fill(colors.black)
  GenerateText('2', GAMEZONE.centerx, GAMEZONE.centery)
  pg.display.update()
  pg.time.wait(1000)
  DISPLAYSURF.fill(colors.black)
  GenerateText('1', GAMEZONE.centerx, GAMEZONE.centery)
  pg.display.update()
  pg.time.wait(1000)

def drawAssets():
  DISPLAYSURF.fill(colors.black)
  pg.draw.rect(DISPLAYSURF, colors.black, GAMEZONE)
  pg.draw.rect(DISPLAYSURF, colors.white, CENTERLINE)
  GenerateText(repr(c.PLAYERONESCORE), GAMEZONE.centerx - 30, GAMEZONE.top + 25, 45)
  GenerateText(repr(c.PLAYERTWOSCORE), GAMEZONE.centerx + 30, GAMEZONE.top + 25, 45)
  pg.draw.rect(DISPLAYSURF, colors.white, PlayerOne.paddle)
  pg.draw.rect(DISPLAYSURF, colors.white, PlayerTwo.paddle)
  pg.draw.rect(DISPLAYSURF, GameBall.color, GameBall.ball)

def GenerateText(text, posx, posy, size=32):
  fontObj = pg.font.Font('freesansbold.ttf', size)
  textSurfaceObj = fontObj.render(text, True, colors.white, colors.black)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = (posx, posy)
  DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def CheckForOtherInput(restrictions='None'):
  for event in pg.event.get():
    if event.type == QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      pg.quit()
      sys.exit()
    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and restrictions == 'EndGame':
      return False
    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and restrictions != 'EndGame':
      PauseGame('PlayerPaused')
  return True

def PauseGame(type):
  global GameBall
  PauseGame = True
  store_dx = GameBall.dx
  store_dy = GameBall.dy
  GameBall.dx = 0
  GameBall.dy = 0
  if type == 'PointMade1':
    GenerateText('Player One Scored!', GAMEZONE.centerx, GAMEZONE.centery)
    GenerateText('(Press Spacebar to Continue)', GAMEZONE.centerx, GAMEZONE.centery + 60, 18)
  elif type == 'PointMade2':
    GenerateText('Player Two Scored!', GAMEZONE.centerx, GAMEZONE.centery)
    GenerateText('(Press Spacebar to Continue)', GAMEZONE.centerx, GAMEZONE.centery + 60, 18)
  else:
    GenerateText('Game Paused', GAMEZONE.centerx, GAMEZONE.centery)
    GenerateText('(Press Spacebar to Continue)', GAMEZONE.centerx, GAMEZONE.centery + 60, 18)
  pg.display.update()
  while PauseGame:
    for event in pg.event.get():
      if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
        if type == 'PointMade1' or type == 'PointMade2' and GameInProgress == True:
          GameBall  = Ball(GAMEZONE.centerx - c.BALLWIDTH, random.randint(GAMEZONE.top,GAMEZONE.bottom-c.BALLHEIGHT),colors.white)
        PauseGame = False
      elif event.type == QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
  if type != 'PointMade1' and type != 'PointMade2':
    GameBall.dx = store_dx
    GameBall.dy = store_dy


def initializeGame(gameStatus):
  global GAMEZONE, CENTERLINE, PADDLESLIST, PlayerOne, PlayerTwo, GameBall
  # initialize assets
  GAMEZONE = pg.Rect(c.BOUNDARYSIZE, c.BOUNDARYSIZE, c.WINDOWWIDTH - (c.BOUNDARYSIZE * 2), c.WINDOWHEIGHT - (c.BOUNDARYSIZE * 2))
  CENTERLINE = pg.Rect(GAMEZONE.centerx - 1, GAMEZONE.top, 5, GAMEZONE.height)
  PADDLESLIST = []
  PlayerOne = Paddle(GAMEZONE.left + 10, GAMEZONE.top, 'HUMAN1')
  PlayerTwo = Paddle(GAMEZONE.right - c.PADDLETHICKNESS - 10, GAMEZONE.top, 'AI')
  GameBall  = Ball(GAMEZONE.centerx - c.BALLWIDTH, random.randint(GAMEZONE.top,GAMEZONE.bottom-c.BALLHEIGHT),colors.white)
  c.PLAYERONESCORE = 0
  c.PLAYERTWOSCORE = 0
  if PlayerTwo.humanid == 'AI' and gameStatus == 'EASY':
    PlayerTwo.speed = PlayerTwo.speed * .65
  if gameStatus == 'EASY':
    GameBall.dx = GameBall.dx * .70
    GameBall.dy = GameBall.dy * .70
  
def main(gameStatus):
  while True:
    global GameInProgress, GamePoint
    initializeGame(gameStatus)
    startGame()
    GameInProgress = True
    while GameInProgress:
      GamePoint = True
  
      while GamePoint: # main game loop
        drawAssets()
  
        # player controls
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] or key[pg.K_UP]:      PlayerOne.move(-1) # move with multiplier -1.0
        elif key[pg.K_RIGHT] or key[pg.K_DOWN]: PlayerOne.move( 1)  # move with multiplier +1.0
  
        # game commands
        PlayerOne.move(0)
        if PlayerTwo.humanid == 'AI': PlayerTwo.moveAI()
        else: PlayerTwo.move(0)
        GameBall.move()
        CheckForOtherInput()
        pg.display.update()
        FPSCLOCK.tick(c.FPS)
      
        if c.PLAYERTWOSCORE == 7: GameInProgress = False
        elif c.PLAYERONESCORE == 7: GameInProgress = False
  
      # game point made, show final position, then wait for space bar to continue game.
      drawAssets()
      pg.display.update()
      FPSCLOCK.tick(c.FPS)
      if GameBall.color == colors.red:
        PauseGame('PointMade2') # wait for space bar
      if GameBall.color == colors.green:
        PauseGame('PointMade1') # wait for space bar
  
    # match point made, show final position and quit.
    if c.PLAYERONESCORE == 7:
      drawAssets()
      GenerateText('Player One Wins!',  GAMEZONE.centerx, GAMEZONE.centery)
      GenerateText('(Press Spacebar to Restart Game or ESC to Quit)', GAMEZONE.centerx, GAMEZONE.centery + 60, 18)
      pg.display.update()
    elif c.PLAYERTWOSCORE == 7:
      drawAssets()
      GenerateText('Player Two Wins!',  GAMEZONE.centerx, GAMEZONE.centery)
      GenerateText('(Press Spacebar to Restart Game or ESC to Quit)', GAMEZONE.centerx, GAMEZONE.centery + 60, 18)
      pg.display.update()
    EndGame = True
    while EndGame == True:
      EndGame = CheckForOtherInput('EndGame')