# Initial version Complete!
#  INCREASED TERMINAL INTEGRATED ROLLBACK TO 2000 it was 1000 as default

import cv2
import numpy as np
import os
import time

start_time = time.time()

def ascii(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_level = 50
    black_pixel_coordinates = np.column_stack(np.where(gray < threshold_level))
    output_width = 480
    output_height = 360 
    ascii_canvas = [[' ' for _ in range(output_width)] for _ in range(output_height)]
    char_for_black = '#'
    for y, x in black_pixel_coordinates:
        if 0 <= x < output_width and 0 <= y < output_height:
            ascii_canvas[int(y/4)][int(x/2)] = char_for_black
    os.system('cls')
    for row in ascii_canvas:
        print("".join(row))
    
video_path = 'C:\\Users\\revas\\Source\\Repos\\funlittleprojects\\badapple\\BadAppleOriginal.mp4'
cap = cv2.VideoCapture(video_path)

sample_rate = 2
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
for fno in range(0, total_frames, sample_rate):
	cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
	_, image = cap.read()
	ascii(image)
print("--- %s seconds ---" % (time.time() - start_time))
# 311 seconds
