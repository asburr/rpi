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
    self.sleep = .1
    self.newplane_tick = 10
    self.moveplane_tick = 5
    self.movebullet_tick = 2
    self.moveuserbullet_tick = 2
    self.movement()

  def movement(self) -> (bool,int):
    """ Planes fly streight down, so no change to x-axis. Randomly the plane will send a burst of random shots. The shots travel twice as fast as the planes and also move streight down.
        Generates new plane(s) from the top when the sky is somewhat empty and there is still a path from the user's plane through the sky.
        Return True when user's plane has crashed into something, and count of user hits. """
    userhit = False
    userhits = 0

    self.ticks += 1

    # Clear the hits from the sky.
    for pos,thing in self.sky.items():
      if thing == self.SKY_HIT:
       self.draw_led(*pos,self.black)

    self.sky={}

    if self.newplane_tick > 0 and self.ticks % self.newplane_tick == 0:
      # Generate a plane.
      plane = (random.randint(0,self.width),self.height-1)
      if not plane in self.planes:
        self.planes[plane] = random.randint(0,round(self.height/2))

    if self.moveplane_tick > 0 and self.ticks % self.moveplane_tick == 0:
      # Move planes
      newplanes = {} # build new dict to prevent clashing old and new planes.
      for plane,amo in self.planes.items():
        if self.sky.get(plane,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.draw_led(*plane,self.black)
        (x,y) = plane
        if y == 0: # Already at the bottom of the screen, nowhere to go.
          continue
        y -= 1 # Planes move down.
        ux = self.user[0]
        if random.randint(0,2) == 1: # Move towards user
          if ux > x:
            x += random.randint(0,1)
          if ux < x:
            x -= random.randint(0,1)
        else: # Move away from user.
          if ux > x:
            x -= random.randint(0,1)
          if ux < x:
            x += random.randint(0,1)
        if x < 0: # But not off the left edge.
          x += 1
        if x == self.width: # And not off the right edge.
          x -= 1
        plane = (x,y)
        if self.sky.get(plane,self.SKY_CLEAR) == self.SKY_PLANE:
          del newplanes[plane]
          self.sky[plane] = self.SKY_HIT
          self.draw_led(*plane,self.red)
          continue
        if self.sky.get(plane,self.SKY_CLEAR) == self.SKY_HIT:
          continue
        if plane == self.user:
          self.sky[self.user] = self.SKY_HIT
          self.draw_led(*self.user,self.red)
          userhit = True
          continue
        self.sky[plane] = self.SKY_PLANE
        newplanes[plane] = amo
        self.draw_led(*plane,self.yellow)
      self.planes = newplanes
    else:
      # Add planes to the sky.
      for plane in self.planes.keys():
        self.sky[plane] = self.SKY_PLANE

    if self.movebullet_tick > 0 and self.ticks % self.movebullet_tick == 0:
      # Bullets move downwards.
      newbullets = {}
      for bullet,distance in self.bullets.items():
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.draw_led(*bullet,self.black)
        if not distance:
          continue
        (x,y) = bullet
        y -= 1
        if y < 0:
          continue
        bullet = (x,y)
        if self.sky.get(bullet,self.SKY_CLEAR) != self.SKY_CLEAR:
          if bullet in self.planes:
            del self.planes[bullet]
          if bullet in self.userbullets:
            del self.userbullets[bullet]
          self.sky[bullet] = self.SKY_HIT
          self.draw_led(*bullet,self.red)
        else:
          self.sky[bullet] = self.SKY_BULLET
          newbullets[bullet] = distance-1
          self.draw_led(*bullet,self.green)
      self.bullets = newbullets
      # Planes with amo can fire new bullet, one per movement.
      for plane in [plane for plane in self.planes.keys() if self.planes[plane] > 0]:
        if plane not in self.planes: # See del planes below!
          continue
        amo = self.planes[plane]
        if amo <= 0: # Out of amo!
          continue
        self.planes[plane] = amo - 1
        (x,y) = plane
        bullet = (x,y-1)
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_CLEAR:
          if bullet == self.user:
            self.sky[bullet] = self.SKY_HIT
            self.draw_led(*bullet,self.red)
            userhit = True
          else:
            self.sky[bullet] = self.SKY_BULLET
            self.bullets[bullet] = self.BULLET_DISTANCE
            self.draw_led(*bullet,self.green)
        else:
          self.sky[bullet] = self.SKY_HIT
          self.draw_led(*bullet,self.red)
          if bullet in self.planes:
            del self.planes[bullet]
          if bullet in self.bullets:
            del self.bullets[bullet]
          if bullet in self.userbullets:
            del self.userbullets[bullet]
    else:
      # Add bullets to the sky.
      for bullet in self.bullets.keys():
        self.sky[bullet] = self.SKY_BULLET

    if self.moveuserbullet_tick > 0 and self.ticks % self.moveuserbullet_tick == 0:
      # User bullets move upwards
      newuserbullets = {}
      for bullet,distance in self.userbullets.items():
        if self.sky.get(bullet,self.SKY_CLEAR) == self.SKY_CLEAR:
          self.draw_led(*bullet,self.black)
        if not distance:
          continue
        (x,y) = bullet
        y += 1
        if y == self.height:
          continue
        bullet = (x,y)
        if self.sky.get(bullet,self.SKY_CLEAR) != self.SKY_CLEAR:
          if bullet in self.planes:
            userhits += 1
            del self.planes[bullet]
          if bullet in self.bullets:
            del self.bullets[bullet]
          if bullet in newuserbullets:
            del newuserbullets[bullet]
          self.sky[bullet] = self.SKY_HIT
          self.draw_led(*bullet,self.red)
        else:
          self.sky[bullet] = self.SKY_USERBULLET
          self.draw_led(*bullet,self.blue)
          newuserbullets[bullet] = distance - 1
      self.userbullets = newuserbullets
    else:
      # Add userbullets to the sky.
      for bullet in self.userbullets.keys():
        self.sky[bullet] = self.SKY_USERBULLET


    return (userhit,userhits)

  def run(self):
    """ Run until game is lost. """
    pause = False
    self.draw_points()
    while True:
      self.sleep = .1
      if self.userInput():
        self.userbullets[self.user] = self.BULLET_DISTANCE
      if self.pause:
        continue
      (userhit,userhits) = self.movement()
      if userhit:
        self.sleep = .3
        self.points -= 1
        self.draw_points()
      if userhits:
        self.points += (.2*userhits)
        self.draw_points()
      self.check_points()
      time.sleep(self.sleep)

p = game.factory(midway)
