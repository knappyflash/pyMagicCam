import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyvirtualcam
from pyvirtualcam import PixelFormat

# Load an image
mybgimage = cv2.imread('bg_images\\bg6.jpeg')
mybgimage = cv2.resize(mybgimage,(640,480))

# Load MediaPipe model
base_options = python.BaseOptions(model_asset_path='selfie_segmenter/selfie_segmenter.tflite')
options = vision.ImageSegmenterOptions(base_options=base_options)
segmenter = vision.ImageSegmenter.create_from_options(options)

# Open webcam
cap = cv2.VideoCapture(0)

# Background color
bg_color = (255, 255, 255)

# Open virtual camera
with pyvirtualcam.Camera(width=640, height=480, fps=30, fmt=PixelFormat.BGR) as cam:
    print(f'Virtual camera device: {cam.device}')
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and convert

        # Crop center region

        # Crop center region for zoom
        h, w = frame.shape[:2]
        crop_width = 320  # smaller width for zoom
        crop_height = 240  # smaller height for zoom
        x_start = ((w - crop_width) // 2) + 20
        y_start = ((h - crop_height) // 2) + 50
        frame = frame[y_start:y_start + crop_height, x_start:x_start + crop_width]
        # Resize back to virtual cam size
        frame = cv2.resize(frame, (640, 480))

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Segment
        segmentation_result = segmenter.segment(mp_image)

        mask = segmentation_result.confidence_masks[0].numpy_view()
        mask = np.squeeze(mask)
        mask = cv2.GaussianBlur(mask, (15, 15), 0)  # Smooth edges
        condition = (mask > 0.8).astype(np.uint8)
        condition = cv2.morphologyEx(condition, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        # Apply background
        # bg_image = np.full(frame.shape, bg_color, dtype=np.uint8)
        bg_image = mybgimage
        output_frame = np.where(condition[..., None].astype(bool), frame, mybgimage)

        # Send to virtual camera
        cam.send(output_frame)
        cam.sleep_until_next_frame()

        # Optional preview
        cv2.imshow('Virtual Cam Preview', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
