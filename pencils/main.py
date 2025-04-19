import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import sobel, threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing, binary_dilation
from collections import defaultdict


def analyze_pencils(images):
    total_count = 0
    
    for idx, img_path in enumerate(images, 1):
        image = plt.imread(img_path).mean(axis = 2)
        s = sobel(image)

        thresh = threshold_otsu(s)/2
        s[s < thresh] = 0
        s[s >= thresh] = 1
        
      
        
        for _ in range(5):
            s = binary_dilation(s)
        
       
        labeled_components = label(s)
        regions = regionprops(labeled_components)
        
       
        current_count = sum(
            1 for obj in regions
            if 0.997 < obj.eccentricity < 0.9985 
            and obj.convex_area > 20000
        )
        
       
        total_count += current_count
        
        print(f"На изображении {idx} обнаружено карандашей: {current_count}")
    
    return  total_count


image_collection = [f'./images/img ({i}).jpg' for i in range(1, 13)]
    
total = analyze_pencils(image_collection)

    
print(f"\nСумма карандашей: {total}")

