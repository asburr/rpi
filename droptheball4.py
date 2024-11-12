#!/usr/bin/python3
""" This module demonstrates a solution for drop the drop the ball using "for" loops and "range". The solution is two lines shorter than droptheball.py, but the major benefit is the for loop is a single line of code containg all of the logic. This style of coding is favoured by data scientists and mathematicians. """
"""

import time
import unicornhathd

white_g = (255,255,255)
black_g = (0,0,0)

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
