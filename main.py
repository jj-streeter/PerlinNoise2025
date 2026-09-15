'''
This program generates 
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

# generate a 2D Perlin noise image
def generate_noise(w, h, scale, seed):
    image = Image.new("RGB", (w, h))
    raster = image.load()

    # generate grid of random vectors with seed
    grid = [[random_vector(x, y, seed) for x in range(w)] for y in range(h)]

    for x in range(image.width):
        for y in range(image.height):
            sx = x / scale
            sy = y / scale

            perlin = perlin_noise2D(sx, sy, grid)
            v = int((perlin + 1) * 255 - 255/2)

            raster[x,y] = (v, v, v)

    return image

# generate a Perlin worm - a randomly generated path (for rivers)
def perlin_worm(image, start_x, start_y, seed, duration, color, exempt_colors):
    raster = image.load()
    w, h = image.size

    # starting position
    x, y = start_x, start_y
    raster[x,y] = color

    # generate grid of random vectors
    grid = [[random_vector(x, y, seed) for x in range(w)] for y in range(h)]

    # generate the path
    for i in range(duration):
        sx = x / 10.0
        sy = y / 10.0

        # map the Perlin noise value to an angle
        perlin = perlin_noise2D(sx, sy, grid)
        angle = (perlin + 1) * math.pi

        dx = int(round(math.cos(angle)))
        dy = int(round(math.sin(angle)))

        # find the next path pixel and update the color
        x = (x + dx) % w
        y = (y + dy) % h

        if raster[x,y] not in exempt_colors:
            raster[x,y] = color
        else:
            return image # end path when it reaches a pixel of the same color
    
    return image

# dilation takes an image and target color, and finds pixels next to two or more
# of that target color, and changes it to that same color
# used to widen rivers
def dilation(image, reference_image, color):
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

    pixel_count = 0
    pixels_to_change = []

    for x in range(image.width):
        for y in range(image.height):
            if raster[x,y] != color: # detect non-path pixels

                # check 8 neighbor pixels
                for dx, dy in offsets:
                    nx = x + dx
                    ny = y + dy

                    # check pixel position is in range
                    if 0 <= nx <= image.width - 1 and 0 <= ny <= image.height - 1:
                        reference_pixel = reference_image[nx, ny]
                        if raster[nx, ny] == color and reference_pixel[0] >= 100: # only dilate on river pixels on land, not ocean pixels
                            pixel_count += 1
                
                if pixel_count >= 2:
                    pixels_to_change.append((x,y))

                pixel_count = 0
    
    for x, y in pixels_to_change:
        raster[x,y] = color
    
    return image

# altered dilation function for adding 'shores' of pixels around a target color
def add_shore(image, shore_color, target_color, exempt_colors):
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

    pixel_count = 0
    pixels_to_change = []

    for x in range(image.width):
        for y in range(image.height):
            if raster[x,y] not in exempt_colors: # detect valid non-path pixels

                # check 8 neighbor pixels
                for dx, dy in offsets:
                    nx = x + dx
                    ny = y + dy

                    # check pixel position is in range
                    if 0 <= nx <= image.width - 1 and 0 <= ny <= image.height - 1:
                        if raster[nx, ny] == target_color:
                            pixel_count += 1
                
                if pixel_count >= 2:
                    pixels_to_change.append((x,y))

                pixel_count = 0
    
    for x, y in pixels_to_change:
        raster[x,y] = shore_color
    
    return image

# add multiple rivers (including dilation and adding shores)
def add_rivers(image, land_raster, scale_ratio, num_rivers, exempt_colors, seed):
    river_color = (38, 183, 255)
    shore_color = (217, 179, 147)

    raster = image.load()

    for i in range(num_rivers):
        # find random valid starting point for a river
        np.random.seed(seed + i)

        pixel = exempt_colors[0]
        while pixel in exempt_colors:
            x_rand = np.random.randint(0, image.width - 1)
            y_rand = np.random.randint(0, image.height - 1)

            pixel = raster[x_rand, y_rand]

        duration = np.random.randint(0, int((image.width - 1) / 2))
        image = perlin_worm(image, x_rand, y_rand, seed + i, duration, river_color, exempt_colors)
    
    # perform dilation to widen the rivers
    if scale_ratio < 0.1:
        dilation_times = 6
    elif scale_ratio < 0.25:
        dilation_times = 5
    elif scale_ratio < 0.5:
        dilation_times = 4
    elif scale_ratio < 1:
        dilation_times = 3
    elif scale_ratio < 3:
        dilation_times = 2
    elif scale_ratio < 5:
        dilation_times = 1
    else:
        dilation_times = 0

    for i in range(dilation_times):
        image = dilation(image, land_raster, river_color)

    # add sand shores around rivers
    image = add_shore(image, shore_color, river_color, exempt_colors)

    return image

# generate composite Perlin noise map, using multiple layers, Perlin worms, dilation, and adding shores
def generate_map(w, h, scale, seed, rivers):
    land = generate_noise(w, h, scale, seed)
    land_raster = land.load()

    image = Image.new("RGB", (w, h))
    image_raster = image.load()

    # land and ocean colors
    deep_water = (16, 76, 179)
    medium_water = (62, 133, 255)
    shallow_water = (38, 183, 255)
    sand = (217, 197, 147)
    light_grass = (135, 158, 54)
    dark_grass = (67, 87, 26)
    dirt = (112, 78, 40)
    dark_rock = (125, 102, 82)
    light_rock = (189, 188, 187)
    ice = (228, 238, 247)
    snow = (255, 255, 255)

    # map the land and oceans
    for x in range(image.width):
        for y in range(image.height):
            land_pixel = land_raster[x,y]

            if land_pixel[0] < 50:
                image_raster[x,y] = deep_water
            
            elif land_pixel[0] < 75:
                image_raster[x,y] = medium_water
            
            elif land_pixel[0] < 100:
                image_raster[x,y] = shallow_water
            
            elif land_pixel[0] < 120:
                image_raster[x,y] = sand
            
            elif land_pixel[0] < 140:
                image_raster[x,y] = light_grass
            
            else:
                if land_pixel[0] < 170:
                    image_raster[x,y] = dark_grass
                
                elif land_pixel[0] < 190:
                    image_raster[x,y] = dirt

                elif land_pixel[0] < 210:
                    image_raster[x,y] = dark_rock

                elif land_pixel[0] < 230:
                    image_raster[x,y] = light_rock

                elif land_pixel[0] < 245:
                    image_raster[x,y] = ice
                
                else:
                    image_raster[x,y] = snow
    
    # add rivers using Perlin worms
    if rivers == 'y':
        sr = (image.width + image.height) / 2 / scale
        np.random.seed(seed)
        num_rivers = np.random.randint(0, 30)
        image = add_rivers(image, land_raster, sr, num_rivers, [deep_water, medium_water, shallow_water, ice, snow], seed)

    return image

def main():
    w = int(input("Image width: "))
    h = int(input("Image height: "))
    s = int(input("Scale: "))
    seed = int(input("Seed: "))
    rivers = (input("Add rivers? (y/n): "))
    img_name = input("Image filename: ")

    generate_map(w, h, s, seed, rivers.lower()).save(img_name + ".png")

main()

# reccomended inputs for map sizes:

# Small map: 64x64, scale 30
# Medium map: 128x128, scale 80
# Large map: 256x256, scale 75

# in general, larger scales create more zoomed in maps
# depending on the size of the image, the scale ratio will change
# and affect how rivers are generated as well as the amount of dilation
