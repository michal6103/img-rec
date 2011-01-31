#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
#
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlecode.com)
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.




#TODO Interpolacia
"""
http://docs.scipy.org/doc/numpy/reference/generated/numpy.interp.html
alebo
http://docs.scipy.org/doc/scipy/reference/interpolate.html
"""

from test_main import *
import cv
from random import random
import p2t
import sys
import math



class Empty(Framework):
    """You can use this class as an outline for your tests.

    """
    name = "Empty" # Name of the class to display
    _pickle_vars=[] # variables to pickle (save/load). e.g., ['name', 'var1', 'var2']
    def __init__(self):
        """
        Initialize all of your objects here.
        Be sure to call the Framework's initializer first.
        """
        super(Empty, self).__init__()
        #sys.setrecursionlimit(15000)
        self.countrours =(0,0)
        self.objectBodies = {}
        self.step = 0
        # Initialize all of the objects
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)


        bd=box2d.b2BodyDef()
        bd.position = ( 0.0, 0.0 )
        body = self.world.CreateBody(bd)
        edgeDef=box2d.b2EdgeChainDef()
        obvod = [(0,0),(360/30.0,0),(360/30.0,296/30.0),(0,296/30.0)]
        obvod.reverse()
        edgeDef.setVertices(obvod)
        body.CreateShape(edgeDef)
        body.SetMassFromShapes()
        #self.CreateRandomSpheres(100)


        self.InitCamera()
        self.GetFrame()
        self.CreateObjectsFromCountours(self.contours)
        self.setZoom(50)
        #self.debugDraw.scale = 1.3

        self.viewCenter = (250,250)
        #self.debugDraw.view = (-30,350)

    def CreateRandomBoxes(self, count):
        sd=box2d.b2PolygonDef()

        a = 0.1
        sd.SetAsBox(a, a)
        sd.density = 5.0
        sd.restitution = 0.6
        sd.friction = 0.8
        x=box2d.b2Vec2(0, 0)
        for i in range(count):
            y = x.copy()
            bd=box2d.b2BodyDef()
            bd.position = (random()*360/30.0,random()*296/30.0)
            body = self.world.CreateBody(bd)
            body.CreateShape(sd)
            body.SetMassFromShapes()

    def CreateRandomSpheres(self, count):
        sd = box2d.b2CircleDef()
        sd.radius = 0.1
        sd.localPosition.Set(1.0, 0.0)
        #sd=box2d.b2PolygonDef()
        #a = 1.5
        #sd.SetAsBox(a, a)
        sd.density = 1.0
        sd.restitution = 0.1
        sd.friction = 0.1
        x=box2d.b2Vec2(0, 0)
        for i in range(count):
            print "Vytvaram gulu cislo: %i" %i
            y = x.copy()
            bd=box2d.b2BodyDef()
            bd.position = (random()*300/30.0,270/30.0)
            body = self.world.CreateBody(bd)
            body.CreateShape(sd)
            body.SetMassFromShapes()


    def InitCamera(self):
        #self.camera = cv.CaptureFromFile("test.ogv")
        self.camera = cv.CaptureFromCAM(-1)

    def GetFrame(self):
        #src = cv.LoadImageM("images/test.png")
        src = cv.QueryFrame(self.camera)
        cv.Flip(src);
        try:
          self.frameNumber += 1
        except:
          self.frameNumber = 0
        self.contours = self.DetectOutline(src)
        #src_rgb = cv.CreateMat(src.height, src.width, cv.CV_8UC3)
        #cv.CvtColor(src, src_rgb, cv.CV_BGR2RGB)
        #pygame_img = pygame.image.frombuffer(src_rgb.tostring(), cv.GetSize(src_rgb), "RGB")
        #self.screen.blit(pygame_img, (0,0))


    def DetectOutline(self, image):
      image_size = cv.GetSize(image)

      # create grayscale version
      grayscale = cv.CreateImage(image_size, 8, 1)
      cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
      cv.EqualizeHist(grayscale, grayscale)


      # create storage
      storage = cv.CreateMemStorage(0)

      # detect objects
      cv.Threshold(grayscale, grayscale, 50, 255, cv.CV_THRESH_BINARY)
      self.contours = cv.FindContours(grayscale, cv.CreateMemStorage(), cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
      #mame kontury potrebujeme fyziku
      #cv.DrawContours(image, self.contours, cv.RGB(255, 110, 0),cv.RGB(0, 255, 0), 10, 1)
      if len(self.contours) > 0:
        self.contours = cv.ApproxPoly (self.contours, storage, cv.CV_POLY_APPROX_DP, 1, 1)
      return self.contours



    def CreateContour(self, cont, h,v):
      edgeDef=box2d.b2EdgeChainDef()
      #konverzia jednotiek do reozmeru 0.1m - 10m
      contM = []
      for point in cont:
        x = point[0]/30.0
        y = point[1]/30.0
        contM.append((x,y))
      edgeDef.setVertices(contM)

      bd=box2d.b2BodyDef()
      bd.position = ( 0.0, 0.0 )

      if v==0:
        body = self.world.CreateBody(bd)
        try:
          self.contourBodies.append(body)
        except:
          self.contourBodies = [body]
        body.CreateShape(edgeDef)

      """else:
        try:
          body = self.objectBodies[h+self.frameNumber*100000]
          print "Pripajam cast prvku %i" % h
        except:
          print "Vytvaram body opre prvok %i" % h
          body = self.world.CreateBody(bd)
          self.objectBodies[h+self.frameNumber*100000] = body
        for point in contM:
          weight.localPosition = (point)
          body.CreateShape(weight)
      """
      #teselacia
      if v == 1:
        try:
          body = self.objectBodies[h+self.frameNumber*100000]
          print "Pripajam cast prvku %i" % h
        except:
          print "Vytvaram body opre prvok %i" % h
          body = self.world.CreateBody(bd)
          self.objectBodies[h+self.frameNumber*100000] = body
        polyline = []
        for (x,y) in cont:
          try:
            #osetrime prilis kratke vektory, tak aby vsetko malo velkost aspon 0,1
            if math.hypot(x-old_x,y-old_y)<3:
              x = x + math.copysign(3, x-old_x)
              y = y + math.copysign(3, y-old_y)
              print "kratky vektor"
          except:
            pass
          old_x = x
          old_y = y
          polyline.append(p2t.Point(x,y))
          
          
        cdt = p2t.CDT(polyline)
        triangles = cdt.triangulate()

        for t in triangles:
          x1 = t.a.x/30.0
          y1 = t.a.y/30.0
          x2 = t.b.x/30.0
          y2 = t.b.y/30.0
          x3 = t.c.x/30.0
          y3 = t.c.y/30.0
          poly=box2d.b2PolygonDef()
          poly.setVertices(((x1, y1), (x2, y2), (x3, y3)))
          poly.density = 1.0
          poly.restitution = 0.0
          poly.friction = 0.0
          body.CreateShape(poly)
          body.SetMassFromShapes()



    def DestroyContours(self):
      print "Skusam z mazat kontury"
      try:
        for body in self.contourBodies:
          self.world.DestroyBody(body)
        print "OK"
      except:
        print "Exception: Destroy Contours"
      self.contourBodies = None

    def DestroyObjects(self):
      print "Skusam zmazat objekty"
      try:
        print "Kluce %s" % len(self.objectBodies.keys())
        for key in self.objectBodies.keys():
          print "Mazem body opre prvok %i" % key
          self.world.DestroyBody(self.objectBodies[key])
          del(self.objectBodies[key] )
        print "OK"
      except Exception as inst:
        print "Exception: Destroy Objects"
        print inst



    def CreateObjectsFromCountours(self,cont,h=0,v=0):
      print (h,v)
      if v>0:
        density = 10.0
      else:
        density = 0

      if len(cont)>3  and len(cont)<40  or v==0:
        self.CreateContour(cont,h,v)

      if cont.v_next():
        v += 1
        self.CreateObjectsFromCountours(cont.v_next(),h,v)
        v -= 1

      if cont.h_next():
        h += 1
        self.CreateObjectsFromCountours(cont.h_next(),h,v)


    def Keyboard(self, key):
        """
        The key is from pygame.locals.K_*
        (e.g., if key == K_z: ... )

        If you are using the pyglet backend, you should be able to use the same
        K_[a-z], see pyglet_keymapper.py
        """
        if key == K_t:
          self.CreateRandomSpheres(100)

        if key == K_y:
          self.world.gravity = (0,-10)

        if key == K_u:
          self.world.gravity = (0,10)

        if key == K_i:
          self.DestroyContours()
          #self.DestroyObjects()
          self.GetFrame()
          self.CreateObjectsFromCountours(self.contours)

        if key == K_o:
          self.DestroyObjects()

        if key == K_p:
          self.DestroyContours()


        pass

    def Step(self, settings):
        """Called upon every step.
        You should always call
         -> super(Your_Test_Class, self).Step(settings)
        at the beginning or end of your function.

        If placed at the beginning, it will cause the actual physics step to happen first.
        If placed at the end, it will cause the physics step to happen after your code.
        """
        #if self.step % 200 == 0:
        #  self.CreateRandomBoxes(1)
          #self.CreateRandomSpheres(100)

#        if self.step % 200 == 0:
#          self.DestroyContours()
#          self.DestroyObjects()
#          self.GetFrame()
#          self.CreateObjectsFromCountours(self.contours)

        #r = random()*20
        #cont = ((40+r,40+r),(45+r,40+r),(45+r,45+r),(41+r,51+r))
        #self.pulsar.setVertices(cont)
        super(Empty, self).Step(settings)


        # do stuff

        self.step = self.step + 1
        # Placed after the physics step, it will draw on top of physics objects
        #self.DrawStringCR("Test")

    def ShapeDestroyed(self, shape):
        """
        Callback indicating 'shape' has been destroyed.
        """
        pass

    def JointDestroyed(self, joint):
        """
        The joint passed in was removed.
        """
        pass

    #def BoundaryViolated(self, body):
    #    """
    #    The body went out of the world's extents.
    #    """
    #    See pygame_main's implementation of BoundaryViolated for more information
    #    about pickling and general stability.

if __name__=="__main__":
    main(Empty)

