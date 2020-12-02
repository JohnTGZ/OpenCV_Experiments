import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('sample_pics/gradient.png', 0)
#(t,t_max) = 1, else 0
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
#(t,t_max) = 0, else 1
ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
#(t,t_max) becomes t
ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
#NOT(t,t_max) = 0
ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
#(t,t_max) becomes 0
ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)

titles = ['original', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in xrange(6):
  plt.subplot(2,3, i+1), plt.imshow(images[i], 'gray', vmin=0, vmax=255)
  plt.title(titles[i])
  plt.xticks([]), plt.yticks([])

plt.show()