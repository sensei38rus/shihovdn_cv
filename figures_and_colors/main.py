import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
from collections import defaultdict



def divide_shades(color_counts):
    sorted_items = sorted(color_counts.items())
    pairs = [[hue, count] for hue, count in sorted_items]
    hues = [h for h, c in sorted_items]
    diffs = [hues[i+1] - hues[i] for i in range(len(hues)-1)]
    avg_diff = np.mean(diffs)
    
    split_points = []
    for i, diff in enumerate(diffs):
        if diff > avg_diff * 2:
            split_points.append(i+1)
    
  
    shade_groups = []
    start = 0
    for point in split_points:
        shade_groups.append(pairs[start:point])
        start = point
    shade_groups.append(pairs[start:])
    
 
    shades = defaultdict(int)
    for group in shade_groups:
        avg_hue = round(sum(h for h, c in group)/len(group), 2)
        total = sum(c for h, c in group)
        shades[avg_hue] = total
    
    return shades

def analyze_image(image_path):

    image = plt.imread(image_path)
    gray = image.mean(axis=2)
    binary = gray > 0
    
    
    labeled = label(binary)
    regions = regionprops(labeled)
    
  
    rect_colors = defaultdict(int)
    circle_colors = defaultdict(int)
    
    for region in regions:
       
        y, x = map(int, region.centroid)
        hue = rgb2hsv(image[y, x])[0]
        
       
        if region.area == region.image.shape[0] * region.image.shape[1]:
            rect_colors[hue] += 1
        else:
            circle_colors[hue] += 1
    
  
    rect_shades = divide_shades(rect_colors)
    circle_shades = divide_shades(circle_colors)
    
  
    sorted_rects = sorted(rect_shades.items(), key=lambda x: x[1])
    sorted_circles = sorted(circle_shades.items(), key=lambda x: x[1])
    
  
    total_figures = sum(rect_colors.values()) + sum(circle_colors.values())
    print(f'Всего фигур: {total_figures}')
    
    
    all_shades = set(rect_shades.keys()).union(set(circle_shades.keys()))
    for shade in sorted(all_shades):
        count = rect_shades.get(shade, 0) + circle_shades.get(shade, 0)
        print(f'\tНа изображении {count} фигур оттенка {shade}')
    
    print(f'Прямоугольников: {sum(rect_colors.values())}')
    for shade, count in sorted_rects:
        print(f'\tНа изображении {count} прямоугольников оттенка {shade}')
    
    print(f'Кругов: {sum(circle_colors.values())}')
    for shade, count in sorted_circles:
        print(f'\tНа изображении {count} кругов оттенка {shade}')

analyze_image('balls_and_rects.png')
