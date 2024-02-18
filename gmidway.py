import sys
import random
import time
from game import game

class midway(game):
  """ Simplified version of Midway. Must run run as root when using unicornhat. Points in the left column... """
  SKY_CLEAR = 0
  SKY_PLANE = 1
  SKY_BULLET = 2
  SKY_HIT = -1
  BULLET_DISTANCE = 3 # Distance a bullet travels.
  def __init__(self, width, height):
    super.__init__(width, height)
    self.planes = {} # Map of plane x&y to amo.
    self.bullets = {} # Map bullet x&y to remaining distance.
    self.userbullets = {} # Map bullet x&y to remaining distance.
    self.sky={} # Track what is happening in the sky.
    self.movement()

  def movement(self) -> (bool,int):
    """ Planes fly streight down, so no change to x-axis. Randomly the plane will send a burst of random shots. The shots travel twice as fast as the planes and also move streight down. """
        Generates new plane(s) from the top when the sky is somewhat empty and there is still a path from the user's plane through the sky.
        Return True when user's plane has crashed into something, and count of user hits. """
    userhit = False
    userhits = 0

    self.sky={} # Clear the sky

    # Generate a plane.
    plane = (0,random.randint(0,self.width))
    if not plane in self.planes:
      self.planes(plane) = random.randint(0,round(self.height/2))

    # Move planes
    for plane in [self.planes.keys()]:
      amo = self.plane[plane]
      del self.plane[plane]
      if self.sky.get(plane,SKY_CLEAR) == SKY_CLEAR:
        self.draw_led(*plane,self.black)
      (x,y) = plane
      if x == 0:
        continue
      x -= 1 # Planes move down.
      y += random.randint(-1,1) # Planes can move left or right.
      if y < 0: # But not off the left edge.
        y += 1
      if y == self.width: # And not off the right edge.
        y -= 1
      plane = (x,y)
      if self.sky.get(plane,SKY_CLEAR) != SKY_CLEAR: # Colliding planes.
        del self.planes[plane]
        self.sky[plane] = SKY_HIT
        self.draw_led(*plane,self.red)
        continue
      self.sky[plane] = SKY_PLANE
      if plane == self.user:
        self.draw_led(*self.user,self.red)
        userhit = True
        continue
      self.draw_led(*plane,self.white)
      self.planes[plane]=amo

    # Bullets move downwards.
    for bullet in [self.bullets.keys()]:
      distance = self.bullets[bullet]
      del self.bullets[bullet]
      if self.sky.get(bullet,SKY_CLEAR) == SKY_CLEAR:
        self.draw_led(*bullet,self.black)
      (x,y) = bullet
      y --
      if y < 0:
        continue
      bullet = (x,y)
      if self.sky.get(bullet,SKY_CLEAR) == SKY_BULLET:
        del self.bullets[bullet]
        self.draw_led(*bullet,self.red)
        continue
      if self.sky.get(bullet,SKY_CLEAR) == SKY_PLANE:
        del self.planes[bullet]
        self.draw_led(*bullet,self.red)
        continue
      self.sky[bullet] = SKY_BULLET
      self.draw_led(*bullet,self.green)
      distance -= 1
      if not distance:
        continue
      y --
      if y < 0:
        continue
      bullet = (x,y)
      if self.sky.get(bullet,SKY_CLEAR) == SKY_BULLET:
        del self.bullets[bullet]
        self.draw_led(*bullet,self.red)
        continue
      if self.sky.get(bullet,SKY_CLEAR) == SKY_PLANE:
        del self.planes[bullet]
        self.draw_led(*bullet,self.red)
        continue
      self.sky[bullet] = SKY_BULLET
      self.draw_led(*bullet,self.green)
      distance -= 1
      if not distance:
        continue
      self.bullets[bullet] = distance

    # User bullets move upwards
    for bullet in [self.userbullets.keys()]:
      distance = self.userbullets[bullet]
      del self.userbullets[bullet]
      if self.sky.get(bullet,SKY_CLEAR) == SKY_CLEAR:
        self.draw_led(*bullet,self.black)
      (x,y) = bullet
      y ++
      if y == self.height:
        continue
      bullet = (x,y)
      if self.sky.get(bullet,SKY_CLEAR) == SKY_BULLET:
        del self.userbullets[bullet]
        self.draw_led(*bullet,self.red)
        continue
      if self.sky.get(bullet,SKY_CLEAR) == SKY_PLANE:
        del self.planes[bullet]
        self.draw_led(*bullet,self.blue)
        userhits ++
        continue
      self.sky[bullet] = SKY_BULLET
      self.draw_led(*bullet,self.green)
      distance -= 1
      if not distance:
        continue
      y ++
      if y == self.height:
        continue
      bullet = (x,y)
      if self.sky.get(bullet,SKY_CLEAR) == SKY_BULLET:
        del self.userbullets[bullet]
        self.draw_led(*bullet,self.red)
        continue
      if self.sky.get(bullet,SKY_CLEAR) == SKY_PLANE:
        del self.planes[bullet]
        self.draw_led(*bullet,self.blue)
        userhits ++
        continue
      self.sky[bullet] = SKY_BULLET
      self.draw_led(*bullet,self.green)
      distance -= 1
      if not distance:
        continue
      self.userbullets[bullet] = distance

    # Planes with amo can fire one bullet in this movement.
    for plane in [plane for plane in self.planes.keys() if self.planes[plane] > 0]:
      amo = self.planes[plane]
      self.planes[plane] = amo - 1
      (x,y) = plane
      bullet = (x-1,y)
      if bullet == self.user:
        self.draw_led(*bullet,self.red)
        userhit = True
        continue
      if self.sky.get(bullet,SKY_CLEAR) == SKY_CLEAR:
        self.bullets[bullet] = BULLET_DISTANCE
        self.draw_led(*bullet,self.green)
        continue
      else:
        self.draw_led(*bullet,self.red)
        if bullet in self.planes:
          del self.planes[bullet]
        if bullet in self.bullets:
          del self.bullets[bullet]
        self.sky[bullet] = SKY_HIT
        continue

    return (userhit,userhits)

  def run(self):
    """ Run until game is lost. """
    pause = False
    while True:
      sleep = .1
      if self.userInput():
        self.userbullets[self.user] = BULLET_DISTANCE
      if self.pause:
        continue
      (userhit,userhits) = self.movement()
      if userhit:
        self.points -= .5
        sleep = .3
      if userhits:
        self.points += (.5*userhits)
        sleep = .3
      self.check_points(sleep)

p = game.factory(midway)
