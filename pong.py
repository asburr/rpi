import sys
import colorsys
import pygame.gfxdraw
import pygame
import random
import time

class pong():
  def __init__(self, width, height):
    self.AUTO = None
    self.PHAT = None
    self.pixel_size = 15
    self.width = width
    self.height = height
    self.window_width = width * self.pixel_size
    self.window_height = height * self.pixel_size
    self.white = (255,255,255)
    self.black = (0,0,0)
    self.red = (255,0,0)
    self.green = (0,255,0)
    self.paddle = (width/2,0)
    self.ball = {"from": (round(width/2),height-1)}
    self.ball["pos"] = self.ball["from"]
    self.newTarget()
    print("Your bet is $10")
    self.money = 10

    pygame.init()
    pygame.key.set_repeat(1) # held keys repeatedly generate an event every 1ms.
    pygame.display.set_caption(f"${self.money}")
    self.screen = pygame.display.set_mode(
      [self.window_width, self.window_height])

  def newTarget(self):
    (fx,fy) = self.ball["from"]
    (tx,ty) = self.ball["from"]
    while (tx == fx):
      (tx,ty) = (random.randint(0,self.width-1),0)
    #print(f"{fx},{fy}>{tx},{ty}")
    self.gx = (fx-tx) / (ty-fy)
    self.gy = -1.0
    #print(f"{self.gx} {self.gy}")
    return (tx,ty)

  def moveBall(self):
    """ Ball moves on a trajectory, bounce when hit the wall. """
    (px,py) = self.ball["pos"]
    px += self.gx
    py += self.gy
    if px <= 0 or px > (self.width-1):
      if px <= 0:
        px = 0
      if px > (self.width-1):
        px = self.width-1
      if self.gx > 0:
        self.gx = -self.gx
      else:
        self.gx = abs(self.gx)
    if py < 0 or py > (self.height-1):
      if py < 0:
        py = 0
      if py > (self.height-1):
        py = self.height-1
      if self.gy > 0:
        self.gy = -self.gy
      else:
        self.gy = abs(self.gy)
      #print(f"{self.gx} {self.gy}")
    self.ball["pos"] = (px,py)

  def run(self):
    pause = False
    while True:
      sleep = .1
      (x,y) = self.paddle
      self.draw_led(x,y,self.black)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            x -= 1
            if x < 0:
              x = 0
          elif event.key == pygame.K_RIGHT:
            x += 1
            if x > self.width-1:
              x = self.width-1
          elif event.key == pygame.K_p:
            pause = True
          elif event.key == pygame.K_r:
            pause = False
      if pause:
        time.sleep(.3)
        continue
      self.paddle = (x,y)
      self.draw_led(x,y,self.white)
      (px,py) = self.ball["pos"]
      self.draw_led(px,py,self.black)
      self.moveBall()
      (px,py) = self.ball["pos"]
      if py == 0:
        if round(px) != x:
          self.draw_led(px,py,self.red)
          self.money -= 1
          sleep = .3
        else:
          self.draw_led(px,py,self.green)
          self.money += 1
          sleep = .3
        pygame.display.set_caption(f"${self.money}")
      else:
        self.draw_led(px,py,self.white)
      pygame.display.update()
      time.sleep(sleep)
      if self.money == 0:
        print("House wins, you lost $10")
        sys.exit()
      if self.money == 20:
        print("You win $20")
        sys.exit()

  def draw_led(self, x, y,color):
    p = self.pixel_size
    w_x = int(x * p + self.pixel_size / 2)
    w_y = int((self.height - 1 - y) * p + self.pixel_size / 2)
    r = int(self.pixel_size / 4)
    pygame.gfxdraw.aacircle(self.screen, w_x, w_y, r, color)
    pygame.gfxdraw.filled_circle(self.screen, w_x, w_y, r, color)

  def get_shape(self):
    return (self.width, self.height)

  def brightness(self, *args):
    pass

  def set_layout(self, *args):
      pass

  def off(self):
      pygame.quit()

p = pong(16,16)
p.run()
