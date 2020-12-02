import cv2 
import numpy as np
import argparse

s

def openingMorph():

def morphEx():

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", default= "spotit3d/A1.mp4" )
  parser.add_argument("--algo", default="KNN")
  parser.add_argument("--output", default="default_output.mp4")

  args = parser.parse_args()

  #capture video
  cap = cv2.VideoCapture(args.input)
  if (cap.isOpened() == False):
    print("Error opening video")
    exit(0)

  #Resize the video
  SCALE_FACTOR = 0.6
  FPS = cap.get(CV_CAP_PROP_FPS)
  WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
  HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
  
  #video writer
  out = cv2.VideoWriter("output/"+args.output, cv2.VideoWriter_fourcc(*'h264'),
                        FPS, (FRAME_WIDTH, FRAME_HEIGHT*2))

  while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
      #Display the resulting frame
      cv2.imshow('Frame', frame)

      #2. convert to grayscale

      #3. Gaussian blur

      #4. Background subtraction via KNN

      #5. Opening (individual erosion then dilation)

      #6. Blob detection

      #7. Mask keypoints on image 

      #Press Q on keyboard to exit
      if cv2.waitKey(0) & 0xFF==ord('q'):
        break
    else:
      break

  cap.release()

  cv2.destroyAllWindows()