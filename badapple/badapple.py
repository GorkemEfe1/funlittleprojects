# This one will be complicated.
# First I suppose we need to process an image... a video...
#   I'll use opencv to process each image.
#       Won't it take a long time? I have a rtx 4060 but with enough bad practices it will so before running it for the whole 3 minute video I'll check how much it take to run one image
# Finally with the info we recieve from the image we will run a loop through all the frames using ASCII art to remake the scene.

# Starting options... How did I start tictactoe again? the simple logic there was I had an array and I put things in it to eventually match three numbers together so this is on a completely new level.
# Chose a programming language: Python
# Learn fundementals of image processing?
# Break down the project (currently at 2 levels)
# Learn to build spesific components 
#   If I can't break down a project how am I supposed to build its spesific components?
# Build the simple parts first

# Starting I will open the opencv documentation. TLDR CV stands for computer vision
# I saw an image processing module within openCV its looking good
# There is a video capturing module as well
# Video analysis module too.
# I guess the first step is to download opencv
# While downloading matplotlib I agreed to creating a virtual enviorment... Two things that were completely optional...

# First step before even downloading open cv should have been to download the video
# Video and open cv downloaded! Have to listen to it again! its a mp4 file with 360p resolution but probably good enough for video processing although I don't yet know how it works
# I am already sweating from the hard work!

# Now the second step... I can either start with image processing first or go straight into video...I probably won't be needing image processing right?
# I just saw the tutorial for this and it seems quite lengthy maybe I should make a folder for all the tutorials I do inside of the project folder like badapple/tutorials kind of deal
# I realized that I installed opencv in the general environment. Well no need to worry I'm sure it won't cause any problems in the future!
# uhh so the first tutorial wants me to grab a camera huh... My pc doesn't have a camera so I'll plug in my phone I suppose 

# Good news! I now know how to play a video from a file! It has no sound and I don't know how it will be useful but its a start!

# Time to get technical, I said I needed to get information from the video and display it ASCII but what kind of information do I need?

# image decoding by frame?

# What if I get each coordinate data of black pixels 
# Maybe a 2 dimensional array that corresponds to the size of the image.
# Displaying them is troublesome as well but what I essentially want is their locations on the image.

# I learned how to get the coordinates of black pixels (even turned them to blue) w/https://stackoverflow.com/questions/58398300/find-all-coordinates-of-black-grey-pixels-in-image-using-python
# So the plan is I will get all these coordinates then I will print out the ASCII characters accordingly 
# after all the coordinates have been saved. its going to be an array of arrays!

# Seems like the image is 1435 x 1078 but the video is different.

# I'll use the append function to add the data of a single image in to the video data.
# Iterating through it will make it seem like its a video, I think
# Size of the image: 1435 x 1078
# 483 x 362
# 285 x 214
# 118 x 64
# Create a 2D list filled with spaces


# Initial version Complete!
import cv2
import numpy as np

def move_cursor_to_top():
    # ANSI escape code for cursor home position
    print("\033[H", end="")

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
            ascii_canvas[int(y/5)][int(x/5)] = char_for_black
    move_cursor_to_top()
    for row in ascii_canvas:
        print("".join(row))
    

video_path = 'C:\\Users\\revas\\Source\\Repos\\funlittleprojects\\badapple\\BadAppleOriginal.mp4'
cap = cv2.VideoCapture(video_path)
success, img = cap.read()
fno = 0
sample_rate = 3 # every nth frame
while success:
	if fno % sample_rate == 0:
		ascii(img)
	# read next frame
	success, img = cap.read()



# INCREASING TERMINAL INTEGRATED ROLLBACK TO 2000 it was 1000 as default