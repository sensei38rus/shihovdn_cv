import cv2
import numpy as np
import os
import json
import random
import time


cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

def get_color(image):
   
    x, y, w, h = cv2.selectROI("Color selection", image)
    roi = image[y:y+int(h), x:x+int(w)]
    color = (np.median(roi[:, :, 0]),
             np.median(roi[:, :, 1]),
             np.median(roi[:, :, 2]))
    cv2.destroyWindow("Color selection")
    return color

def get_ball(image, color):
   
    lower = (max(0, color[0] - 5), color[1] * 0.8, color[2] * 0.8)
    upper = (color[0] + 5, 255, 255)
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        return True, (int(x), int(y), int(radius), mask)
    return False, (-1, -1, -1, np.array([]))

cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)


file_name = "settings.json"
base_colors = json.load(open(file_name, "r")) if os.path.exists(file_name) else {}

# Игровые переменные
game_state = "setup"  
target_sequence = []
user_sequence = []

def generate_target_sequence():
    
    if len(base_colors) < 4:
        return []
    
    # Создаем копию ключей и перемешиваем
    colors = list(base_colors.keys())
    random.shuffle(colors)
    
    # Возвращаем первые 4 цвета
    return colors[:4]

def check_sequence(user_seq, target_seq):
   
    return user_seq == target_seq

#Вывод информации на экран
def draw_game_info(frame):
   
    text_color = (255, 255, 255)
    if game_state == "setup":
        cv2.putText(frame, "Press 1-4 to setup colors, 's' to start", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif game_state == "playing":
        cv2.putText(frame, f"Target: {' '.join(target_sequence)}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    elif game_state == "win":
        cv2.putText(frame, "YOU WIN! Press 'r' to restart", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif game_state == "lose":
        cv2.putText(frame, "GAME OVER! Press 'r' to restart", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Target: {' '.join(target_sequence)}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

def detect_square_sequence(subsequence):
    if len(subsequence) < 4:
        return []

   
    sorted_balls = sorted(subsequence.items(), key=lambda x: x[1][1]) 

    #средняя  вертикальная координата
    mid_y = (sorted_balls[0][1][1] + sorted_balls[-1][1][1]) / 2  
    upper = []
    lower = []
    
    for ball in sorted_balls:
        if ball[1][1] < mid_y:  
            upper.append(ball)
        else:  
            lower.append(ball)

    
    if len(upper) < 2 or len(lower) < 2:
        upper = sorted_balls[:2]
        lower = sorted_balls[2:4]

    
    upper_sorted = sorted(upper, key=lambda x: x[1][0])  
    lower_sorted = sorted(lower, key=lambda x: x[1][0])  

  
    return [
        upper_sorted[0][0],  
        upper_sorted[1][0], 
        lower_sorted[0][0], 
        lower_sorted[1][0]   
    ]


while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break
        

    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    key = chr(cv2.waitKey(1) & 0xFF)
  
    if game_state == "setup":
        if key in "1234":
            color = get_color(hsv)
            base_colors[key] = color
            json.dump(base_colors, open(file_name, "w"))
        elif key == "s" and len(base_colors) >= 4:
            target_sequence = generate_target_sequence()
            game_state = "playing"
            user_sequence = []
    elif game_state == "playing":
        ball_positions = {}
        for key, color in base_colors.items():
            found, (x, y, r, mask) = get_ball(hsv, color)
            if found:
                ball_positions[key] = (x, y, r, mask)
                cv2.circle(frame, (x, y), r, (255, 0, 255), 2)
        
        user_sequence = detect_square_sequence(ball_positions)
        if len(user_sequence) == 4 and check_sequence(user_sequence, target_sequence):
            game_state = "win"
    elif game_state in ["win", "lose"] and key == "r":
        game_state = "setup"
        target_sequence = []
        user_sequence = []
    
    if key == "q":
        break
    
    draw_game_info(frame)
    cv2.imshow("Camera", frame)


capture.release()
cv2.destroyAllWindows()
