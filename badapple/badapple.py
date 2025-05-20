# Initial version Complete!
#  INCREASED TERMINAL INTEGRATED ROLLBACK TO 2000 it was 1000 as default

import cv2
import numpy as np
import os
import time


start_time = time.time()
output_width = 480
output_height = 360 
threshold_level = 50
total_coordinates = []
char_for_black = '#'
ascii_canvas = [[' ' for _ in range(240)] for _ in range(90)]
x_scale_factor = 2
y_scale_factor = 4
def black_pixel_coordinates(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_pixel_coordinates = np.column_stack(np.where(gray < threshold_level))
    scaled_black_pixel_coordinates = []
    for y_orig, x_orig in black_pixel_coordinates: # Iterate through original black pixel coordinates
        # Apply the scaling factors to get the coordinates on the smaller ASCII grid
        scaled_y = int(y_orig / y_scale_factor)
        scaled_x = int(x_orig / x_scale_factor)

        # Ensure scaled coordinates are within the target output dimensions
        # This check is important during pre-processing
        if 0 <= scaled_x < output_width and 0 <= scaled_y < output_height:
            # Store the SCALED coordinate
            scaled_black_pixel_coordinates.append((scaled_y, scaled_x))
    return scaled_black_pixel_coordinates

def ascii(total_coordinates):
    for black_pixel_coordinates in total_coordinates: 
        for c in range(len(ascii_canvas)):
            for r in range(len(ascii_canvas[0])):
                ascii_canvas[c][r] = ' '
        for y, x in black_pixel_coordinates:
            if 0 <= x < output_width and 0 <= y < output_height:
                ascii_canvas[y][x] = char_for_black
        os.system('cls')
        for row in ascii_canvas:
            print("".join(row))
        # time.sleep(0.001)  # Adjust the sleep time as needed for your display speed
    
video_path = 'C:\\Users\\revas\\Source\\Repos\\funlittleprojects\\badapple\\BadAppleOriginal.mp4'
cap = cv2.VideoCapture(video_path)

sample_rate = 1
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
for fno in range(0, total_frames, sample_rate):
	cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
	_, image = cap.read()
	total_coordinates.append(black_pixel_coordinates(image))
time_for_preprocess = "--- %s seconds ---" % (time.time() - start_time)
print("Time for preprocessing " + time_for_preprocess)
ascii(total_coordinates)
time_for_all = "--- %s seconds ---" % (time.time() - start_time)
print("Time for preprocessing " + time_for_preprocess)
print("Time for all " + time_for_all)
# 311 seconds
# 221 seconds at sample rate 2
# 219 seconds is the video duration
# 45 pre process 445 render at sampele rate 1

# Goal is to get the render time as low as possible
# 385 pre processing 572 in total. That is 187 seconds for rendering! 957 in total so way worse 
# but good for showing off the render speed after processing.