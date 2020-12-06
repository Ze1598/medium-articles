from PIL import Image

# Create a blank grey image
wip_img = Image.new("RGBA", (550, 450), "#f2f2f2")
# Load the santa hat
santa_hat = Image.open("santa_hat.png")
# At first this is just a black rectangle of the same size as the hat
shadow = Image.new("RGBA", santa_hat.size, color="black")

# Coordinates at which to draw the hat and shadow
hat_coords = (25, 25)
shadow_coords = (30, 30)

# Custom-mask the shadow so it has the same shape as the santa hat
wip_img.paste(shadow, shadow_coords, mask=santa_hat)
# Now paste the hat on top of the shadow
wip_img.paste(santa_hat, box=hat_coords, mask=santa_hat)

wip_img.save("result.png")