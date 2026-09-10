from PIL import Image
import numpy as np

'''
Linear Interpolation formula

( 1 - x ) * A + ( x * B )
'''

# v0 is the y value of the first point
# v1 is the y value of the second point
# t is the x value between v0 and v1 for which to find the corresponding y value
# 0 <= t <= 1
def lerp(v0, v1, t):
    return (1 - t) * v0 + (t * v1)

print(lerp(1.3, 2, 0.3))


def bilerp(tx, ty, c00, c10, c01, c11):
    # interpolate first two x axes
    a = c00 * (1 - tx) + c10 * tx
    b = c01 * (1 - tx) + c11 * tx
    # return interpolation of y axis
    return a * (1 - ty) + b * ty