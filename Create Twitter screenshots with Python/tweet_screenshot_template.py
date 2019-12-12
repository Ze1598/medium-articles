from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

# Constants
# -----------------------------------------------------------------------------
# Set the font to be used
FONT_USER_INFO = ImageFont.truetype("arial.ttf", 90, encoding="utf-8")
FONT_TEXT = ImageFont.truetype("arial.ttf", 110, encoding="utf-8")
# Image dimensions (pixels)
WIDTH = 2376
HEIGHT = 2024
# Color scheme
COLOR_BG = 'white'
COLOR_NAME = 'black'
COLOR_TAG = (64, 64, 64)
COLOR_TEXT = 'black'
# Write coordinates
COORD_PHOTO = (250, 170)
COORD_NAME = (600, 185)
COORD_TAG = (600, 305)
COORD_TEXT = (250, 510)
# Extra space to add in between lines of text
LINE_MARGIN = 15
# -----------------------------------------------------------------------------

# Information for the image
# -----------------------------------------------------------------------------
user_name = "José Fernando Costa"
user_tag = "@soulsinporto"
text = "Go out there and do some fun shit, not because it makes money, but because it is fun for you!"
img_name = "work_towards_better_tomorrow"
# -----------------------------------------------------------------------------

# Setup of variables and calculations
# -----------------------------------------------------------------------------
# Break the text string into smaller strings, each having a maximum of 37\
# characters (a.k.a. create the lines of text for the image)
text_string_lines = wrap(text, 37)

# Horizontal position at which to start drawing each line of the tweet body
x = COORD_TEXT[0]

# Current vertical position of drawing (starts as the first vertical drawing\
# position of the tweet body)
y = COORD_TEXT[1]

# Create an Image object to be used as a means of extracting the height needed\
# to draw each line of text
temp_img = Image.new('RGB', (0, 0))
temp_img_draw_interf = ImageDraw.Draw(temp_img)

# List with the height (pixels) needed to draw each line of the tweet body
# Loop through each line of text, and extract the height needed to draw it,\
# using our font settings
line_height = [
    temp_img_draw_interf.textsize(text_string_lines[i], font=FONT_TEXT)[1]
    for i in range(len(text_string_lines))
]
# -----------------------------------------------------------------------------

# Image creation
# -----------------------------------------------------------------------------
# Create what will be the final image
img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
# Create the drawing interface
draw_interf = ImageDraw.Draw(img)

# Draw the user name
draw_interf.text(COORD_NAME, user_name, font=FONT_USER_INFO, fill=COLOR_NAME)
# Draw the user handle
draw_interf.text(COORD_TAG, user_tag, font=FONT_USER_INFO, fill=COLOR_TAG)

# Draw each line of the tweet body. To find the height at which the next\
# line will be drawn, add the line height of the next line to the current\
# y position, along with a small margin
for index, line in enumerate(text_string_lines):
    # Draw a line of text
    draw_interf.text((x, y), line, font=FONT_TEXT, fill=COLOR_TEXT)
    # Increment y to draw the next line at the adequate height
    y += line_height[index] + LINE_MARGIN

# Load the user photo (read-mode). It should be a 250x250 circle 
user_photo = Image.open('user_photo.png', 'r')

# Paste the user photo into the working image. We also use the photo for\
# its own mask to keep the photo's transparencies
img.paste(user_photo, COORD_PHOTO, mask=user_photo)

# Finally, save the created image
img.save(f'{img_name}.png')
# -----------------------------------------------------------------------------