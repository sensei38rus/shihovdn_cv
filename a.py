import cv2
import numpy as np


cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
capture = cv2.VideoCapture(0)


capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, -4)

def censore(image, size=(5,5)):
    result = np.zeros_like(image)
    stepy = result.shape[0] // size[0]
    stepx = result.shape[1] // size[1]
    for y in range(0, image.shape[0], stepy):
        for x in range(0, image.shape[1], stepx):
            for c in range(0, image.shape[2]):
                result[y:y+stepy, x:x+stepx, c] = np.mean(image[y:y+stepy, x:x+stepx, c])
    return result


face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")


glasses = cv2.imread("deal-with-it.png")

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break
        
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    
   
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=9)
    
  
    if len(eyes) >= 2:
       
        eyes = sorted(eyes, key=lambda x: x[0])

        eye1 = eyes[0]
        eye2 = eyes[1]
       
        x = min(eye1[0], eye2[0])
        y = min(eye1[1], eye2[1])
        w = max(eye1[0] + eye1[2], eye2[0] + eye2[2]) - x
        h = max(eye1[1] + eye1[3], eye2[1] + eye2[3]) - y
        
      
        y -= h // 3
        h += h // 2
        w += w // 2
        x -= w // 4
      
        x, y = max(0, x), max(0, y)
        w = min(w, frame.shape[1] - x)
        h = min(h, frame.shape[0] - y)
        
        if w > 0 and h > 0:
            resized_glasses = cv2.resize(glasses, (w, h))
            frame[y:y+h, x:x+w] = resized_glasses
    
   
    cv2.imshow("Camera", frame)

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break

capture.release()
cv2.destroyAllWindows()