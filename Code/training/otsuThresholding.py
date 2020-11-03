import datetime
import os
import time
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import cv2


print("Hello")

img = cv2.imread('test.png',0)

# global thresholding
ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

# Otsu's thresholding
ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Otsu's thresholding after Gaussian filtering

# plot all the images and their histograms
images = [img, 0, th1,
          img, 0, th2,]

titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding"]


