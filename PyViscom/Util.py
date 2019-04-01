import numpy as np
import pyrr
import cv2

PIXEL_3_XL_CAMERA_MATRIX = np.array([
    [1.82068809e+03, 0.00000000e+00, 9.42263672e+02],
    [0.00000000e+00, 1.81550969e+03, 5.45563131e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

PIXEL_3_XL_CAMERA_MATRIX_STILL = np.array([
    [3.26806837e+03, 0.00000000e+00, 2.00608987e+03],
    [0.00000000e+00, 3.26443819e+03, 1.51012087e+03],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

PIXEL_3_XL_DISTORTION_COEFFICIENTS = np.array([0.22071439, -1.01127954, -0.00135397, -0.00178447, 0.72496869])
PIXEL_3_XL_DISTORTION_COEFFICIENTS_STILL = np.array(
    [1.60115065e-01, -6.99654230e-01, 9.95647782e-05, -4.89378151e-04, 8.38093507e-01])


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


def cv_to_gl_mat4(view_cv):
    """
    cv::Mat cv_to_gl = cv::Mat::eye(view_cv.rows, view_cv.cols, view_cv.type());
    cv_to_gl.at<T>(1, 1) = static_cast<T>(-1.0); // Invert the y axis
    cv_to_gl.at<T>(2, 2) = static_cast<T>(-1.0); // invert the z axis

    const cv::Mat view_matrix = cv_to_gl * view_cv; // transform axis
    view_gl = cv::Mat(view_cv.rows, view_cv.cols, view_cv.type());
    cv::transpose(view_matrix, view_gl); // row order to column order
    :return:
    """
    cv_to_gl = pyrr.matrix44.create_identity()
    cv_to_gl[1][1] = -1.0
    cv_to_gl[2][2] = -1.0
    view_matrix = pyrr.matrix44.multiply(cv_to_gl, view_cv)
    return view_matrix.T


def view_matrix_from_rvec_tvec(rvec, tvec):
    R, _ = cv2.Rodrigues(rvec)
    view = pyrr.matrix44.create_identity()
    view[0:3, 0:3] = R
    view[0:3, 3] = tvec.flatten()
    return cv_to_gl_mat4(view)


def projection_matrix_from_intrinsic_julian(camera_matrix, near, far, width, height):
    depth = far - near
    q = -(far + near) / depth
    qn = -2.0 * (far * near) / depth

    K00 = camera_matrix[0][0]  # alpha
    K01 = camera_matrix[0][1]  # s
    K02 = camera_matrix[0][2]  # x0
    K11 = camera_matrix[1][1]  # beta
    K12 = camera_matrix[1][2]  # y0

    return np.array([
        [2.0 * K00 / width, -2.0 * K01 / width, (-2.0 * K02 + width) / width, 0.0],
        [0.0, 2.0 * K11 / height, (2.0 * K12 - height) / height, 0.0],
        [0.0, 0.0, q, qn],
        [0.0, 0.0, -1.0, 0.0]]).T


def projection_pixel_3xl(width, height, near=0.1, far=1000.0):
    return projection_matrix_from_intrinsic_julian(camera_matrix=PIXEL_3_XL_CAMERA_MATRIX,
                                                   near=near,
                                                   far=far,
                                                   width=width,
                                                   height=height)
