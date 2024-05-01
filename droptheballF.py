#!/usr/bin/python3
import time as tm

white_g = (255,255,255)
black_g = (0,0,0)

def dropTheBallF():
    from unicornhathd import set_pixel, get_shape, show, brightness
    global white_g
    global black_g
    brightness(0.2)
    (width,height) = get_shape()
    ymax = height - 1
    x = 0   
    while True:
      for y in range(0,ymax,1):
        set_pixel(x,y,*white_g)
        show()
        tm.sleep(.1)
        set_pixel(x,y,*black_g)
      for y in range(ymax,0,-1):
        set_pixel(x,y,*white_g)
        show()
        tm.sleep(.1)
        set_pixel(x,y,*black_g)

if __name__ == "__main__":
  dropTheBallF()
else:
  pass
