import numpy as np
import time
#import cv2

X = 70
Y = 40
new_pixels = [[0,0,0]] * 2

arr1 = np.array(
[[[ 84, 101,  98],
  [ 56,  81,  81],
  [ 79, 109, 113],
  [ 50,  54,  55],
  [ 63,  79,  78],
  [ 65,  68,  68],
  [ 95, 128, 145],
  [ 96, 123, 130],
  [ 45,  77,  97]],

 [[ 55,  77,  73],
  [ 31,  52,  49],
  [119, 150, 159],
  [ 43,  50,  49],
  [121, 144, 150],
  [ 91,  98,  97],
  [ 89, 123, 138],
  [ 59,  66,  65],
  [123, 156, 180]]])

for i in range(2):
    color = arr1[(2-1) - i, 1]
    new_pixels[i] = color.tolist()

print(new_pixels)

new_pixels[:] = arr1[:, 1][::-1].tolist()

print(new_pixels)

new_pixels = np.array(new_pixels)

new_pixels[:, [0, 2]] = new_pixels[:, [2, 0]]

print(new_pixels)

#img = cv2.imread("resized_image.jpg")
#img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#img = cv2.flip(img, 1)

#def get_smooth_color(c1, c2, ratio=0.3):
#    return c1*ratio + c2*(1-ratio)

#arr1 = np.array([[[0,0,0], [1,7,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]], [[0,0,0], [1,255,255], [255,255,255]]])
#arr2 = np.array([[[0,0,0], [1,2,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]], [[0,0,0], [1,1,1], [2,2,2]]])
#arr3 = np.array([1, 2, 3, 4, 5, 6, 7, 8])

#arr1_mean = np.mean(arr1, axis=2, keepdims=True)

#print(np.ones((10,1)))

#print(arr1[0,1])
#print(arr1_mean[0,1])
#print((arr1_mean/255))

#print(np.roll(arr3, -3))

#while(True):
#    print("Moin")
#    time.sleep(10)

#for j in range(Y):
 #   print("\n")
  #  for i in range(X):
   #     print(img[j, i], end=" ")
