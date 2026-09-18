<img width="256" height="256" alt="image" src="https://github.com/user-attachments/assets/ce07f0b4-3f03-4de6-aa19-e2c8876b2f78" />
<img width="256" height="256" alt="image" src="https://github.com/user-attachments/assets/a57c0864-b2b5-4951-9d56-6a51ae54ecd8" />
<img width="256" height="256" alt="image" src="https://github.com/user-attachments/assets/30f5e1f8-2ce9-478e-a05e-c195434d54f3" />

# Project Overview:
This project was completed from August to December of 2025 for CSCI 2620 2D Graphics at University of Nebraska at Omaha. The objective was to learn and implement the algorithm developed by Ken Perlin, a gradient noise function, to procedurally generate unique and replicable images that resemble geographical maps. This algorithm has applications in creating organic image textures and terrain generation for computer games, which was the inspiration for this project. 

# Instructions for running:
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

# The Perlin Noise Algorithm:
Below is a simplified explanation of how the algorithm is implemented in this project. View Ken Perlin's paper here: https://doi.org/10.1145/566654.566636 
### 1. Create a seeded direction grid
An integer seed is used to define a grid of random 2D vectors. 
### 2. For each pixel, find the four nearby grid points
These points provide the local information needed to calculate the pixel's noise value.
### 3. Compute dot products for the pixel and all four vector points
The pixel's position is compared with the direction at each nearby grid point, determining how strongly each point influences the pixel's value.
### 4. Smoothly blend the results
The four results are smoothly blended together using interpolation, creating changes that look organic rather than boxy
### 5. Convert the value into terrain colors
The final calculated value of the pixel is then mapped to a specific color
