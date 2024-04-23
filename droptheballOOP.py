#!/usr/bin/python3
# Global imports.
import time
import unicornhathd


# class
# notes,
#  "class" defines a thing as a collection of functions and/or variables.
#  Class can be easier to maintain due to all of the functions are variables
#  being encapsulated (collected together) in the class, for example, to change
#  the colour of the ball is a one line change in the show() method.
class Ball():
  # note,
  #  The string after "class" is the description for the class that is output
  #  by help(Ball).
  """ Remember ball's position, providing methods to move, show and hide the ball. """
  # Class variables.
  # note,
  #  Accessible by "Ball.white" and also "self.white".
  white = (255,255,255)
  black = (0,0,0)
  
  # constructor
  # notes,
  #  "__init__" is called when a Ball is created, for example, "ball = Ball(x=0,y=0)".
  #  "self" is the thing, so in this case "self" is the ball.
  def __init__(self,x,y):
    self.x = 0
    self.y = 0
    self.move(x,y)
    self.show()

  # functions

  def move(self,x,y):
    # note,
    #  The following string (after each function/variable) is a description
    #  that is output by help(Ball.move).
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

  # static function
  # note,
  #  "staticmethod" declares a regular function. Note that "self" is missing
  #  because this is a regular function and is invoked by "Ball.main()".
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

  # class function
  # note,
  #  "classmethod" also declares a regular function, invoked by "Ball.main_cls()".
  #  "cls" is "Ball"
  @classmethod
  def main_cls(cls):
    """ This function calls main() and is a demo of a classmethod. """
    cls.main()

# Global code
if __name__ == "__main__":
    Ball.main()
else:
    Ball.main_cls()
