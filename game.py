import sys
import time
usePYGAME = False
# Uncomment usePYGAME=True to use pygame instead of unicornhat.
usePYGAME = True
# Following controls are set programatically depending on usePYGAME being True or False.
useCURSE = False
useTERMIOS = False
useUHAT = False
useCURSE = False
useTERMIOS = False
useUHAT = False
# When not simulating the hat using pygame, import curses or termops to get keyboard events.
if not usePYGAME:
  try:
    import unicornhathd
    useUHAT = True
    try:
      import curses
      useCURSE = True
    except:
      import tty, termios, select    
      useTERMIOS = True
  except:
    usePYGAME=True
if usePYGAME:
  useUHAT=False
  usePYGAME = True 
  import pygame.gfxdraw
  import pygame

class game():
  """ Using unicornhat when it's available to import, or use pygame to emulate unicornhat. This base for a game. There is a points board on the left side that starts midway and turns red when drop below 50% and green when above. The user is a single led that can move using the j and k keys and fire using the f key. """

  @classmethod
  def factory(cls,factory_cls,width:int=16,height:int=16):
    """ Creates and runs a class of game. """
    if useUHAT:
      (width,height) = unicornhathd.get_shape()
    p = factory_cls(width,height)
    if useCURSE:
      stdscr = curses.initscr()
      stdscr.nodelay(True) # True means nonblocking getch().
      curses.noecho() # Dont echo what is typed to screen.
      stdscr.addstr(2, 5, 'Unicorn HAT HD')
      stdscr.addstr(4, 5, 'j = LEFT, k = RIGHT, f=Fire, p=PAUSE, r=RESUME')
      stdscr.addstr(6, 5, 'Press Ctrl+C to exit!')
      p.stdscr = stdscr
    else:
      print("pygame simulator of Unicord HAT HD")
      print('j = LEFT, k = RIGHT, f=Fire, p=PAUSE, r=RESUME')
      print('Press Ctrl+C to exit!')
    try:
      p.run()
    finally:
      p.__reset__()

  def debug(self,title:str):
    if useCURSE:
      self.stdscr.addstr(8, 5, title)
    else:
      print(title)

  def __init__(self, title, width, height):
    self.useCURSE = useCURSE
    self.usePYGAME = usePYGAME
    self.useUHAT = useUHAT
    self.useTERMIOS = useTERMIOS
    if useCURSE:
      self.stdscr = None
    self.pause = False
    self.width = width-1 # Last column is the points
    self.height = height
    self.points = int(self.height/2)
    self.user = (width/2,0) # User starts at the middle on the bottom.
    self.white = (255,255,255)
    self.black = (0,0,0)
    self.red = (255,0,0)
    self.green = (0,255,0)
    self.blue = (0,0,255)
    self.yellow = (255,255,0)
    if self.usePYGAME:
      self.pixel_size = 15
      self.window_width = width * self.pixel_size
      self.window_height = height * self.pixel_size
      pygame.init()
      # pygame.key.set_repeat(1) # held keys repeatedly generate an event every 1ms.
      pygame.display.set_caption(title)
      self.screen = pygame.display.set_mode([self.window_width, self.window_height])
    if self.useUHAT:
      unicornhathd.brightness(0.6)
    if self.useTERMIOS:
        self.oldStdinSettings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

  def __reset__(self):
    if self.useTERMIOS:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldStdinSettings)
    if self.useUHAT:
      unicornhathd.clear()
      unicornhathd.off()
    if self.useCURSE:
      curses.endwin()

  def isStdin(self):
    """ Checks for input being ready to read on stdin. """
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

  def userInput(self) -> bool:
    """ Redraws user getting user input that may change users position. Return True when user hits f. """
    f = False
    self.draw_led(*self.user,self.black)
    if self.usePYGAME:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            sys.exit()
          if event.key == pygame.K_f:
            f = True
          elif event.key == pygame.K_j:
            x = self.user[0]
            x -= 1
            if x < 0:
              x = 0
            self.user=(x,0)
          elif event.key == pygame.K_k:
            x = self.user[0]
            x += 1
            if x > self.width-1:
              x = self.width-1
            self.user=(x,0)
          elif event.key == pygame.K_p:
            self.pause = True
          elif event.key == pygame.K_r:
            self.pause = False
    elif self.useTERMIOS:
      while self.isStdin():
        event = sys.stdin.read(1)
        if event == 'f':
          f = True
        elif event == 'q':
          sys.exit()
        elif event == "j":
          x = self.user[0]
          x -= 1
          if x < 0:
            x = 0
          self.user=(x,0)
        elif event == "k":
          x = self.uskr[0]
          x += 1
          if x > self.width-1:
            x = self.width-1
          self.user=(x,0)
        elif event == 'p':
          self.pause = True
        elif event == 'r':
          self.pause = False
    elif self.useCURSE:
      event = 0
      while event != -1:
        event = self.stdscr.getch()
        if event == ord('f'):
          f = True
        elif event == ord('q'):
          sys.exit()
        elif event == ord("j"):
          x = self.user[0]
          x -= 1
          if x < 0:
            x = 0
          self.user=(x,0)
        elif event == ord("k"):
          x = self.user[0]
          x += 1
          if x > self.width-1:
            x = self.width-1
          self.user=(x,0)
        elif event == ord('p'):
          self.pause = True
        elif event == ord('r'):
          self.pause = False
    else:
      raise Exception("No input")
    self.draw_led(*self.user,self.white)
    if self.pause:
      if usePYGAME:
        pygame.display.update()
      time.sleep(.3)
    return f

  def draw_points(self):
    """ Draws the points as a meter on the side of the screen. """
    color = self.green
    if (self.points < (self.height/2)):
      color = self.red
    for y in range(0,self.height):
      if y < self.points:
        self.draw_led(self.width,y,color)
      else:
        self.draw_led(self.width,y,self.black)

  def check_points(self):
    """ IS the game over? """
    if usePYGAME:
      pygame.display.update()
    if self.useUHAT:
      unicornhathd.show()
    if self.points <= 0:
      self.__reset__()
      print(f"Computer won")
      sys.exit()
    if self.points >= self.height:
      self.__reset__()
      print(f"You won")
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
    if self.useUHAT:
      x = round(x)
      if x >= self.width:
        x= self.width-1
      y = round(y)
      if y >= self.height:
        y=self.height-1
      unicornhathd.set_pixel(x,y,*color)

