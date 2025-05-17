import numpy as np
import pyautogui as pg
import mss
import keyboard

i = 1
w = 90
top = 340      
left = 670                  
h = 60

mon1 = {'top': top, 'left': left, 'width': w, 'height':h}
restart_coords = (478, 478)

sct = mss.mss()
pg.click(restart_coords)

while True:
    img = np.array(sct.grab(mon1))

    if img.mean() < 247.5:
        pg.press('space')
    if w < 600:
        i+=1
        if i == 100:
            w+=4              
            mon1 = {'top': top, 'left': left, 'width': w, 'height':h}
            i = 1
           
   
    if keyboard.is_pressed('q'):
        break



