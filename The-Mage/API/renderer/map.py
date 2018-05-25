import numpy

class Map:

    def __init__(self, matrix):
        self.matrix = matrix
        self.x = 0
        self.y = 0
        self.m = 30
        self.wall = 0
        self.mx = len(max(self.matrix, key=len))
        self.my = len(self.matrix)

    def move(self, x, y):
        self.matrix[self.y][self.x] = 0
        self.x = x
        self.y = y
        self.matrix[y][x] = 2

    def getrows(self, radius):
        _r = [i for i in range(radius+1+radius)]
        _x = [i for i in range(self.x-radius, self.x+1+radius)]
        _y = [i for i in range(self.y-radius, self.y+1+radius)]
        array = [[0 for i in range(radius+1+radius)] for l in range(radius+1+radius)]
        for y in _r:
            for x in _r:
                try:
                    if _y[y] < 0 or _x[x] < 0:
                        array[y][x] = 3
                    else:
                        array[y][x] = self.matrix[_y[y]][_x[x]]
                except:
                    array[y][x] = 3
        return array

class _Map:

    def __init__(self, matrix):
        self.matrix = matrix
        self.x = 0
        self.y = 0
        self.oy = 0
        self.ox = 0
        self.mx = len(max(matrix, key=len))
        self.my = len(matrix)

    @property
    def abx(self):
        return self.x//30

    @property
    def aby(self):
        return self.y//30

    def move(self, x, y):
        self.matrix[self.x][self.y] = 0
        self.ox = x
        self.oy = y
        self.x = self.abx
        self.y = self.aby
        self.matrix[self.x][self.y] = 2

    def getrows(self, radius):
        ra = (1+radius+1+radius+1)
        _r = [i for i in range(ra)]
