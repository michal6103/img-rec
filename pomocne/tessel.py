#!/usr/bin/python

import sys
from time import clock

import p2t
import cv


def tesselCont(img,cont,h=0,v=0,col = (0,0,0)):

  if v==0:
    print str((h,v)) + "*"
    col = (255,0,0)
  else:
    print (h,v)
    col = (255,0,255)
    polyline = []
    for (x,y) in cont:
      cv.Circle(img, (x,y) , 2, col,2)
      polyline.append(p2t.Point(x,y))
    cdt = p2t.CDT(polyline)
    triangles = cdt.triangulate()
    
    for t in triangles:
      x1 = int(t.a.x)
      y1 = int(t.a.y)
      x2 = int(t.b.x)
      y2 = int(t.b.y)
      x3 = int(t.c.x)
      y3 = int(t.c.y)
      cv.PolyLine(img, [((x1, y1), (x2, y2), (x3, y3))], 1, col, 1)

  if cont.v_next():
    v += 1
    tesselCont(img,cont.v_next(),h,v)
    v -= 1

  if cont.h_next():
    h += 1
    tesselCont(img,cont.h_next(),h,v)


def main():
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
    image = cv.LoadImageM("test.png")
    image_size = cv.GetSize(image)
    im = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, im, cv.CV_BGR2GRAY)
    storage = cv.CreateMemStorage(0)
    cont = cv.FindContours(im, storage, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
    if len(cont) > 0:
      cont = cv.ApproxPoly (cont, storage, cv.CV_POLY_APPROX_DP, 1, 1)
      print "Aproximacia OK"
    else:
      print "Prilis malo kontur"
    
    tesselCont(im,cont,h=0,v=0,col = (0,0,0))

    k=-1
    while k==-1:
      cv.ShowImage('Camera', im)
      k = cv.WaitKey(30)

if __name__=="__main__":
      main()

