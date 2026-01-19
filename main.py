import cv2
import pyvirtualcam
from pyvirtualcam import  PixelFormat

# Load an image
image = cv2.imread('\\images\\TestPic.png')
image = cv2.resize(image,(640,480))

# Open virtrual camera

with pyvirtualcam.Camera(width=640, height=480, fps=30, fmt=PixelFormat.BGR) as cam:
    print(f'Virtual camera device: {cam.device3}')
    while True:
        cam.send(image)
        cam.sleep_until_next_frame()