import cv
from random import random
import sys
import math


def GetOutlines(image):
  image_size = cv.GetSize(image)

  # create grayscale version
  grayscale = cv.CreateImage(image_size, 8, 1)
  cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
  cv.EqualizeHist(grayscale, grayscale)

  # create storage
  storage = cv.CreateMemStorage(0)

  # detect objects
  cv.Threshold(grayscale, grayscale, 50, 255, cv.CV_THRESH_BINARY)
  contours = cv.FindContours(grayscale, cv.CreateMemStorage(), cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
  #mame kontury potrebujeme fyziku
  #cv.DrawContours(image, self.contours, cv.RGB(255, 110, 0),cv.RGB(0, 255, 0), 10, 1)
  #if len(contours) > 0:
  #  contours = cv.ApproxPoly (contours, storage, cv.CV_POLY_APPROX_DP, 1.5, 1)
  return contours

def GetObjectOutline(cont,h=0,v=0, objects=[]):
  
  if v==1:
    objects.append(cont)
  
  if cont.v_next():
    v += 1
    GetObjectOutline(cont.v_next(),h,v,objects)
    v -= 1

  if cont.h_next():
    h += 1
    GetObjectOutline(cont.h_next(),h,v,objects)
  
  return objects




src = cv.LoadImageM("../images/test.png")
image_size = cv.GetSize(src)

contours = GetOutlines(src)
objectOutline = GetObjectOutline(contours)
masks = []
for poly in objectOutline:
  temp = cv.CreateMat(image_size[1],image_size[0], cv.CV_8UC1)
  cv.FillPoly(temp, [poly], (255,255,255))
  masks.append(temp)
  
 
objects = []
for mask in masks:
  dst = cv.CreateImage(image_size, 8, 3)
  cv.Copy(src, dst, mask)
  objects.append(dst)

output = cv.CreateImage(image_size, 8, 3)
angle = 0
while 1:
  cv.Set(output, (0,0,0))
  dst = cv.CreateImage(image_size, 8, 3)
  mapMatrix = cv.CreateMat(2,3,cv.CV_32F)
  for object in objects:
    rotMatrix = cv.GetRotationMatrix2D((0,0), angle, 1.0, mapMatrix)
    cv.WarpAffine(object, dst, mapMatrix)
    cv.Or(dst, output, output)
    
    
  angle += 1
  cv.ShowImage('Camera', output)
 
  k = cv.WaitKey(10)

  if k != -1:
    print 'Exiting ...'
    break

