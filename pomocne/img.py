import cv



def printCont(img,cont,h=0,v=0,col = (0,0,0)):

  if v==1:
    print str((h,v)) + "*"
    col = (255,0,0)
  else:
    print (h,v)
    col = (0,0,0)
  for (x,y) in cont:
    #cv.PutText(img, "%s,%s" % (h,v), (x,y), font, col)
    cv.Circle(img,(x,y), 2, col,2)

  if cont.v_next():
    v += 1
    printCont(img,cont.v_next(),h,v)
    v -= 1

  if cont.h_next():
    h += 1
    printCont(img,cont.h_next(),h,v)



"""def printCont(img,cont):
  i = 0
  while cont_orig:
    cont = cont_orig
    print len(cont)
    while cont:
      #print "--------------------------------------------"
      old = None
      for (x,y) in cont:
        #print (x,y)
        cv.Circle(im,(x,y), 3, cv.RGB(0, 0, 255))
        try:
          cv.Line(im, (x,y), old, cv.RGB(0, 0, 255))
        except:
          old = (x,y)
        finally:
          old = (x,y)
      print type(cont.v_next())
      print type(cont_orig.h_next())
      print "-"
      try:
        cont = cont.v_next()
      except:
        cont = None
    try:
      cont_orig = cont_orig.h_next()
    except:
    cont_orig = None
  i = i+1
"""

im = cv.LoadImageM("test.png")
cv.SaveImage("foo.png", im)


im = cv.LoadImageM("test.png", 1)
dst = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_16S, 3)
laplace = cv.Laplace(im, dst)
cv.SaveImage("foo-laplace.png", dst)


im = cv.LoadImageM("test.png")
img = cv.LoadImageM("test.png", cv.CV_LOAD_IMAGE_GRAYSCALE)

#cam = cv.CreateCameraCapture(-1)
#img = cv.QueryFrame(cam)

cv.Threshold(img, img, 80, 255, cv.CV_THRESH_BINARY)
#cv.AdaptiveThreshold(img, img, 150, cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C)
cv.SaveImage("foo-threshold.png", img)
storage = cv.CreateMemStorage(0)


cont = cv.FindContours(img, storage, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
#cont = cv.ApproxPoly (cont, storage, cv.CV_POLY_APPROX_DP, 3, 1)


#cv.DrawContours(im, cont, cv.RGB(255, 0, 0),cv.RGB(0, 255, 0), 2, 3)


printCont(im,cont)
cv.SaveImage("foo-cont.png", im)

cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)

k = -1
while k == -1:
  cv.ShowImage('Camera', im)
  k = cv.WaitKey(30)





