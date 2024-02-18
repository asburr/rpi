import sys
import random
import time
from game import game

class midway(game):
  """ Simplified version of Midway. Must run run as root when using unicornhat. Points in the left column... """
  SKY_CLEAR = 0
  SKY_PLANE = 1
  SKY_BULLET = 2
  SKY_USERBULLET = 3
  SKY_HIT = -1
  BULLET_DISTANCE = 3 # Distance a bullet travels.
  def __init__(self, width, height):
    super().__init__("MIDWAY",width, height)
    self.planes = {} # Map of plane x&y to amo.
    self.bullets = {} # Map bullet x&y to remaining distance.
    self.userbullets = {} # Map bullet x&y to remaining distance.
    self.sky={} # Track what is happening in the sky.
    self.ticks = 0
    self.newplane_tick = 20
    self.moveplane_tick = 9
    self.movebullet_tick = 3
    self.movement()

  def movement(self) -> (bool,int):
    """ Planes fly streight down, so no change to x-axis. Randomly the plane will send a burst of random shots. The shots travel twice as fast as the planes and also move streight down.
        Generates new plane(s) from the top when the sky is somewhat empty and there is still a path from the user's plane through the sky.
        Return True when user's plane has crashed into something, and count of user hits. """
    userhit = False
    userhits = 0

    self.ticks += 1
    self.sky={} # Clear the sky

    if (self.ticks % self.newplane_tick) == 0:
      # Generate a plane.
      plane = (random.randint(0,self.width),self.height-1)
      if not plane in self.planes:
        self.planes[plane] = random.randint(0,round(self.height/2))

    if (self.ticks % self.moveplane_tick) == 0:
      # Move planes
      newplanes = {} # build new dict to prevent clashing old and new planes.
      for plane,amo in self.planes.items():
        if self.sky.get(plane,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.draw_led(*plane,self.black)
        (x,y) = plane
        if y == 0: # Already at the bottom of the screen, nowhere to go.
          continue
        y -= 1 # Planes move down.
        x += random.randint(-1,1) # Planes can move left or right.
        if x < 0: # But not off the left edge.
          x += 1
        if x == self.width: # And not off the right edge.
          x -= 1
        plane = (x,y)
        if self.sky.get(plane,self.SKY_CLEAR) == self.SKY_PLANE:
          del newplanes[plane]
          del self.sky[plane]
          self.draw_led(*plane,self.red)
          continue
        if plane == self.user:
          self.draw_led(*self.user,self.red)
          userhit = True
          continue
        self.sky[plane] = self.SKY_PLANE
        newplanes[plane]=amo
        self.draw_led(*plane,self.yellow)
      self.planes = newplanes
    else:
      # Add planes to the sky.
      for plane in self.planes.keys():
        self.sky[plane] = self.SKY_PLANE

    if (self.ticks % self.movebullet_tick) == 0:
      # Bullets move downwards.
      newbullets = {}
      for bullet,distance in self.bullets.items():
        if not distance:
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.draw_led(*bullet,self.black)
        (x,y) = bullet
        y -= 1
        if y < 0:
          continue
        bullet = (x,y)
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_BULLET:
          del self.sky[bullet]
          del newbullets[bullet]
          self.draw_led(*bullet,self.red)
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_PLANE:
          del self.sky[bullet]
          del self.planes[bullet]
          self.draw_led(*bullet,self.red)
          continue
        self.sky[bullet] = self.SKY_BULLET
        newbullets[bullet] = 0
        self.draw_led(*bullet,self.green)
        y -= 1
        if y < 0:
          continue
        bullet = (x,y)
        distance -= 1
        if not distance:
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_BULLET:
          del self.sky[bullet]
          del newbullets[bullet]
          self.draw_led(*bullet,self.red)
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_PLANE:
          del self.sky[bullet]
          del self.planes[bullet]
          self.draw_led(*bullet,self.red)
          continue
        self.sky[bullet] = self.SKY_BULLET
        newbullets[bullet] = distance
        self.draw_led(*bullet,self.green)
      self.bullets = newbullets
    else:
      # Add bullets to the sky.
      for bullet in self.bullets.keys():
        self.sky[bullet] = self.SKY_BULLET

    if (self.ticks % self.movebullet_tick) == 0:
      # User bullets move upwards
      newuserbullets = {}
      for bullet,distance in self.userbullets.items():
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.draw_led(*bullet,self.black)
        (x,y) = bullet
        y += 1
        if y == self.height:
          continue
        bullet = (x,y)
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_BULLET:
          del self.sky[bullet]
          del self.bullets[bullet]
          self.draw_led(*bullet,self.red)
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_USERBULLET:
          del self.sky[bullet]
          del newuserbullets[bullet]
          self.draw_led(*bullet,self.red)
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_PLANE:
          del self.sky[bullet]
          del self.planes[bullet]
          self.draw_led(*bullet,self.red)
          userhits += 1
          continue
        self.sky[bullet] = self.SKY_USERBULLET
        self.draw_led(*bullet,self.green)
        distance -= 1
        if not distance:
          continue
        y += 1
        if y == self.height:
          continue
        bullet = (x,y)
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_BULLET:
          del self.sky[bullet]
          del self.bullets[bullet]
          self.draw_led(*bullet,self.red)
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_USERBULLET:
          del self.sky[bullet]
          del newuserbullets[bullet]
          self.draw_led(*bullet,self.red)
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_PLANE:
          del self.sky[bullet]
          del self.planes[bullet]
          self.draw_led(*bullet,self.red)
          userhits += 1
          continue
        distance -= 1
        if not distance:
          continue
        self.sky[bullet] = self.SKY_USERBULLET
        self.draw_led(*bullet,self.green)
        self.userbullets[bullet] = distance
      self.userbullets = newuserbullets
    else:
      # Add userbullets to the sky.
      for bullet in self.userbullets.keys():
        self.sky[bullet] = self.SKY_USERBULLET

    if (self.ticks % self.movebullet_tick) == 0:
      # Planes with amo can fire one bullet in this movement.
      for plane in [plane for plane in self.planes.keys() if self.planes[plane] > 0]:
        if plane not in self.planes:
          continue
        amo = self.planes[plane]
        self.planes[plane] = amo - 1
        (x,y) = plane
        bullet = (x-1,y)
        if bullet == self.user:
          self.draw_led(*bullet,self.red)
          userhit = True
          continue
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.sky[bullet] = self.SKY_BULLET
          self.bullets[bullet] = self.BULLET_DISTANCE
          self.draw_led(*bullet,self.green)
          continue
        else:
          self.draw_led(*bullet,self.red)
          del self.sky[bullet]
          if bullet in self.planes:
            del self.planes[bullet]
          if bullet in self.bullets:
            del self.bullets[bullet]
          if bullet in self.userbullets:
            del self.userbullets[bullet]
          continue

    return (userhit,userhits)

  def run(self):
    """ Run until game is lost. """
    pause = False
    while True:
      sleep = .1
      if self.userInput():
        self.userbullets[self.user] = self.BULLET_DISTANCE
      if self.pause:
        continue
      (userhit,userhits) = self.movement()
      if userhit:
        self.points -= .5
        sleep = .3
      if userhits:
        self.points += (.5*userhits)
        sleep = .3
      self.check_points()
      time.sleep(sleep)

p = game.factory(midway)
