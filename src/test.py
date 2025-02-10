import numpy as np
import cv2

X = 70
Y = 40

img = cv2.imread("resized_y.jpg")
#img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#img = cv2.flip(img, 1)

print(img[39,1])

for i in range(0,-10):
    print("moin")

for j in range(Y):
    print("\n")
    for i in range(X):
        print(img[j, i], end=" ")
