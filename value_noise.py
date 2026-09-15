'''
This program takes an image width and height in pixels, a scale factor, and an integer seed value as input to generate a value noise image
in either grayscale or color RGB.
'''

from PIL import Image
import numpy as np

# pseudo-random number generator using hashing function and seed
def random_value(x, y, seed=0):
    np.random.seed(int(x * 1000 + y + seed))
    return np.random.rand()

# cubic Hermite curve/smoothstep 
def smoothstep(t):
    return t * t * t * ((6 * t * t) - (15 * t) + 10)
    #return t * t * (3 - 2 * t) # 3t^2 - 2t^3

# generate noise value
def noise_2d(x, y, seed=0):
    # corner coordinates
    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    x1 = x0 + 1
    y1 = y0 + 1 

    # fractional parts
    xf = x - x0
    yf = y - y0

    # random values at four corners
    v00 = random_value(x0, y0, seed)
    v10 = random_value(x1, y0, seed)
    v01 = random_value(x0, y1, seed)
    v11 = random_value(x1, y1, seed)

    # interpolate x axis
    ix0 = v00 + smoothstep(xf) * (v10 - v00)
    ix1 = v01 + smoothstep(xf) * (v11 - v01)

    # interpolate y axis
    noise_value = ix0 + smoothstep(yf) * (ix1 - ix0)

    return noise_value * 255

# generate random noise image
def generate_noise(w, h, scale, grayscale, seed=0):
    noise_Image = Image.new("RGB", (w, h))
    raster = noise_Image.load()

    for x in range(noise_Image.width):
        for y in range(noise_Image.height):
            val = int(noise_2d(x / scale, y / scale, seed))

            if (grayscale == 'y'):
                raster[x,y] = (val, val, val)
            else:
                if (val > 220):
                    raster[x,y] = (245, 238, 218)
                elif (val > 200):
                    raster[x,y] = (194, 189, 176)
                elif (val > 180):
                    raster[x,y] = (69, 68, 67)
                elif (val > 160):
                    raster[x,y] = (51, 37, 20)
                elif (val > 140):
                    raster[x,y] = (41, 64, 16)
                elif (val > 120):
                    raster[x,y] = (64, 112, 11)
                elif (val > 100):
                    raster[x,y] = (191, 187, 111)
                elif (val > 80):
                    raster[x,y] = (51, 166, 189)
                elif (val > 60):
                    raster[x,y] = (17, 50, 125)
                elif (val > 40):
                    raster[x,y] = (8, 31, 84)
                elif (val > 20):
                    raster[x,y] = (4, 20, 56)

    noise_Image.save("valueNoise.png")

def main():
    image_width = int(input("Image width: "))
    image_height = int(input("Image height: "))
    image_scale = int(input("Scale: "))
    grayscale = input("Grayscale? (y/n): ")
    seed = int(input("Seed: "))

    generate_noise(image_width, image_height, image_scale, seed, grayscale.lower())

main()