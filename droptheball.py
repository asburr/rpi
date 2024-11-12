#!/usr/bin/python3
# "#!" allow this file to run on the command line, in this case, passing the file to python3 which will run the code.

""" This module demonstates a novice solution to a simulation of dropping a ball from the top of the led hat to the bottom and then bounce the ball back up to the top agan, and repeating forever. "while" is the least complicated loop. """
# Docstring starts with """ and ends with """. It is standard practise to have docstrings for Modules, classes and functions.
# Docstring is shown by help(module or class or function). String at the top of a file are module docstrings, for example,
#  >>>import droptheball
#  <control-c>
#  >>>help(droptheball)
#  Help on module droptheball
#  NAME droptheball - This module simulates dropping a ball from the top of the led hat to the bottom and then bounce the ball back up to the top, repeating forever.

import time
# This is the module time.py. Time.py is part of the standard packages of modules installed when Python is installed. Importing a module is
# with an intent to use a function from the module, for example, time.sleep() is used below. Knowing what standard modules are available is
# part of learning the Python language, this knowledge is somewhat transferable to other other programming languages, for example, "C" and Java
# have similar time modules.

import unicornhathd
# This is the module "unicornhathd.py". unicornhathd.py is not a standard module, it is provided by the manufacturer of the led device.
# Advanced note: unicornhathd was added to the Python environment using the Package Installer for Python (called pip).
# for example, "pip install unicornhathd". Packages contain one or more modules and additional information such as
# dependencies.  pip install will resolve dependencies i.e. it will automatically install modules needed by unicornhathd.

white_g = (255,255,255)
black_g = (0,0,0)
# Global vars keep their value while the program/script is running.
# You don't have to use "_g" in their name, but some people like to.
# Global vars can be used anywhere which makes them ideal for small programs, but troublesome for larger programs.
# Larger program should hide as local variables inside functions or instance variables in classes. Hidden data
# is accessed via functions with a well defined parameter and return value and no access to the variables themselves.

unicornhathd.brightness(0.2)
# Brightness is written by somebody else and resides in the unicornhathd module.
# Python has a help function, for example,
#    >>>help(unicornhathd.brightness)
#    brightness(b=0.2), set the display brightness between 0.0 and 1.0.
#    0.2 is recommended, hat can get painfully bright!
#    :param b: Brightness 0.0 to 1.0 (default 0.2)"
# Advanced notes: help shows the functions docstring which is manually written.

(width_g,height_g) = unicornhathd.get_shape()
# get_shape is another function in unicornhathd, for example,
#    >>> help(unicornhathd.get_shape)
#    Returns the shape (width, height) of the display
# Advanced notes: get_shape returns a Tuple. A Tuple contains two values. Equals and perentheses converts the Tuple to
#       two variables named width_g and height_g. Returning Tuples is error prone, Consider transposing the names
#       "(height_g,width_g)=h.get_shape()". Alternative: a/ individual functions, h.get_width() and h.get_height();
#       or b/ return a dictionary type with keys "width" and "height".

ymax_g = height_g - 1 # range of y (in set_pixel) is 0 to height-1.
x_g = 0
y_g = ymax_g
while True: # Loop forever, user has to hit control-c to interrupt this program!
  while y_g > 0: # Drop the ball.
    unicornhathd.set_pixel(x_g,y_g,*white_g) # Switch off the previous location of the ball.
    unicornhathd.show() # Update the hat display with all of the led settings made up to this point.
    time.sleep(.1) # Wait 100 milliseconds which is 0.1 second.
    unicornhathd.set_pixel(x_g,y_g,*black_g) #  Switch on the new location of the ball.
    y_g -= 1 # Move ball downwards by one led.
  while y_g < ymax_g: # Bounce the ball.
    unicornhathd.set_pixel(x_g,y_g,*white_g)
    unicornhathd.show()
    time.sleep(.1)
    unicornhathd.set_pixel(x_g,y_g,*black_g)
    y_g += 1 # Move ball upwards by one led.
