##import testingEnemies
import heapq
import numpy as mpy
from map import towerLoc

def adjacent(aroundPos, rows, cols, grid):
    i,j = aroundPos
    for hor,ver in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        ihor, jver = i + hor, j + ver
        if 0<= ihor<rows and 0<=jver<cols and grid[ihor][jver] ==0:
            yield ihor, jver

def towerCost(r,c, rows, cols, towerLocations):
    radius = 3
    cost = 0
    for rx in range(-radius, radius+1):
        for ry in range(-radius,radius+1):
            nr,nc = r+rx,c+ry
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) in towerLocations:
                    cost += 1
    return cost

def heuristic(A,B):
    return abs(A[0]-B[0]) + abs(A[1]-B[1])


def aSearc(grid, startPos, endPos, towerLocations):
    rows, cols = grid.shape
    opening = [(0,startPos)]
    gS = {startPos: 0}
    comingFrom = {}

    while opening:
        _,temp = heapq.heappop(opening) ##we are grabbing our starting pos
        if temp == endPos:
            completedPath = []
            while temp in comingFrom:
                completedPath.append(temp)
                temp = comingFrom[temp]
            completedPath.append(startPos) ##adds start at end because we will reverse list
            return completedPath[::-1] ##returns a reversed list
        for neigh in adjacent(temp, rows, cols, grid):
            x,y = neigh
            gCost = gS[temp] + 1 + towerCost(x,y,rows,cols,towerLocations)

            if neigh not in gS or gCost < gS[neigh]:
                gS[neigh] = gCost
                f = gCost + heuristic(neigh,endPos)
                heapq.heappush(opening,(f,neigh))
                comingFrom[neigh] = temp
    return None

##path = aSearc(testingEnemies.grid, (0,0),(10, 19),[])
##print(path)