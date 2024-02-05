#!/usr/bin/python3

import cv2

image_path = 'data/image.jpg'

# Open a camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a single frame
for iter in range(3):
    _, frame = cap.read()

 # Save the frame
cv2.imwrite(image_path, frame)

cap.release()

# Release the camera capture object and close the window
cap.release()
cv2.destroyAllWindows()