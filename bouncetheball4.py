#!/usr/bin/python3
""" This modules demonstrates the improved readability when using an outer "for" loop to bounce the ball in bouncetheball.py. """

import time
import unicornhathd

white = (255,255,255)
black = (0,0,0)

unicornhathd.brightness(0.2)
(width,height) = unicornhathd.get_shape()

x = 0
ymax = height - 1

for bounce in range(ymax,0,-2):
  for y in range(0,bounce,1):
    unicornhathd.set_pixel(x,y,*white)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x,y,*black)
  for y in range(bounce,0,-1):
    unicornhathd.set_pixel(x,y,*white)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x,y,*black)
