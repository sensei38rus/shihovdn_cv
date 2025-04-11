import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.morphology import binary_dilation
from pathlib import Path
 

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) -1 



def count_vlines(region):
    return np.all(region.image, axis = 0).sum()

def count_lgr_vlines(region):
    x = region.image.mean(axis = 0) == 1
    return np.sum(x[:len(x) // 2]) > np.sum(x[len(x) // 2:])

def recognize(region):
    if np.all(region.image):
        return "-"
    else: 
        holes = count_holes(region)
        if holes == 2:
            cy,cx= region.centroid_local
            cx /= region.image.shape[1]
            if cx < 0.44:
                return "B"
            return "8"
        elif holes == 1:
            cy,cx = region.centroid_local
            cx /= region.image.shape[1]
            cy /= region.image.shape[0]
            
            if np.all(region.image[:, 0]): # P D
                first_row = region.image[0, :]
                last_row = region.image[-1, :]
                f_sum = np.sum(first_row)
                l_sum = np.sum(last_row)
                if f_sum / l_sum > 1.5:
                    return "P"
                return "D"

            if abs(cx -cy) < 0.035: # 0 A
                return "0"
            return "A"
        else:
           if count_vlines(region) >= 3:
               return "1"
           else:
               if region.eccentricity < 0.45:
                   return "*"
               inv_image = ~region.image
               inv_image = binary_dilation(inv_image, np.ones((3,3)))
               labeled = label(inv_image, connectivity=1)
               if np.max(labeled) == 2:
                   return "/"
               elif np.max(labeled) == 4:
                   return "X"
               else:
                   return "W"
      
symbols = plt.imread(Path(__file__).parent / "symbols.png")
gray = symbols[:, :, :-1].mean(axis = 2)
binary = gray > 0

labeled = label(binary)
regions = regionprops(labeled)

result = {}
out_path = Path(__file__).parent / "out"
out_path.mkdir(exist_ok=True)

plt.figure()
for i, region in enumerate( regions):
    print(f"{i+1}/{len(regions)}")
    symbol = recognize(region)
    if symbol not in result:
        result[symbol]= 0
    result[symbol] +=1
    plt.cla()
    plt.title(symbol)
    plt.imshow(region.image)
    plt.savefig(out_path / f"{i:03d}.png")
print(result)
