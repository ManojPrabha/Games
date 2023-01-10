#import definitions
import cv2
import numpy as np
import imutils
import time
from collections import deque


# Input to Step 5: Helper function
# Calculate the foreground frame based on frames
def get_movement(frames, shape):
    movement_frame = np.zeros(shape, dtype='float32')
    i = 0
    for f in frames:
        i += 1
        movement_frame += f * i
    movement_frame = movement_frame / ((1 + i) / 2 * i)
    movement_frame[movement_frame > 254] = 255
    return movement_frame

# Input to Step 5: Helper function
# Calculate the background frame based on frames
# This function has obvious improvement potential
# - Could avoid to recalculate full list every time
def get_background(frames, shape):
    bg = np.zeros(shape, dtype='float32')
    for frame in frames:
        bg += frame
    bg /= len(frames)
    bg[bg > 254] = 255
    return bg

# Detect and return boxes of moving parts
def detect(frame, bg_frames, fg_frames, threshold=20, min_box=200):
    # Step 3-4: Add the frame to the our list of foreground and background frames
    fg_frames.append(frame)
    bg_frames.append(frame)
    # Input to Step 5: Calculate the foreground and background frame based on the lists
    fg_frame = get_movement(list(fg_frames), frame.shape)
    bg_frame = get_background(list(bg_frames), frame.shape)
    # Step 5: Calculate the difference to detect movement
    movement = cv2.absdiff(fg_frame, bg_frame)
    movement[movement < threshold] = 0
    movement[movement > 0] = 254
    movement = movement.astype('uint8')
    movement = cv2.cvtColor(movement, cv2.COLOR_BGR2GRAY)
    movement[movement > 0] = 254
    # As we don't return the movement frame, we show it here for debug purposes
    # Should be removed before release
    cv2.imshow('Movement', movement)
    # Step 6: Find the list of contours
    contours = cv2.findContours(movement, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # Step 7: Convert them to boxes
    boxes = []
    for contour in contours:
        # Ignore small boxes
        if cv2.contourArea(contour) < min_box:
            continue
        # Convert the contour to a box and append it to the list
        box = cv2.boundingRect(contour)
        boxes.append(box)
    return boxes