import cv2
import numpy as np
import imutils
import time
from collections import deque
from detectionTools import get_movement
from detectionTools import get_background
from detectionTools import detect

def main(width=640, height=480, scale_factor=2):
    # Create the buffer of our lists
    bg_frames = deque(maxlen=30)
    fg_frames = deque(maxlen=10)
    # Get the webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # We want to see how many frames per second we process
    last_time = time.time()
    while True:
        # Step 0: Read the webcam frame (ignore return code)
        _, frame = cap.read()
        # Resize the frame
        frame = cv2.resize(frame, (width, height))
        # Step 1: Scale down to improve speed (only takes integer scale factors)
        work_frame = cv2.resize(frame, (width // scale_factor, height // scale_factor))
        # Step 2: Blur it and convert the frame to float32
        work_frame = cv2.GaussianBlur(work_frame, (5, 5), 0)
        work_frame_f32 = work_frame.astype('float32')
        # Step 3-7 (steps in function): Detect all the boxes around the moving parts
        boxes = detect(work_frame_f32, bg_frames, fg_frames)
        # Step 8: Draw all boxes (remember to scale back up)
        for x, y, w, h in boxes:
            cv2.rectangle(frame, (x * scale_factor, y * scale_factor), ((x + w) * scale_factor, (y + h) * scale_factor),
                          (0, 255, 0), 2)
        # Add the Frames Per Second (FPS) and show frame
        text = "FPS:" + str(int(1 / (time.time() - last_time)))
        last_time = time.time()
        cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()