#!/usr/bin/python3
import time
import unicornhathd


white = (255,255,255)
black = (0,0,0)

unicornhathd.brightness(0.2)
(width,height) = unicornhathd.get_shape()

ymax = height - 1

x = 0

for bounce in range(ymax,0,-2):
  for y in range(0,ymax,1):
    unicornhathd.set_pixel(x,y,*white)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x,y,*black)
  for y in range(ymax,0,-1):
    unicornhathd.set_pixel(x,y,*white)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x,y,*black)
