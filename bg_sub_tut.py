import cv2 
import numpy as np
import argparse


# def openingMorph():

# def morphEx():

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
  FPS = (cap.get(cv2.CAP_PROP_FPS))
  RESIZED_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * SCALE_FACTOR)  
  RESIZED_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * SCALE_FACTOR) 
  
  #video writer
  #if grayscale, then set last parameter to false
  out = cv2.VideoWriter("output/"+args.output, 0x00000021,
                        FPS, (RESIZED_WIDTH, RESIZED_HEIGHT), True)

  #Background Subtraction
  bgs = cv2.createBackgroundSubtractorKNN(history=int(5*FPS), dist2Threshold=300/SCALE_FACTOR , detectShadows = False)

  while (True):
    ret, frame = cap.read()
    if ret == False:
      break
    else:
      # Resize video
      frame_resized = cv2.resize(frame, (RESIZED_WIDTH, RESIZED_HEIGHT), 0, 0, cv2.INTER_CUBIC )
      
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

      #6. Blob detection
      keypoints = blobdetector.detect(fgMask)
      frame_resized_with_keypoints = cv.drawKeypoints(frame_resized, keypoints, np.array([]),
                                          (0,0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

      #7. Mask keypoints on image and add frame number information
      cv2.rectangle( frame_resized, (10,2), (100, 20), (255, 255, 255), -1 )
      cv2.putText( frame_resized, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0) )

      cv2.imshow('frame_resized_with_keypoints', frame_resized_with_keypoints )
      cv2.imshow('frame_wb', frame_wb)
      # cv2.imshow('frame_final', frame_final)
      cv2.imshow('fgMask', fgMask)

      cv2.moveWindow('frame_resized', 0, 25)
      cv2.moveWindow('frame_wb', 1150, 25)
      cv2.moveWindow('fgMask', 2300, 25)

      #Output video
      out.write(frame_resized_with_keypoints)

      if cv2.waitKey(10) & 0xFF==ord('q'):
        break

  #release all video files
  cap.release()
  out.release()
  cv2.destroyAllWindows()