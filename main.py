from PIL import Image

size = 300
img = Image.new("RGB", (size, size), "white")

img.save("white_square.png")