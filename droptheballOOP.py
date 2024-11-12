#!/usr/bin/python3
""" This module demonstrates a solution for drop the drop the ball using object oriented programming i.e. class. OOP is used when creating large programs that need maintaining, in general, OOP is favoured by computer scientists. """
import time
import unicornhathd


# "class" defines a collection of functions to manage hidden data. The hidden data is the last coordiates
# of the ball and the color of the ball.
# 
class Ball():
  # docstring for the class, help(Ball) will show this docstring.
  """ Remember ball's position, providing methods to move, show and hide the ball. """

  # class variables may be shown by Ball.white and Ball.black.
  white = (255,255,255)
  black = (0,0,0)
  
  # construtor, this creates an object from the Ball class. Note that "self" is the ball.
  def __init__(self,x,y):
    self.x = 0
    self.y = 0
    self.move(x,y)
    self.show()

  def move(self,x,y):
    """ Move ball to new coordinates. """
    # docstring for function, help(Ball.move) will show this docstring.
    self.x = x
    self.y = y

  def show(self):
    """ Show ball at current position. """
    unicornhathd.set_pixel(self.x,self.y,*self.white)
    unicornhathd.show()

  def hide(self):
    """ Hide ball at current position. """
    unicornhathd.set_pixel(self.x,self.y,*self.black)

  # static function declares a regular function inside the class. Note that self is missing
  # because this is a regular function and is invoked by Ball.main().
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

  # class function also declares a regular function within the class. It is also invoked by
  # Ball.main_cls(). The difference is the parameter "cls" which in this case is "Ball".
  @classmethod
  def main_cls(cls):
    """ This function calls main() and is a demo of a classmethod. """
    cls.main()

# The above code creates the class called Ball, but does not create balls.
# The code below uses __name__ which equals "__main__" whenever this file is running as a Unix command i.e. "./droptheballOOP.py",
# or when it is run from python i.e. "python -c droptheballOOP.py". In which case, this code will call main() which will create a ball.
if __name__ == "__main__":
    Ball.main()
