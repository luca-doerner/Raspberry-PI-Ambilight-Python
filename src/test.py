import numpy as np
import cv2

X = 70
Y = 40

img = cv2.imread("resized_image.jpg")

for i in range(X):
    print("\n")
    for j in range(Y):
        print(img[i,j], end=" ")
