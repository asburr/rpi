#!/usr/bin/python3
import time
import unicornhathd


white_g = (255,255,255)
black_g = (0,0,0)

unicornhathd.brightness(0.2)
(width_g,height_g) = unicornhathd.get_shape()
ymax_g = height_g - 1 # range of y (in set_pixel) is 0 to height-1.
x_g = 0
y_g = ymax_g
while True:
  while y_g > 0:
    unicornhathd.set_pixel(x_g,y_g,*white_g)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x_g,y_g,*black_g)
    y_g -= 1
  while y_g < ymax_g:
    unicornhathd.set_pixel(x_g,y_g,*white_g)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x_g,y_g,*black_g)
    y_g += 1
