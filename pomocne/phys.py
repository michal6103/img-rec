import cv
from random import random

class World:
  def __init__(self):
    self.objekty = []
    print "Vytvaram okno"
    cv.NamedWindow('Okno', cv.CV_WINDOW_AUTOSIZE)
    print "Nahravam obrazok"
    self.img = cv.LoadImageM("test.png")
    #pridame gravitaciu

  def createSphere(self):
    #vytvorime gulu
    return 0

  def render(self):
    cv.ShowImage('Okno', self.img)








print "Vytvaram svet"
world = World()

key = -1
while key == -1:
  world.createSphere()
  world.render()
  key = cv.WaitKey(10)



#hranice obrazku
#vytvorime random gulicky
#vytvorime gravitaciu
#zacneme simulovat
