import numpy as np

class AABB():
    def __init__(self, vertices=None, minimum=None, maximum=None):
        self.min = minimum
        self.max = maximum
        if vertices is not None:
            self.min = np.minimum.accumulate(vertices)[-1]
            self.max = np.maximum.accumulate(vertices)[-1]

    def size(self):
        return self.max - self.min

    def __sub__(self, other):
        return AABB(minimum=self.min - other.min, maximum=self.max - other.max)

    def __add__(self, other):
        return AABB(minimum=self.min + other.min, maximum=self.max + other.max)

    def __mul__(self, other):
        if type(other) == AABB:
            return AABB(minimum=self.min * other.min, maximum=self.max * other.max)
        elif type(other) == float or type(other) == int:
            return AABB(minimum=self.min * other, maximum=self.max * other)
        else:
            raise ValueError("Not implemented")

    def __truediv__(self, other):
        if type(other) == AABB:
            return AABB(minimum=self.min / other.min, maximum=self.max / other.max)
        elif type(other) == float or type(other) == int:
            return AABB(minimum=self.min / other, maximum=self.max / other)
        else:
            raise ValueError("Not implemented")

    def __str__(self):
        return "min: " + str(self.min) + " max: " + str(self.max)

    @staticmethod
    def union(a, b):
        return AABB(minimum=np.minimum(a.min, b.min), maximum=np.maximum(a.max, b.max))


class Tetrahedron(object):
    def __init__(self, v0, v1, v2, v3):
        self.v = np.array([v0, v1, v2, v3])

    def volume(self):
        a = self.v[1] - self.v[0]
        b = self.v[2] - self.v[0]
        c = self.v[3] - self.v[0]
        return np.abs(np.dot(a, np.cross(b, c))) / 6.0
