#import definitions
import cv2
import numpy as np

#Class Definition
# Read the logo to use later
class Object:
    def __init__(self, size=50):
        self.logo_org = cv2.imread('logo.png')
        self.size = size
        self.logo = cv2.resize(self.logo_org, (size, size))
        img2gray = cv2.cvtColor(self.logo, cv2.COLOR_BGR2GRAY)
        _, logo_mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        self.logo_mask = logo_mask
        self.speed = 15
        self.x = 100
        self.y = 0
        self.score = 0
    def insert_object(self, frame):
        roi = frame[self.y:self.y + self.size, self.x:self.x + self.size]
        roi[np.where(self.logo_mask)] = 0
        roi += self.logo
    def update_position(self, tresh):
        height, width = tresh.shape
        self.y += self.speed
        if self.y + self.size > height:
            self.y = 0
            self.x = np.random.randint(0, width - self.size - 1)
            self.score += 1
        # Check for collision
        roi = tresh[self.y:self.y + self.size, self.x:self.x + self.size]
        check = np.any(roi[np.where(self.logo_mask)])
        if check:
            self.score -= 1
            self.y = 0
            self.x = np.random.randint(0, width - self.size - 1)
            # self.speed += 1
        return check




# Capture the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# To capture the background - take a few iterations to stabilize view
print("Click 's' key to start the game")
while True:
    # Get the next frame
    _, bg_frame = cap.read()
    bg_frame = cv2.flip(bg_frame, 1)
    #text = "Click 's' key to start"
    #cv2.putText(bg_frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    # Update the frame in the window
    cv2.imshow("Webcam", bg_frame)
    # Check if q is pressed, terminate if so
    if cv2.waitKey(1) == ord('s'):
        break
# Processing of frames are done in gray
bg_gray = cv2.cvtColor(bg_frame, cv2.COLOR_BGR2GRAY)
# We blur it to minimize reaction to small details
bg_gray = cv2.GaussianBlur(bg_gray, (5, 5), 0)

# Let's create the object that will fall from the sky
obj = Object()
# This is where the game loop starts
print("Click 'q' key to quit the game")
while True:
    # Get the next frame
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # Processing of frames are done in gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # We blur it to minimize reaction to small details
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # Get the difference from last_frame
    delta_frame = cv2.absdiff(bg_gray, gray)
    # Have some threshold on what is enough movement
    thresh = cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1]
    # This dilates with two iterations
    thresh = cv2.dilate(thresh, None, iterations=2)
    # cv2.imshow("track", thresh)
    hit = obj.update_position(thresh)
    obj.insert_object(frame)
    # To make the screen white when you get hit
    if hit:
        frame[:, :, :] = 255
    text = f"Score: {obj.score}"
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    # Update the frame in the window
    cv2.imshow("Webcam", frame)
    # Check if q is pressed, terminate if so
    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy windows
cap.release()
cv2.destroyAllWindows()