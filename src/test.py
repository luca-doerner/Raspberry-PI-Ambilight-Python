import numpy as np
import cv2

X = 70
Y = 40

img = cv2.imread("resized_image.jpg")
#img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#img = cv2.flip(img, 1)

for j in range(Y):
    print("\n")
    for i in range(X):
        print(img[j, i], end=" ")
