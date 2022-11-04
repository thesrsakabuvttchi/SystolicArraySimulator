import cv2
import numpy as np
from numpy.lib.type_check import imag
import conv

image = cv2.imread('img_1.jpg',cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image,(8,8))
filter = np.array([[-1,0],[0,-1]])

image_out = conv.convolution_as_maultiplication(image,filter)
cv2.imwrite('img_filtered.jpg')