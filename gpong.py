import sys
import random
import time
from game import game


class pong(game):
  """ Simplified version of pong. Must run run as root when using unicornhat. Points in the left column, and the ball bounces on the remaining tiles, with a one-pixel paddle on the first row which can be moved left or right using the j and k keys. The paddle turns red when the paddle misses the ball and points drop by .5, green when the paddle hits the ball and points increase by .5. Points increase up to height of the unicornhat when the user wins. Points decrease to zero when the user has lost. """
  def __init__(self, width, height):
    super.__init(width,height)
    self.ball = {"from": (round(width/2),height-1)}
    self.ball["pos"] = self.ball["from"]
    self.newTarget()

  def newTarget(self):
    """ Generates a new target location for the ball that is not streight down. """
    (fx,fy) = self.ball["from"]
    (tx,ty) = self.ball["from"]
    while (tx == fx):
      (tx,ty) = (random.randint(0,self.width-1),0)
    self.gx = (fx-tx) / (ty-fy)
    self.gy = -1.0
    return (tx,ty)

  def moveBall(self):
    """ Ball moves on a trajectory, bounce off the wall. """
    (px,py) = self.ball["pos"]
    px += self.gx
    py += self.gy
    if px <= 0 or px > (self.width-1):
      if px <= 0:
        px = 1
      if px > (self.width-1):
        px = self.width-1
      if self.gx > 0:
        self.gx = -self.gx
      else:
        self.gx = abs(self.gx)
    if py < 0 or py > (self.height-1):
      if py < 0:
        py = 1
      if py > (self.height-1):
        py = self.height-1
      if self.gy > 0:
        self.gy = -self.gy
      else:
        self.gy = abs(self.gy)
    self.ball["pos"] = (px,py)

  def run(self):
    """ Run until game is lost. """
    self.pause = False
    while True:
      sleep = .1
      self.userInput()
      if pause:
        continue
      (px,py) = self.ball["pos"]
      self.draw_led(px,py,self.black)
      self.moveBall()
      (px,py) = self.ball["pos"]
      if py == 0:
        if round(px) != self.user[0]:
          self.draw_led(px,py,self.red)
          self.points -= .5
          sleep = .3
        else:
          self.draw_led(px,py,self.green)
          self.points += .5
          sleep = .3
        self.draw_points()
      else:
        self.draw_led(px,py,self.white)
      self.check_points()
      time.sleep(sleep)

game.factory(pong)
