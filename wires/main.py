import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_opening, binary_dilation, binary_erosion)



def find_gap(wire):
    labeled = label(wire)
    countObj = np.max(labeled)

    eroded = binary_erosion(wire, np.ones(3).reshape(3,1))
    
    count_gaps_by_wire =[]
    for i in range(eroded.shape[0] - 1):
        count = 0
        if eroded[i,0] ==  1:
            for j in range(eroded.shape[1] - 1):
                if eroded[i,j] == 0:
                    count+=1
            count_gaps_by_wire.append(count)
            
    if countObj != len(count_gaps_by_wire):
        count_gaps_by_wire.append(-1)

    return count_gaps_by_wire


data = np.load("./provoda/wires6npy.txt")
result = find_gap(data)

print( f"Кол-во проводов: {len(result)}")
k = 1
for i in result:
    if i == -1:
        print(k, "провод уничтожен")
        k+=1
    else:   
        print(i, "разрывов в ", k, "проводе")
        k+=1


plt.imshow(data)
plt.show()
