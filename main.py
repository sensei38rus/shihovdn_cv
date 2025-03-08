from operator import truediv

import numpy as np
import matplotlib.pyplot as plt

external = np.array([
 [[0, 0], [0, 1]],
 [[0, 0], [1, 0]],
 [[0, 1], [0, 0]],
 [[1, 0], [0, 0]]
])

internal = np.logical_not(external)

crossed = np.array([
 [[0, 1],[1, 0]],
 [[1, 0], [0, 1]]
])



def match(sub, masks):
 for mask in masks:
   if np.all(sub == mask):
      return True
 return False


def count_object(image):
 E = 0

 for y in range(0, image.shape[0]-1):
   for x in range(1, image.shape[1]-1):
     sub = image[y:y+2, x:x+2]
     if match(sub, external):
       E += 1
     elif match(sub, internal):
       E -= 1
     elif match(sub, crossed):
       E += 2
 return E/4


image = np.load("example2.npy")
image[image != 0] = 1

if image.shape[-1] == 3:
  print(np.sum([count_object(image[:, :, i])
     for i in range(image.shape[-1])]))
else:
  print(np.sum(count_object(image)))

plt.imshow(image)
plt.show()
