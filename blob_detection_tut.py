import cv2 as cv
import numpy as np

src = cv.imread('blob.jpg', cv2.IMREAD_GRAYSCALE)

detector = cv.SimpleBlobDetector()

keypoints = detector.detect(src)

#draw detected blobs as red circles
#cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle 
#corresponds to the size of blob
im_with_keypoints = cv.drawKeypoints(src, keypoints, np.array([]),
                                      (0,0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#show keypoints
cv.imshow("im with keypoints", im_with_keypoints)

cv.waitKey(0)