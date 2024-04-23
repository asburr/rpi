#!/usr/bin/python3
# Global imports.
# notes,
#  "import time" => make-available everything from the time module.
#  "as tm" => imports the time module with the name "tm" instead of "time"
#  for example, "time.sleep(1)" becomes "tm.sleep(1)".
import time as tm

# Global variables
white_g = (255,255,255)
black_g = (0,0,0)

# global function
def dropTheBallF():
    # local imort
    # notes,
    #  A local import is within a function.
    from unicornhathd import set_pixel, get_shape, show, brightness
    # global variables
    # notes,
    #  "global" => creates a global variable and in this case it refers to
    #  the above global variables. Global variable are available to other
    #  functions, they do not vanish once the function returns.
    global white_g
    global black_g
    # notes,
    #  the above "from import" imports a limited number of functions and/or
    #  variables that are added to the function's namespace i.e. invoked without the
    #  module name such as "brighness()" rather than "unicornhathd.brightness".
    brightness(0.2)
    # local variables
    # notes,
    #  width and height and ymax and x, are local variables. local vars are
    #  newly created each time the function is called, they are only available
    #  to this function, they vanish once the function returns.
    (width,height) = get_shape()
    ymax = height - 1
    x = 0   
    while True:
      for y in range(0,ymax,1):
        set_pixel(x,y,*white_g)
        show()
        # module time is imported at the top of the module and is then global.
        tm.sleep(.1)
        set_pixel(x,y,*black_g)
      for y in range(ymax,0,-1):
        set_pixel(x,y,*white_g)
        show()
        tm.sleep(.1)
        set_pixel(x,y,*black_g)

# Global code
if __name__ == "__main__":
  # notes,
  #  Put code here that is called when the module is run as a script,
  #  such as "python3 droptheballF.py". 
  dropTheBallF()
else:
  # notes,
  #  Put code here that is called when the module is imported,
  #  such as "import droptheballF".
  #  "pass" means do nothing. Pass is used when a condition is expected
  #  to be used in the future, but is not used currently.
  pass
