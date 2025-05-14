import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
# цвета кота
colors = {
    "yellow": (14, 201, 255),
    "green": (76, 177, 34),
    "red": (36, 28, 237),
    "pink": (201, 174, 255),
    "black": (0, 0, 0)
}

#отклонение
tolerance = 30

def is_color_in_frame(frame, target_color, tolerance):
    lower_bound = np.array([max(0, c - tolerance) for c in target_color])
    upper_bound = np.array([min(255, c + tolerance) for c in target_color])
    mask = cv2.inRange(frame, lower_bound, upper_bound)
    return cv2.countNonZero(mask) > 0

def count_frames_with_all_colors(video_path):
    cap = cv2.VideoCapture(video_path)    
    count = 0
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        all_colors_present = True
        for _, color_bgr in colors.items():
            if not is_color_in_frame(frame, color_bgr, tolerance):
                all_colors_present = False
                break
        
        if all_colors_present:
             gray = frame[:, :, :-1].mean(axis = 2)
             binary = gray > 0
             labeled = label(binary)
             regions = regionprops(labeled)
             if len(regions) == 1:
                print(f"найден кот: {frame_number}")
                count += 1
        frame_number+= 1
    cap.release()
    return count


video_path = "output.avi"  
result = count_frames_with_all_colors(video_path)
print(f"Количество кадров, где есть все указанные цвета: {result}")