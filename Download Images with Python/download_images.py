import requests
from PIL import Image
from io import BytesIO

# Target image URL
url = "https://i.imgur.com/EdAGGFS.jpg"
# Get the text after the last slash in the URL, that is, the file name,\
# which includes its extension
file_name = url.split("/")[-1]

# Make a GET request for the URL
img_request = requests.get(url)
# Parse the content of the request to an in-memory binary stream and then\
# open that stream as an Image of the Pillow library
img = Image.open(BytesIO(img_request.content))
# Now that the request's content has been "transformed" to an image, just\
# save it as a new file in your computer
img.save(file_name)