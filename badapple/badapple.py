# Initial version Complete!
#  INCREASED TERMINAL INTEGRATED ROLLBACK TO 2000 it was 1000 as default



import cv2
import numpy as np
import os
import time
import sys

# Define ASCII canvas dimensions (derived from your original ascii_canvas and scale factors)
ASCII_CANVAS_WIDTH = 240
ASCII_CANVAS_HEIGHT = 90

# Define the dimensions to which video frames will be resized before processing
PROCESSING_WIDTH = 480  # This was your original output_width
PROCESSING_HEIGHT = 360 # This was your original output_height

# Scale factors (ensure PROCESSING_WIDTH / x_scale_factor = ASCII_CANVAS_WIDTH, etc.)
X_SCALE_FACTOR = PROCESSING_WIDTH // ASCII_CANVAS_WIDTH # Should be 2 based on your values
Y_SCALE_FACTOR = PROCESSING_HEIGHT // ASCII_CANVAS_HEIGHT # Should be 4 based on your values

THRESHOLD_LEVEL = 50
CHAR_FOR_BLACK = '#'

# Initialize ascii_canvas globally (or pass/return it from functions)
ascii_canvas = [[' ' for _ in range(ASCII_CANVAS_WIDTH)] for _ in range(ASCII_CANVAS_HEIGHT)]

def get_black_pixel_coordinates(image_frame):
    """
    Converts an image frame to grayscale, identifies black pixels,
    and scales their coordinates to fit the ASCII canvas.
    The input 'image_frame' is expected to be already resized to PROCESSING_WIDTH x PROCESSING_HEIGHT.
    """
    gray_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
    # Find coordinates of pixels below the threshold
    original_black_pixels_y, original_black_pixels_x = np.where(gray_frame < THRESHOLD_LEVEL)
    
    scaled_black_pixel_coords = set() # Use a set to store unique coordinates on the canvas

    for y_orig, x_orig in zip(original_black_pixels_y, original_black_pixels_x):
        scaled_y = int(y_orig / Y_SCALE_FACTOR)
        scaled_x = int(x_orig / X_SCALE_FACTOR)

        # Ensure scaled coordinates are within the ASCII canvas bounds
        if 0 <= scaled_x < ASCII_CANVAS_WIDTH and 0 <= scaled_y < ASCII_CANVAS_HEIGHT:
            scaled_black_pixel_coords.add((scaled_y, scaled_x))
            
    return list(scaled_black_pixel_coords)

def play_ascii_animation(all_frames_pixel_coords, target_fps):
    """
    Plays the ASCII animation in the terminal with proper frame rate control
    and reduced flickering using ANSI escape codes.
    """
    if not all_frames_pixel_coords:
        print("No frames to display.")
        return

    if target_fps <= 0:
        print("Target FPS must be positive. Defaulting to 25 FPS.")
        target_fps = 30
        
    time_per_frame = 1.0 / target_fps
    get_current_time = time.perf_counter

    next_frame_target_time = get_current_time()

    # Hide cursor before animation starts (optional, but can look cleaner)
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        for frame_coords in all_frames_pixel_coords:
            # 1. Reset ASCII canvas (already in your global ascii_canvas or create locally)
            for r in range(ASCII_CANVAS_HEIGHT): # Use global ASCII_CANVAS_HEIGHT
                for c in range(ASCII_CANVAS_WIDTH): # Use global ASCII_CANVAS_WIDTH
                    ascii_canvas[r][c] = ' '      # Use global ascii_canvas
            
            # 2. Populate ASCII canvas
            for y, x in frame_coords:
                ascii_canvas[y][x] = CHAR_FOR_BLACK # Use global CHAR_FOR_BLACK and ascii_canvas
            
            # 3. Prepare the full frame string
            output_string = "\n".join("".join(row) for row in ascii_canvas) # Use global ascii_canvas
            
            # 4. Wait until it's time to display
            current_time_before_sleep = get_current_time()
            sleep_duration = next_frame_target_time - current_time_before_sleep
            
            if sleep_duration > 0:
                time.sleep(sleep_duration)

            # 5. Display the frame using ANSI escape codes
            # \033[H moves cursor to home (top-left)
            sys.stdout.write(f"\033[H{output_string}") 
            sys.stdout.flush() # Ensure it's written immediately
            
            # 6. Schedule the next frame's display time
            next_frame_target_time += time_per_frame
    except KeyboardInterrupt:
        print("\nAnimation stopped by user.")
    finally:
        # Show cursor again when animation ends or is interrupted
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        print() # Newline after animation

def main():
    start_time = time.time() # Overall script start time

    video_path = 'C:\\Users\\revas\\Source\\Repos\\funlittleprojects\\badapple\\BadAppleOriginal.mp4'
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps == 0: # Handle cases where FPS might not be correctly read
        print("Warning: Video FPS reported as 0. Defaulting to 25 FPS for playback.")
        video_fps = 30.0 # Use a float default

    total_frames_in_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # sample_rate = 1 means process every frame. Adjust if preprocessing is too slow.
    # For Bad Apple, which is high contrast, a higher sample_rate (e.g., 2 or 3) might still look okay
    # and speed up preprocessing significantly if needed. For now, let's keep it at 1.
    sample_rate = 1 
    
    processed_frames_data = [] # Store coordinates for each frame

    print("Starting preprocessing...")
    frames_to_process = range(0, total_frames_in_video, sample_rate)
    for i, frame_number in enumerate(frames_to_process):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {frame_number}. Skipping.")
            continue
        
        # Resize frame to the standard processing dimensions
        resized_frame = cv2.resize(frame, (PROCESSING_WIDTH, PROCESSING_HEIGHT))
        
        # Get scaled black pixel coordinates for the ASCII canvas
        frame_pixel_coords = get_black_pixel_coordinates(resized_frame)
        processed_frames_data.append(frame_pixel_coords)
        
        # Print progress without being too verbose for every single frame if many frames
        if (i + 1) % 100 == 0 or i == len(frames_to_process) - 1 : # Print every 100 frames or on the last frame
            print(f"Processed frame {frame_number + 1}/{total_frames_in_video}...")

    cap.release() # Release video capture object

    time_for_preprocess = time.time() - start_time
    print(f"--- Preprocessing finished in {time_for_preprocess:.2f} seconds ---")

    if not processed_frames_data:
        print("No frames were processed. Exiting.")
        return
        
    print(f"Starting ASCII playback at {video_fps:.2f} FPS...")
    # Give a moment for the user to see the message before clearing screen
    time.sleep(2) 
    
    play_ascii_animation(processed_frames_data, video_fps)

    total_script_time = time.time() - start_time
    print(f"--- Total execution time {total_script_time:.2f} seconds ---")
    print(f"--- (Preprocessing was {time_for_preprocess:.2f} seconds) ---")

if __name__ == '__main__':
    main()



# import cv2
# import numpy as np
# import os
# import time


# start_time = time.time()
# output_width = 480
# output_height = 360 
# threshold_level = 50
# total_coordinates = []
# char_for_black = '#'
# ascii_canvas = [[' ' for _ in range(240)] for _ in range(90)]
# x_scale_factor = 2
# y_scale_factor = 4
# def black_pixel_coordinates(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     black_pixel_coordinates = np.column_stack(np.where(gray < threshold_level))
#     scaled_black_pixel_coordinates = []
#     for y_orig, x_orig in black_pixel_coordinates: # Iterate through original black pixel coordinates
#         # Apply the scaling factors to get the coordinates on the smaller ASCII grid
#         scaled_y = int(y_orig / y_scale_factor)
#         scaled_x = int(x_orig / x_scale_factor)

#         # Ensure scaled coordinates are within the target output dimensions
#         # This check is important during pre-processing
#         if 0 <= scaled_x < output_width and 0 <= scaled_y < output_height:
#             # Store the SCALED coordinate
#             scaled_black_pixel_coordinates.append((scaled_y, scaled_x))
#     return scaled_black_pixel_coordinates

# def ascii(total_coordinates):
#     for black_pixel_coordinates in total_coordinates: 
#         for c in range(len(ascii_canvas)):
#             for r in range(len(ascii_canvas[0])):
#                 ascii_canvas[c][r] = ' '
#         for y, x in black_pixel_coordinates:
#             if 0 <= x < output_width and 0 <= y < output_height:
#                 ascii_canvas[y][x] = char_for_black
#         os.system('cls')
#         for row in ascii_canvas:
#             print("".join(row))
#         # time.sleep(0.001)  # Adjust the sleep time as needed for your display speed
    
# video_path = 'C:\\Users\\revas\\Source\\Repos\\funlittleprojects\\badapple\\BadAppleOriginal.mp4'
# cap = cv2.VideoCapture(video_path)

# sample_rate = 1
# total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# for fno in range(0, total_frames, sample_rate):
#     cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
#     _, image = cap.read()
#     total_coordinates.append(black_pixel_coordinates(image))
#     print(f"Processed frame {fno + 1}/{total_frames} at sample rate {sample_rate}")
# time_for_preprocess = "--- %s seconds ---" % (time.time() - start_time)
# print("Time for preprocessing " + time_for_preprocess)
# ascii(total_coordinates)
# time_for_all = "--- %s seconds ---" % (time.time() - start_time)
# print("Time for preprocessing " + time_for_preprocess)
# print("Time for all " + time_for_all)
# 311 seconds
# 221 seconds at sample rate 2
# 219 seconds is the video duration
# 45 pre process 445 render at sampele rate 1

# Goal is to get the render time as low as possible
# 385 pre processing 572 in total. That is 187 seconds for rendering! 957 in total so way worse 
# but good for showing off the render speed after processing.