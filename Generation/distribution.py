import cv2
import random
import numpy as np
import math
import random


def isValid(candidate, size, cellsize, radius, points, grid):
    if candidate[0] >= 0 and candidate[0] < size[0] and candidate[1] > 0 and candidate[1] < size[1]:
        cellX = math.floor(candidate[0] / cellsize)
        cellY = math.floor(candidate[1] / cellsize)
        if grid[cellX, cellY] != 0: return False
        searchStartX = cellX - 2
        searchEndX = (cellX + 2) % len(grid)
        searchStartY = cellY - 2
        searchEndY = (cellY + 2) % len(grid[searchEndX])

        for x in range(searchStartX, searchEndX + 1):
            for y in range(searchStartY, searchEndY + 1):
                pointIndex = grid[x][y] - 1
                if pointIndex >= 0:
                    dif = (candidate[0] - points[pointIndex][0], candidate[1] - points[pointIndex][1])
                    sqrDst = dif[0] * dif[0] + dif[1] * dif[1]
                    if sqrDst < radius*radius:
                        return False
        return True
    return False

def generatePoints(radius, size, samples = 15):
    cellsize = radius / math.sqrt(2)

    grid = np.zeros((math.ceil(size[0]/cellsize), math.ceil(size[1]/cellsize)), np.uint8)
    points = []
    spawnPoints = []

    spawnPoints.append((size[0]/2,size[1]/2))

    while len(spawnPoints) > 0:
        spawnIndex = random.randint(0, len(spawnPoints) - 1)
        spawnCenter = spawnPoints[spawnIndex]
        accepted = False
        
        for i in range(samples):
            angle = (random.randrange(10000)/10000) * math.pi * 2;
            direction = (math.sin(angle), math.cos(angle))
            dist = random.randrange(radius*1000, radius*2000) / 1000
            candidate = (spawnCenter[0] + direction[0] * dist, spawnCenter[1] + direction[1] * dist)
            if isValid(candidate, size, cellsize, radius, points, grid):
                points.append(candidate)
                spawnPoints.append(candidate)
                grid[math.floor(candidate[0]/cellsize)][math.floor(candidate[1]/cellsize)] = len(points);
                accepted = True
                break
        if not accepted:
            spawnPoints.remove(spawnCenter)
    print("points generated")
    return points

def drawPoints(img, points, radius, color = [255, 255, 255]):
    for i in range(len(points)):
        #print(points[i])
        cv2.circle(img, (int(points[i][0]), int(points[i][1])), radius, color, -1)
    print("points drawn")
    

size = (4000, 4000)

bigRadius = 2
bigRadius2 = 100

smallRadius = 1
smallRadius2 = 50

big = generatePoints(bigRadius2, size)
small = generatePoints(smallRadius2, size)

img = np.zeros((size[0],size[1],3), np.uint8)

drawPoints(img, small, smallRadius, [100, 100, 100])
drawPoints(img, big, bigRadius, [200, 200, 200])

cv2.imwrite('distribution.png',img)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

