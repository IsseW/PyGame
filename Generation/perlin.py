import cv2
import random
import numpy as np
import math
from noise import perlin
noise = perlin.SimplexNoise()

def GetNoise(pos, distortion, offset):
    return (noise.noise2(pos[0] * distortion + offset, pos[1] * distortion + offset) + 1) / 2

def GetColor(position):
    v = GetNoise(position, 0.01, 0) * 255
    return (v, v, v)


def GeneratePerlin(imageSize):
    img = np.zeros((imageSize,imageSize,3), np.uint8)

    for i in range(imageSize):
        for j in range(imageSize):
            img[i][j] = GetColor((i, j))
    
    cv2.imwrite('perlin.png',img)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

GeneratePerlin(400)
