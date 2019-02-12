import numpy as np
from PyViscom.Util import AABB, Tetrahedron
import pyrr


class UnstructuredGridVolume(object):
    def __init__(self):
        self.point_bounds = None
        self.data = []
        self.points = []
        self.tetra_indices = []
        self.tetras = []
        self.faces = []
        self.planes = []

    def __str__(self):
        return "data: " + str(self.data) \
               + "\npoints: " + str(self.points) \
               + "\ntetra indices: " + str(self.tetra_indices) \
               + "\nfaces: " + str(self.faces)

    def create_tetras(self):
        self.tetras = []
        for ti in self.tetra_indices:
            a = self.points[ti[0]]
            b = self.points[ti[1]]
            c = self.points[ti[2]]
            d = self.points[ti[3]]
            self.tetras.append(Tetrahedron(a, b, c, d))

    def create_planes(self):
        self.planes = []
        for face in self.faces:
            a = self.points[face.x]
            b = self.points[face.y]
            c = self.points[face.z]
            n = pyrr.vector3.normalize(pyrr.vector3.cross(b - a, c - a))
            d = pyrr.vector3.dot(n, a)
            self.planes.append(pyrr.Vector4([n[0], n[1], n[2], d]))


def load_node(node_file, vol):
    with open(node_file, "r") as node:
        volume_data = node.readlines()
        [node_count, _, _, _] = map(int, volume_data[0].split())
        vol.points = []
        vol.data = []
        for i in range(1, node_count+1):
            [_, x, y, z, attr0, attr1, attr2] = map(float, volume_data[i].split())
            vol.points.append(pyrr.Vector3([x, y, z]))
            vol.data.append(np.array([attr0, attr1, attr2]))
        vol.point_bounds = AABB(vertices=vol.points)


def load_ele(ele_file, vol):
    with open(ele_file, "r") as ele:
        volume_data = ele.readlines()
        [ele_count, _, _] = map(int, volume_data[0].split())
        vol.tetra_indices = []
        for i in range(1, ele_count+1):
            [_, x, y, z, w] = map(float, volume_data[i].split())
            vol.tetra_indices.append(pyrr.Vector4([x, y, z, w], dtype=int))


def load_face(face_file, vol):
    with open(face_file, "r") as face:
        volume_data = face.readlines()
        [face_count, _] = map(int, volume_data[0].split())
        vol.faces = []
        for i in range(1, face_count+1):
            [_, x, y, z] = map(float, volume_data[i].split())
            vol.faces.append(pyrr.Vector3([x, y, z], dtype=int))


if __name__ == '__main__':
    vol = UnstructuredGridVolume()
    load_node("../media/unstructured/colorcube.node", vol)
    load_ele("../media/unstructured/colorcube.ele", vol)
    load_face("../media/unstructured/colorcube.face", vol)
    vol.create_planes()
    vol.create_tetras()
