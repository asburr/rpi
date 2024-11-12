#!/usr/bin/python3
""" This modules demonstrates changing dropthe ball.py to have the ball bounce after being dropped. """
import time
import unicornhathd

white = (255,255,255)
black = (0,0,0)

unicornhathd.brightness(0.2)
(width,height) = unicornhathd.get_shape()

ymax = height - 1

x = 0
y = ymax
bounce = ymax
while bounce:
  while y > 0:
    unicornhathd.set_pixel(x,y,*black)
    y -= 1
    unicornhathd.set_pixel(x,y,*white)
    unicornhathd.show()
    time.sleep(.1)
  while y < bounce:
    unicornhathd.set_pixel(x,y,*black)
    y += 1
    unicornhathd.set_pixel(x,y,*white)
    unicornhathd.show()
    time.sleep(.1)
  bounce -= 2
