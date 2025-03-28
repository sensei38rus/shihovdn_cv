import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops


stars = np.load("./stars/stars.npy")
labeled = label(stars)
regions = regionprops(labeled)

count = 0
for region in regions:
    if region.solidity < 1:
        count+=1

print(count)
plt.imshow(stars)
plt.show()