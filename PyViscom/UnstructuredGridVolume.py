import numpy as np
import sys
from pyrr import Vector3 as vec3


class AABB():
    def __init__(self, vertices):
        self.min = [np.amin(vertices, axis=0), np.amin(vertices, axis=1), np.amin(vertices, axis=2)]
        self.max = np.max(vertices)
        print(self.min)

def load_node(node_file):
    with open(node_file, "r") as node:
        volume_data = node.readlines()
        [node_count, node_dim, node_attr, _] = map(int, volume_data[0].split())
        points = []
        data = []
        for i in range(1, node_count):
            [_, x, y, z, attr0, attr1, attr2] = map(float, volume_data[i].split())
            points.append(vec3([x, y, z]))
            data.append(np.array([attr0, attr1, attr2]))
        AABB(points)


if __name__ == '__main__':
    load_node("../media/unstructured/colorcube.node")
