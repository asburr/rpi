#!/usr/bin/python3
# Global imports
import time
import unicornhathd


# Global variables
# note,
#  Global vars live forever and remember their value forever.
#  You don't have to use "_g" in their name, but some people like to.
#  Global vars are difficult to debug and are generally avoided and
#  instead use the class construct (see droptheballOOP.py).
white_g = (255,255,255)
black_g = (0,0,0)

# Global code.
# note,
#  This code is run when importing a module such as "import droptheball", also
#  it is run when running the module as a script such as "python3 droptheball.py"
#  Global code is difficult to debug and generally avoided and instead use
#  the class construct (see droptheballOOP.py)
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
