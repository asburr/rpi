import sys
import colorsys
import random
import time

usePYGAME=True
if usePYGAME:
  import pygame.gfxdraw
  import pygame
else:
  import unicornhat
  import tty, sys, termios, select

class pong():
  """ Simplified version of pong. Must run run as root when using unicornhat. Points in the left column, and the ball bounces on the remaining tiles, with a one-pixel paddle on the first row which can be moved left or right using the j and k keys. The paddle turns red when the paddle misses the ball and points drop by .5, green when the paddle hits the ball and points increase by .5. Points increase up to height of the unicornhat when the user wins. Points decrease to zero when the user has lost. """
  def __init__(self, width, height):
    self.width = width-1 # Last column is the points
    self.height = height
    self.white = (255,255,255)
    self.black = (0,0,0)
    self.red = (255,0,0)
    self.green = (0,255,0)
    self.paddle = (width/2,0)
    self.ball = {"from": (round(width/2),height-1)}
    self.ball["pos"] = self.ball["from"]
    self.newTarget()
    self.points = int(self.height/2)
    if usePYGAME:
      self.pixel_size = 15
      self.window_width = width * self.pixel_size
      self.window_height = height * self.pixel_size
      pygame.init()
      # pygame.key.set_repeat(1) # held keys repeatedly generate an event every 1ms.
      pygame.display.set_caption("PONG")
      self.screen = pygame.display.set_mode([self.window_width, self.window_height])
    else:
      unicornhat.brightness(0.2)
      self.oldStdinSettings = termios.tcgetattr(sys.stdin)
      tty.setcbreak(sys.stdin)

  def __reset__(self):
    if usePYGAME:
      pass
    else:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldStdinSettings)

  def newTarget(self):
    """ Generates a new target location for the ball that is not streight down. """
    (fx,fy) = self.ball["from"]
    (tx,ty) = self.ball["from"]
    while (tx == fx):
      (tx,ty) = (random.randint(0,self.width-1),0)
    self.gx = (fx-tx) / (ty-fy)
    self.gy = -1.0
    return (tx,ty)

  def moveBall(self):
    """ Ball moves on a trajectory, bounce off the wall. """
    (px,py) = self.ball["pos"]
    px += self.gx
    py += self.gy
    if px <= 0 or px > (self.width-1):
      if px <= 0:
        px = 1
      if px > (self.width-1):
        px = self.width-1
      if self.gx > 0:
        self.gx = -self.gx
      else:
        self.gx = abs(self.gx)
    if py < 0 or py > (self.height-1):
      if py < 0:
        py = 1
      if py > (self.height-1):
        py = self.height-1
      if self.gy > 0:
        self.gy = -self.gy
      else:
        self.gy = abs(self.gy)
    self.ball["pos"] = (px,py)

  def isStdin(self):
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

  def run(self):
    """ Run until game is lost. """
    pause = False
    while True:
      sleep = .1
      self.draw_led(*self.paddle,self.black)
      if usePYGAME:
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
              sys.exit()
            if event.key == pygame.K_j:
              x = self.paddle[0]
              x -= 1
              if x < 0:
                x = 0
              self.paddle=(x,0)
            elif event.key == pygame.K_k:
              x = self.paddle[0]
              x += 1
              if x > self.width-1:
                x = self.width-1
              self.paddle=(x,0)
            elif event.key == pygame.K_p:
              pause = True
            elif event.key == pygame.K_r:
              pause = False
      else:
        while self.isStdin():
          event = sys.stdin.read(1)
          if event == 'q':
            sys.exit()
          elif event == "k":
            x = self.paddle[0]
            x -= 1
            if x < 0:
              x = 0
            self.paddle=(x,0)
          elif event == "j":
            x = self.paddle[0]
            x += 1
            if x > self.width-1:
              x = self.width-1
            self.paddle=(x,0)
          elif event == 'p':
            pause = True
          elif event == 'r':
            pause = False
      self.draw_led(*self.paddle,self.white)
      if pause:
        pygame.display.update()
        time.sleep(.3)
        continue
      (px,py) = self.ball["pos"]
      self.draw_led(px,py,self.black)
      self.moveBall()
      (px,py) = self.ball["pos"]
      if py == 0:
        if round(px) != self.paddle[0]:
          self.draw_led(px,py,self.red)
          self.points -= .5
          sleep = .3
        else:
          self.draw_led(px,py,self.green)
          self.points += .5
          sleep = .3
        color = self.green
        if (self.points < (self.height/2)):
          color = self.red
        for y in range(0,self.height):
          if y < self.points:
            self.draw_led(self.width,y,color)
          else:
            self.draw_led(self.width,y,self.black)
      else:
        self.draw_led(px,py,self.white)
      if usePYGAME:
        pygame.display.update()
      else:
        unicornhat.show()
      time.sleep(sleep)
      if self.points == 0:
        print(f"Computer won")
        self.__reset__()
        sys.exit()
      if self.points >= self.height:
        print(f"You won")
        self.__reset__()
        sys.exit()

  def draw_led(self, x, y, color):
    """ RPI unicornhat LED display """
    if usePYGAME:
      p = self.pixel_size
      w_x = int(x * p + self.pixel_size / 2)
      w_y = int((self.height - 1 - y) * p + self.pixel_size / 2)
      r = int(self.pixel_size / 4)
      pygame.gfxdraw.aacircle(self.screen, w_x, w_y, r, color)
      pygame.gfxdraw.filled_circle(self.screen, w_x, w_y, r, color)
    else:
      unicornhat.set_pixel(round(x),round(y),color)

if usePYGAME:
  (width,height) = (8,8)
else:
  (width,height) = unicornhat.get_shape()
p = pong(width,height)
try:
  p.run()
finally:
  p.__reset__()
