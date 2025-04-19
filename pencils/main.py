import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
import cv2



kernel = np.ones((7, 7), np.uint8) 
count_all = 0

for i in range(1, 13):
    image = cv2.imread(f"./images/img ({i}).jpg", cv2.IMREAD_GRAYSCALE)
    binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
    binary = cv2.bitwise_not(binary)
    binary = cv2.dilate(binary, kernel, iterations=3)
    labeled = label(binary)
    regions = regionprops(labeled)
    count = 0
    for region in regions:
        if region.eccentricity > 0.99 and region.perimeter > 5000 and region.perimeter < 6700:
            count +=1
    print(f"На {i} изображении {count} карандашей")
    count_all += count
print(f"Всего карандашей на всех изображениях: {count_all}")

plt.imshow(binary)
plt.show()


