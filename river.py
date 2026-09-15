'''
This program generates a 2D Perlin worm path on a blank image
This file was created to develop and test the algorithm for generating a river
on a Perlin noise map.
'''

from PIL import Image
import numpy as np
import math

# generate random 2D vector
# ranges for both x and y are [-1.0, 1.0]
def random_vector(x, y, seed=0):
    np.random.seed(int(x * 1000 + y + seed))
    angle = np.random.rand() * math.pi * 2

    return (math.cos(angle), math.sin(angle))

# compute dot product of two 2D vectors
def dot_2D(a, b):
    return a[0] * b[0] + a[1] * b[1]

# get the nearest grid point to pixel
def get_perlin_grid(x, y, grid):
    return grid[int(x)][int(y)]

# smoothing function for noise
def fade(t):
    return ((6 * t - 15) * t + 10) * t * t * t

# compute Perlin noise value for pixel
# The Perlin noise map is used in generating the path of the river
def perlin_noise2D(x, y, grid):
    # the two factors used
    ix = int(x)
    iy = int(y)

    # x factor and y factor range from [0.0, 1.0)
    x_factor = x - ix
    y_factor = y - iy

    # the four corners
    v00 = (x_factor, y_factor)
    v10 = (x_factor - 1, y_factor)
    v01 = (x_factor, y_factor - 1)
    v11 = (x_factor - 1, y_factor - 1)

    # dot products of each corner vector on the grid
    dot00 = dot_2D(v00, get_perlin_grid(ix + 0, iy + 0, grid))
    dot10 = dot_2D(v10, get_perlin_grid(ix + 1, iy + 0, grid))
    dot01 = dot_2D(v01, get_perlin_grid(ix + 0, iy + 1, grid))
    dot11 = dot_2D(v11, get_perlin_grid(ix + 1, iy + 1, grid))

    # interpolate the dot products to find the value of the point
    # u and v range from [0, 1]
    u = fade(x_factor)
    v = fade(y_factor)

    a = (1 - u) * dot00 + u * dot10
    b = (1 - u) * dot01 + u * dot11
    c = (1 - v) * a + v * b

    return c

def perlin_worm(image, start_x, start_y, seed, duration):
    raster = image.load()
    w, h = image.size

    # starting position
    x, y = start_x, start_y
    raster[x, y] = (38, 183, 255) 

    # generate grid of random vectors
    grid = [[random_vector(x, y, seed) for x in range(w)] for y in range(h)]

    for i in range(duration):
        sx = x / 10.0
        sy = y / 10.0

        perlin = perlin_noise2D(sx, sy, grid)
        angle = (perlin + 1) * math.pi  # map Perlin value to [0, 2pi]

        dx = int(round(math.cos(angle)))
        dy = int(round(math.sin(angle)))

        x = (x + dx) % w
        y = (y + dy) % h

        raster[x, y] = (38, 183, 255)  # mark the path

    image = dilation(image)  # thicken the river path    
    image = shore_dilation(image) # add river shore
    return image # return modified image with Perlin Worm path added

def dilation(image):
    raster = image.load()

    offsets = [ 
        (-1, -1),
        (0, -1), 
        (1, -1),   
        (-1, 0),   
        (1, 0), 
        (-1, 1),   
        (0, 1),  
        (1, 1)  
    ]

    river_count = 0

    pixels_to_change = []

    for x in range(image.width):
        for y in range(image.height):
            if raster[x,y] != (38, 183, 255): # detect non-river pixels

                # check 8 neighbor pixels
                for dx, dy in offsets:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx <= image.width - 1 and 0 <= ny <= image.height - 1:
                        if raster[nx,ny] == (38, 183, 255):
                            river_count += 1

                # if neighbor pixel is touching 2 river pixels, add it to the list of pixels to convert
                if river_count >= 2:
                    pixels_to_change.append((x,y))
                    

                river_count = 0
    
    for x, y in pixels_to_change:
        raster[x,y] = (38, 183, 255)

    return image 

# Add a shore around the river
def shore_dilation(image):
    raster = image.load()

    offsets = [ 
        (-1, -1),
        (0, -1), 
        (1, -1),   
        (-1, 0),   
        (1, 0), 
        (-1, 1),   
        (0, 1),  
        (1, 1)  
    ]

    river_count = 0

    pixels_to_change = []

    for x in range(image.width):
        for y in range(image.height):
            if raster[x,y] != (38, 183, 255): # detect non-river pixels

                # check 8 neighbor pixels
                for dx, dy in offsets:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx <= image.width - 1 and 0 <= ny <= image.height - 1:
                        if raster[nx,ny] == (38, 183, 255):
                            river_count += 1
                    
                if river_count >= 2:
                    pixels_to_change.append((x,y))
                
                river_count = 0
    
    for x, y in pixels_to_change:
        raster[x,y] = (217, 197, 147)
    
    return image
      
image = perlin_worm(Image.new("RGB", (100, 100)), 20, 20, 128, 100)
image.save("river_single.png")