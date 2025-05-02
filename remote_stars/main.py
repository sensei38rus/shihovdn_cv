import matplotlib.pyplot as plt
import cv2
import numpy as np
import socket
from skimage.measure import label, regionprops
host = "84.237.21.36"
port = 5152



def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)



    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"beat"
    plt.ion()
    plt.figure()
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock,40002)
        im1 = np.frombuffer(bts[2:40002], dtype = "uint8").reshape(bts[0], bts[1])
       
        binary = im1 > 0
        labeled = label(binary)
        regions = regionprops(labeled)

        if len(regions) == 2:
            y1, x1 = regions[0].centroid
            y2, x2 = regions[1].centroid
            result = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            print(f"{result:.1f}")
            sock.send(f"{result:.1f}".encode())
            print(sock.recv(10))
            sock.send(b"beat")
            beat = sock.recv(10)
            plt.clf()
            plt.subplot(121)
            plt.imshow(im1)
            plt.pause(1)
        
       
     





