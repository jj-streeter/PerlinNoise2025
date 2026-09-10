from PIL import Image
import numpy as np

wnImage = Image.new("RGB", (128, 128))
wnRaster = wnImage.load()

for x in range(wnImage.width):
    for y in range(wnImage.height):
        r = np.random.randint(255)
        g = np.random.randint(255)
        b = np.random.randint(255)

        wnRaster[x, y] = (r, g, b)

wnImage.save("./WhiteNoise.png")

grayNoise = Image.new("RGB", (128, 128))  
grayRaster = grayNoise.load()

for x in range(grayNoise.width):
    for y in range(grayNoise.height):
        r = np.random.randint(255)
        g = np.random.randint(255)
        b = np.random.randint(255)

        gray = 0.2 * r + 0.7 * g + 0.1 * b
        gray = int(gray)

        grayRaster[x,y] = (gray, gray, gray)

grayNoise.save("GrayscaleWhiteNoise.png")
