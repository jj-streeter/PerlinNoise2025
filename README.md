
# Project Overview:
A program that uses Perlin noise to generate 2D images

# Intructions for running:
1. Download or clone the PerlinNoise2025 project
2. Run main.py in a terminal and provide input when prompted
3. Images will be saved in the same folder as the project

# Topics and skills developed:
### Pillow and NumPy image processing
Created and manipulated RGB images pixel by pixel, using Pillow for image generation and NumPy for seeded random values
### Interpolation and vector mathematics
Applied 2D vectors, dot products, trigonometry, linear interpolation, and bilinear interpolation to calculate smooth noise values and movement directions
### Dilation and neighboring operations
Used 8-neighbor pixel checks to expand river paths and create shoreline effects through repeated dilation passes
### Procedural generation with seeded randomness
Generated repeatable terrain, textures, and river layouts from mathematical rules and integer seeds
### Perlin noise algorithm
Implemented 2D Perlin noise with gradient vectors and a fade function to produce smooth, natural-looking terrain and guide Perlin worm river paths
