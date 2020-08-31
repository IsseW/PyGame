import cv2
import random
import numpy as np
import math
import random

def GetColor(position):
    v = random.random() * 255
    return (v, v, v)


def GenerateNoise(imageSize):
    img = np.zeros((imageSize,imageSize,3), np.uint8)

    for i in range(imageSize):
        for j in range(imageSize):
            img[i][j] = GetColor((i, j))
    
    cv2.imwrite('noise.png',img)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

GenerateNoise(400)
