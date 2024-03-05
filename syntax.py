
class syntax():
  def __init__(self):
    self.string="this is a string"
    self.array=["a","b",1,]
    self.dict={"key1":'value1', "key3": 3, 3:"valuex"}

  def types(self):
    """ Type of each variable printed using the three types of string formatting """
    print("self.string is type "+str(type(self.string)))
    print("self.array is type {}".format(str(type(self.array))))
    print(f"self.dict is type {type(self.dict)}")

  def plusStrings(self):
    """ Two ways to use the plus operator on a string """
    self.string = self.string + " and a cup"
    print(f"self.string {self.string}")
    self.string += " and a ball"
    print(f"self.string {self.string}")

  def minus(self):
    """ minus """
    self.array[0] = (1 - 2)
    print(f"self.array {self.array}")

  def whileLoop(self):
    """ while loop """
    x = 0
    while x < 10:
      print(f"while loop {x}")
      x += 1

  def forLoop(self):
    """ for loop """
    for i in [1,2,3,4,5,6]:
      print(f"1 to 6 Loop {i}")
    for i in range(6):
      print(f"0 to 5 loop {i}")
    for i in range(6,-1):
      print(f"6 to 0 loop {i}")
    for i in range(6,0,-2):
      print(f"6 to 1 step -2 loop {i}")

  def dictLoop(self):
    """ different ways to loop thru a dict """
    for key in self.dict.keys():
      print(f"self.dict key {key}={self.dict[key]}")
    for key,val in self.dict.items():
      print(f"self.dict key {key}={val}")

s=syntax()
