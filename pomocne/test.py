# export LD_PRELOAD=/usr/lib/libv4l/v4l1compat.so

import sys
import cv
from opencv import highgui 

 
def detect(image):
    image_size = cv.GetSize(image)
 
    # create grayscale version
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    #cv.EqualizeHist(grayscale, grayscale)
 
    # create storage
    storage = cv.CreateMemStorage(0)
#    cv.ClearMemStorage(storage)
 
    # equalize histogram
    cv.EqualizeHist(grayscale, grayscale)
 
    # detect objects
    cv.Threshold(grayscale, grayscale, 128, 255, cv.CV_THRESH_BINARY)
    cont = cv.FindContours(grayscale, cv.CreateMemStorage(), cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
    
    #mame kontury potrebujeme fyziku
    #print "Dlzka: %i" % len(cont)
    if len(cont) > 0:
      cont = cv.ApproxPoly (cont, storage, cv.CV_POLY_APPROX_DP, 3, 1)
    #print "OK"
    cv.DrawContours(image, cont, cv.RGB(255, 110, 0),cv.RGB(0, 255, 0), 30, 3)
    cv.ShowImage('Grayscale', grayscale)
    depth = 10
    i = 0
    while cont and i < depth:
      #print "--------------------------------------------"
      old = None
      for (x,y) in cont:
        #print (x,y)
        cv.Circle(image,(x,y), 3, cv.RGB(17, 110, 255))
        try:
          cv.Line(image, (x,y), old, cv.RGB(255, 110, 0))
        except:
          old = (x,y)
        finally:
          old = (x,y)
      try:
        cont = cont.h_next()
      except:
        cont = None
      i = i + 1
    
    return 0
 
if __name__ == "__main__":
    print "Press ESC to exit ..."
 
    # create windows
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow('Grayscale', cv.CV_WINDOW_AUTOSIZE)
 
    # create capture device
    device = -1 # assume we want first device
    capture = cv.CaptureFromFile("test.ogv")
    capture = cv.CaptureFromCAM(-1)
#    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
#    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
 
    # check if capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
 
    while 1:
        # do forever
 
        # capture the current frame
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
 
        # mirror
        #cv.Flip(frame, None, 1)
 
        # face detection
        detect(frame)
 
        # display webcam image
        cv.ShowImage('Camera', frame)
 
        # handle events
        k = cv.WaitKey(30)
 
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break
