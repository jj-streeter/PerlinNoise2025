'''
This program contains functions to generate white noise images in both RGB color and RGB grayscale.
'''

from PIL import Image
import numpy as np

def white_noiseRGB(w, h):
    wnImage = Image.new("RGB", (w, h))
    wnRaster = wnImage.load()

    for x in range(wnImage.width):
        for y in range(wnImage.height):
            r = np.random.randint(255)
            g = np.random.randint(255)
            b = np.random.randint(255)

            wnRaster[x, y] = (r, g, b)

    wnImage.save("WhiteNoise.png")

def white_noiseGray(w, h):
    grayNoise = Image.new("RGB", (w, h))  
    grayRaster = grayNoise.load()

    for x in range(grayNoise.width):
        for y in range(grayNoise.height):
            r = np.random.randint(255)
            g = np.random.randint(255)
            b = np.random.randint(255)

            # Apply gray scale
            gray = 0.2 * r + 0.7 * g + 0.1 * b
            gray = int(gray)

            grayRaster[x,y] = (gray, gray, gray)

    grayNoise.save("GrayscaleWhiteNoise.png")
