#!/usr/bin/python3

import cv2

# Open a camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame in a window
    cv2.imshow("Video Stream", frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the camera capture object and close the window
cap.release()
cv2.destroyAllWindows()