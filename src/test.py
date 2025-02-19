import numpy as np
import time
#import cv2

X = 70
Y = 40

#img = cv2.imread("resized_image.jpg")
#img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#img = cv2.flip(img, 1)

def get_smooth_color(c1, c2, ratio=0.3):
    return c1*ratio + c2*(1-ratio)

arr1 = np.array([[[0,0,0], [1,1,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]]])
arr2 = np.array([[[0,0,0], [1,2,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]]])

print(get_smooth_color(arr1, arr2))

while(True):
    print("Moin")
    time.sleep(10)

#for j in range(Y):
 #   print("\n")
  #  for i in range(X):
   #     print(img[j, i], end=" ")
