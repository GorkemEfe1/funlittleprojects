# Assume these are the coordinates of your "black" pixels
# These coordinates are relative to the desired output size, not the original image
black_pixel_coordinates = [
    (10, 5), (11, 5), (12, 5), (13, 5), # Top line
    (10, 6),                         # Left side
    (10, 7), (11, 7), (12, 7), (13, 7), # Bottom line
    (13, 6),                         # Right side
]

# Define the dimensions of your ASCII output grid
output_width = 20
output_height = 10

# Define the character to use for "black" pixels
char_for_black = '#'
# Define the character for "white" pixels (space)
char_for_white = ' '

# 1. Create an empty canvas (list of lists) filled with spaces
ascii_canvas = [[char_for_white for _ in range(output_width)] for _ in range(output_height)]

# 2. Place the black characters on the canvas based on coordinates
for x, y in black_pixel_coordinates:
    # Check if the coordinate is within the canvas bounds
    if 0 <= x < output_width and 0 <= y < output_height:
        ascii_canvas[y][x] = char_for_black
    else:
        # Optional: Handle coordinates outside the bounds if necessary
        print(f"Warning: Coordinate ({x}, {y}) is outside the defined canvas size.")


# 3. Print the canvas row by row
print("--- ASCII Art Output ---")
for row in ascii_canvas:
    print("".join(row))
print("------------------------")

# Example of what this should print (a simple square/rectangle):
# --- ASCII Art Output ---
#
#
#
#
#           ####
#           #  #
#           ####
#
#
#
# ------------------------
