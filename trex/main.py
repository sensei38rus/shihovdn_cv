import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui as pg
import keyboard
from time import sleep, time


mon1 = {'top': 210, 'left': 565, 'width': 765, 'height': 200}
sct1 = mss()
x2 = 215   
 
start_time = time()
x2_increment_interval = 10               
x2_increment_value = 5                                   
 
while True:
    
    current_time = time() 
    elapsed_time = current_time - start_time
     
    if elapsed_time >= x2_increment_interval:
        x2 += x2_increment_value
        start_time = current_time 
      
   
    sct_img = sct1.grab(mon1)
    img_pil = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    img_arry1 = np.array(img_pil)

    cactus = img_arry1[145:180, 110:int(x2)]
   
   
    if cactus.mean() < 246.2: 
      pg.press('space')


    
    if keyboard.is_pressed('q'):
        break


