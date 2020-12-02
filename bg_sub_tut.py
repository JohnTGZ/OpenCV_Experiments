import cv2 
import numpy as np
import argparse


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
  SCALE_FACTOR = 0.3
  FPS = (cap.get(cv2.CAP_PROP_FPS))
  RESIZED_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * SCALE_FACTOR)  
  RESIZED_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * SCALE_FACTOR) 
  
  #video writer
  #if grayscale, then set last parameter to false
  out = cv2.VideoWriter("output/"+args.output, 0x00000021,
                        FPS, (RESIZED_WIDTH, RESIZED_HEIGHT), True)

  #Background Subtraction
  bgs = cv2.createBackgroundSubtractorKNN(history=int(5*FPS), dist2Threshold=300/SCALE_FACTOR , detectShadows = False)

  #Blob detector
  detector_params = cv2.SimpleBlobDetector_Params()
  #Param1: Filter by Color
  detector_params.filterByColor = False
  #Param2: Threshold
  detector_params.minThreshold = 10
  detector_params.maxThreshold = 200
  #Param3: Area 
  detector_params.filterByArea = False
  detector_params.minArea = 10
  detector_params.maxArea = 150
  #Param4: Circularity
  detector_params.filterByCircularity = True
  detector_params.minCircularity = 0.1
  #Param5: Convexity
  detector_params.filterByConvexity = False
  detector_params.minInertiaRatio = 0.01
  #Param6: Inertia 
  detector_params.filterByInertia = False
  detector_params.minInertiaRatio = 0.01 
  #assign parameters
  blob_detector = cv2.SimpleBlobDetector_create(detector_params)

  while (True):
    ret, frame = cap.read()
    if ret == False:
      break
    else:
      #1. Resize video
      frame_resized = cv2.resize(frame, (RESIZED_WIDTH, RESIZED_HEIGHT), 0, 0, cv2.INTER_CUBIC )
      
      ##############
      #Preprocessing 
      ##############
      # White balance on color image
      wb = cv2.xphoto.createGrayworldWB()
      wb.setSaturationThreshold(1.0)
      frame_wb	=	wb.balanceWhite(frame_resized)
      # Convert from color to grayscale
      frame_gray = cv2.cvtColor(frame_wb, cv2.COLOR_BGR2GRAY)

      # Gaussian blur
      frame_gray_blur = cv2.GaussianBlur(frame_gray, (5,5), 0)

      frame_final = frame_gray_blur

      #Preprocessing 
      #lux meter to detect the brightness of the sky
      #contrast adjustment using kotera's method

      #rotation + translation compensation

      #4. Background subtraction via KNN
      fgMask = bgs.apply(frame_final)

      #5. Opening (individual erosion then dilation)
      fgMask_final = 

      #6. Blob detection
      keypoints = blob_detector.detect(fgMask_final)
      frame_resized_w_kp = cv2.drawKeypoints(frame_resized, keypoints, np.array([]),
                                          (0,0, 255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
      fgMask_w_kp = cv2.drawKeypoints(fgMask_final, keypoints, np.array([]),
                                          (0,0, 255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

      #7. Mask keypoints on image and add frame number information
      cv2.rectangle( frame_resized_w_kp, (10,2), (100, 20), (255, 255, 255), -1 )
      cv2.putText( frame_resized_w_kp, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0) )

      cv2.imshow('frame_resized_w_kp', frame_resized_w_kp )
      cv2.imshow('frame_wb', frame_wb)
      # cv2.imshow('frame_final', frame_final)
      cv2.imshow('fgMask_w_kp', fgMask_w_kp)

      cv2.moveWindow('frame_resized_w_kp', 0, 25)
      cv2.moveWindow('frame_wb', 1150, 25)
      cv2.moveWindow('fgMask_w_kp', 2300, 25)

      #Output video
      out.write(frame_resized_w_kp)

      if cv2.waitKey(10) & 0xFF==ord('q'):
        break

  #release all video files
  cap.release()
  out.release()
  cv2.destroyAllWindows()