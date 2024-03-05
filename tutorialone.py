import unicornhathd

class tutorialOne():
  """ Tutorial #1 with four challenges """
  def __init__(self):
    (self.width,self.height) = unicornhathd.get_shape()
    self.white = (255,255,255)
    self.black = (0,0,0)
    self.red = (255,0,0)
    self.green = (0,255,0)
    self.blue = (0,0,255)
    self.yellow = (255,255,0)

  def one(self,colour):
    """ Challenge 1 """
    unicornhathd.set_pixel(0,0,*colour)
    unicornhathd.set_pixel(1,1,*colour)
    unicornhathd.set_pixel(2,2,*colour)
    unicornhathd.set_pixel(3,3,*colour)
    unicornhathd.set_pixel(4,4,*colour)
    unicornhathd.set_pixel(5,5,*colour)
    unicornhathd.set_pixel(6,6,*colour)
    unicornhathd.set_pixel(7,7,*colour)
    unicornhathd.show()

  def two(self,colour):
    """ Challenge 2 """
    for i in range(0,8):
      unicornhathd.set_pixel(0+i,0+i,*colour)
    unicornhathd.show()
    
  def three(self,colour):
    """ Challenge 3 """
    unicornhathd.set_pixel(0,7,*colour)
    unicornhathd.set_pixel(1,6,*colour)
    unicornhathd.set_pixel(2,5,*colour)
    unicornhathd.set_pixel(3,4,*colour)
    unicornhathd.set_pixel(4,3,*colour)
    unicornhathd.set_pixel(5,2,*colour)
    unicornhathd.set_pixel(6,1,*colour)
    unicornhathd.set_pixel(7,0,*colour)
    unicornhathd.show()

  def four(self,colour):
    """ Challenge 4 """
    for x in range(0,8):
      unicornhathd.set_pixel(0+x,7-x,*colour)
    unicornhathd.show()

  def fourY(self,colour):
    """ Why code four differently, is it easier to read? """
    for x,y in [(1,7-i) for i in range(8)]:
      unicornhathd.set_pixel(x,y,*colour)
    unicornhathd.show()

  def all(self):
    self.one(self.yellow)
    junk=input("Hit enter to run two");
    self.two(self.blue)
    junk=input("Hit enter to run three");
    self.three(self.red)
    junk=input("Hit enter to run four");
    self.four(self.white)
    junk=input("Hit enter to run fourY");
    self.four(self.green)

t=tutorialOne()
t.all()
