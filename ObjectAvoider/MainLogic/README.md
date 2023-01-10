# Project Games
Contains Self created games, with a vision to create a system/a virtual world with its own rules and stories.
This is a place to keep my creative and analytical skills in check. 


#Motion Detection:
Motion detection in images can be identified by finding the differences of two images, for example, consider a base image and find the difference in next new images. 

#Steps involved in detect a motion in streams of Image:
Step:1 - Resize the image and store in a sequence to process faster
Step:2 - Blur the image, we dont need too much details to process
Step:3 - Create a list of 10 frames of images, which will be termed as foreground images, we will calculate a weighted average to give more weight to newer images.
Step:4 - 
Step:5 - Find the difference between foreground and background frame list
Step:6 - This yeilds the motion from the difference images
Step:7 - The area which is identified as movement is defined with bounding boxes
Step:8 - Finally, the boxes will be resized back to the original frame and added on it. 

#Clone it and try it:
- Please download the code and run the python code (open the path in the command prompt!)

python MotionDetectionLogic.py 


=====================================================================================
