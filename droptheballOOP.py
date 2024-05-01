#!/usr/bin/python3
import time
import unicornhathd


class Ball():
  """ Remember ball's position, providing methods to move, show and hide the ball. """
  white = (255,255,255)
  black = (0,0,0)
  
  def __init__(self,x,y):
    self.x = 0
    self.y = 0
    self.move(x,y)
    self.show()

  def move(self,x,y):
    """ Move ball to new coordinates. """
    self.x = x
    self.y = y

  def show(self):
    """ Show ball at current position. """
    unicornhathd.set_pixel(self.x,self.y,*self.white)
    unicornhathd.show()

  def hide(self):
    """ Hide ball at current position. """
    unicornhathd.set_pixel(self.x,self.y,*self.black)

  @staticmethod
  def main():
    """ Continueously drops the ball. """
    unicornhathd.brightness(0.2)
    (width,height) = unicornhathd.get_shape()
    ymax = height - 1
    x = 0
    ball = Ball(0,0)
    while True:
      for y in range(0,ymax,1):
        ball.move(x,y)
        ball.show()
        time.sleep(.1)
        ball.hide()
      for y in range(ymax,0,-1):
        ball.move(x,y)
        ball.show()
        time.sleep(.1)
        ball.hide()

  @classmethod
  def main_cls(cls):
    """ This function calls main() and is a demo of a classmethod. """
    cls.main()

# Global code
if __name__ == "__main__":
    Ball.main()
else:
    Ball.main_cls()
