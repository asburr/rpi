#!/usr/bin/python3
# Global imports
import time
import unicornhathd

# Global variables
white_g = (255,255,255)
black_g = (0,0,0)

# Global code.
unicornhathd.brightness(0.2)
(width_g,height_g) = unicornhathd.get_shape()
ymax_g = height_g - 1
x_g = 0

while True:
  for y_g in range(0,ymax_g,1):
    unicornhathd.set_pixel(x_g,y_g,*white_g)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x_g,y_g,*black_g)
  for y_g in range(ymax_g,0,-1):
    unicornhathd.set_pixel(x_g,y_g,*white_g)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x_g,y_g,*black_g)
