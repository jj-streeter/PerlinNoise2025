'''
This program generates a a 2D Perlin noise image in grayscale.
This file was created to develop and test the algorithm
'''

from PIL import Image
import numpy as np
import math

# generate random 2D vector
def random_vector(x, y, seed=0):
    np.random.seed(int(x * 1000 + y + seed))
    angle = np.random.rand() * math.pi * 2

    return (math.cos(angle), math.sin(angle))

# return dot product of two vectors
def dot(a,b):
    return a[0] * b[0] + a[1] * b[1]

def get_perlin_grid(x, y, grid):
    return grid[int(x)][int(y)]

def fade(t):
    return ((6 * t - 15) * t + 10) * t * t * t

# return Perlin noise value
def perlin_noise2D(x, y, grid):
    # the two factors used
    ix = int(x)
    iy = int(y)
    x_factor = x - ix
    y_factor = y - iy

    # four corners
    v00 = (x_factor, y_factor)
    v10 = (x_factor - 1, y_factor)
    v01 = (x_factor, y_factor - 1)
    v11 = (x_factor - 1, y_factor - 1)
    
    # dot products of each corner vector with point on grid
    dot00 = dot(v00, get_perlin_grid(ix + 0, iy + 0, grid))
    dot10 = dot(v10, get_perlin_grid(ix + 1, iy + 0, grid))
    dot01 = dot(v01, get_perlin_grid(ix + 0, iy + 1, grid))
    dot11 = dot(v11, get_perlin_grid(ix + 1, iy + 1, grid))

    # interpolate between the dot products to find the value of point 
    # u and v range from [0.0, 1.0]
    u = fade(x_factor)
    v = fade(y_factor)

    a = (1 - u) * dot00 + u * dot10
    b = (1 - u) * dot01 + u * dot11
    c = (1 - v) * a + v * b

    return c

def generate_noise(w, h, scale, seed):
    image = Image.new("RGB", (w, h))
    raster = image.load()

    # generate grid of random vectors
    grid = [[random_vector(x, y, seed) for x in range(w)] for y in range(h)]

    for x in range(image.width):
        for y in range(image.height):
            sx = x / scale
            sy = y / scale

            perlin = perlin_noise2D(sx, sy, grid)
            val = int((perlin + 1) * 255/2) # tweaking how this value is calculated changes the image in interesting ways

            raster[x,y] = (val, val, val)

    image.save("PerlinNoiseTest.png")

# Binary (black and white) Perlin noise image
def generate_binary_noise(w, h, scale, seed):
    image1 = Image.new("RGB", (w, h))
    raster1 = image1.load()

    grid = [[random_vector(x, y, seed) for x in range(w)] for y in range(h)]

    for x in range(image1.width):
        for y in range(image1.height):
            sx = x / scale
            sy = y / scale

            perlin = perlin_noise2D(sx, sy, grid)
            if perlin > 0:
                v = 0
            else:
                v = 255

            raster1[x,y] = (v, v, v)

generate_noise(128, 128, 30, 4289)