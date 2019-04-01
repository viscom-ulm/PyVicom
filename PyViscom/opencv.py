import cv2
import glfw
import pyrr
import numpy as np
from PyViscom.Shader import Shader
from PyViscom.Texture import Texture
from OpenGL.GL import *
from PyViscom.Util import (projection_matrix_from_intrinsic_julian, PIXEL_3_XL_CAMERA_MATRIX,
                           PIXEL_3_XL_CAMERA_MATRIX_STILL,
                           PIXEL_3_XL_DISTORTION_COEFFICIENTS, PIXEL_3_XL_DISTORTION_COEFFICIENTS_STILL,
                           projection_pixel_3xl,
                           view_matrix_from_rvec_tvec)


class Quad:
    def __init__(self, width=1.0, height=1.0, center=True):
        pattern_width = 16.2
        pattern_height = 11.3
        # prepare buffer
        if center:
            self.vertices = np.array([
                -width, height, 0.0, 0.0, 1.0,
                -width, -height, 0.0, 0.0, 0.0,
                width, height, 0.0, 1.0, 1.0,
                width, -height, 0.0, 1.0, 0.0
            ], dtype=np.float32)
        else:
            self.vertices = np.array([
                0, 0, 0.0, 0.0, 0.0,
                width, 0, 0.0, 1.0, 0.0,
                0, height, 0.0, 0.0, 1.0,
                width, height, 0.0, 1.0, 1.0
            ], dtype=np.float32)
        self.shapeVAO = glGenVertexArrays(1)
        self.shapeVBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.shapeVBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.itemsize * len(self.vertices), self.vertices, GL_STATIC_DRAW)
        glBindVertexArray(self.shapeVAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(12))
        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.shapeVAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
    return img


def main():
    width = 1920
    height = 1080
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(width, height, "OpenCV", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    fullscreen_quad = Quad()
    quad = Quad(width=8, height=5, center=False)
    fullscreen_shader = Shader()
    fullscreen_shader.set_shader(vert='canvas.vert', frag='canvas.frag')
    quad_shader = Shader()
    quad_shader.set_shader(vert='quad.vert', frag='quad.frag')
    fullscreen_texture = Texture()
    quad_texture = Texture()
    quad_texture.set_texture('D:/Documents/projects/PyTools/PyTools/inner_chessboard.jpg')

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
    axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

    objp = np.array([
        objp[0],
        objp[8],
        objp[45],
        objp[53]
    ])

    cap = cv2.VideoCapture('D:/Documents/projects/PyTools/PyTools/chessboard2.mp4')

    projection = projection_matrix_from_intrinsic_julian(camera_matrix=PIXEL_3_XL_CAMERA_MATRIX, near=0.1,
                                                         far=1000.0, width=width, height=height)

    view = pyrr.matrix44.create_look_at(eye=np.array([0, 0, 50]), target=np.array([0, 0, 0]), up=np.array([0, 1, 0]))
    model = pyrr.matrix44.create_identity()
    i = 0
    while cap.isOpened():
        # Capture frame-by-frame
        ret, img = cap.read()
        cv2.imwrite('frames/img{}.jpg'.format(i), img)
        i += 1
        if ret:
            # cv2.imwrite("img.jpg", img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
            corners = np.array([
                corners[0],
                corners[8],
                corners[45],
                corners[53]
            ])
            if ret:
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                # Find the rotation and translation vectors.
                ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, PIXEL_3_XL_CAMERA_MATRIX, None)
                # convert rvecs and tvecs
                if ret:
                    view = view_matrix_from_rvec_tvec(rvec=rvecs, tvec=tvecs)
                    # project 3D points to image plane
                    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, PIXEL_3_XL_CAMERA_MATRIX, None)
                    img = draw(img, corners2, imgpts)
            cv2.flip(img, 0, img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.true_divide(img, 255.0)

            # fullscreen
            fullscreen_texture.set_texture_from_buffer(img)
            fullscreen_shader.use_shader()
            glActiveTexture(GL_TEXTURE0)
            fullscreen_texture.use_texture()
            glUniform1i(glGetUniformLocation(fullscreen_shader.programId, "draw_texture"), 0)
            fullscreen_quad.draw()

            # quad
            quad_shader.use_shader()
            glActiveTexture(GL_TEXTURE0)
            quad_texture.use_texture()

            glUniform1i(glGetUniformLocation(quad_shader.programId, "draw_texture"), 0)
            glUniformMatrix4fv(glGetUniformLocation(quad_shader.programId, "P"), 1, GL_FALSE, projection)
            glUniformMatrix4fv(glGetUniformLocation(quad_shader.programId, "V"), 1, GL_FALSE, view)
            glUniformMatrix4fv(glGetUniformLocation(quad_shader.programId, "M"), 1, GL_FALSE, model)
            quad.draw()

            # Swap front and back buffers
            glfw.swap_buffers(window)

            # Poll for and process events
            glfw.poll_events()
        else:
            break
    cv2.destroyAllWindows()


def main2():
    img = cv2.imread('img.jpg', cv2.IMREAD_COLOR)
    # cv2.imwrite("img.jpg", img)
    img = cv2.resize(img, (2305, 1297))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (height, width, channels) = img.shape

    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(width, height, "OpenCV", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    fullscreen_quad = Quad()
    quad = Quad(width=8, height=5, center=False)
    fullscreen_shader = Shader()
    fullscreen_shader.set_shader(vert='canvas.vert', frag='canvas.frag')
    quad_shader = Shader()
    quad_shader.set_shader(vert='quad.vert', frag='quad.frag')
    fullscreen_texture = Texture()
    quad_texture = Texture()
    quad_texture.set_texture('D:/Documents/projects/PyTools/PyTools/inner_chessboard.jpg')

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
    axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

    objp = np.array([
        objp[0],
        objp[8],
        objp[45],
        objp[53]
    ])

    projection = projection_pixel_3xl(width, height)
    view = pyrr.matrix44.create_look_at(np.array([-20,0,-10]), np.array([0,0,0]), np.array([0,1,0]))
    model = pyrr.matrix44.create_identity()

    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
    corners = np.array([
        corners[0],
        corners[8],
        corners[45],
        corners[53]
    ])
    if ret:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # Find the rotation and translation vectors.
        ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, PIXEL_3_XL_CAMERA_MATRIX, None)
        # convert rvecs and tvecs
        if ret:
            #view = view_matrix_from_rvec_tvec(rvec=rvecs, tvec=tvecs)
            print(projection)
            print(view)
            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, PIXEL_3_XL_CAMERA_MATRIX, None)
            img = draw(img, corners2, imgpts)
    cv2.flip(img, 0, img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.true_divide(img, 255.0)

    while not glfw.window_should_close(window):
        # fullscreen
        fullscreen_texture.set_texture_from_buffer(img)
        fullscreen_shader.use_shader()
        glActiveTexture(GL_TEXTURE0)
        fullscreen_texture.use_texture()
        glUniform1i(glGetUniformLocation(fullscreen_shader.programId, "draw_texture"), 0)
        fullscreen_quad.draw()

        # quad
        quad_shader.use_shader()
        glActiveTexture(GL_TEXTURE0)
        quad_texture.use_texture()

        glUniform1i(glGetUniformLocation(quad_shader.programId, "draw_texture"), 0)
        glUniformMatrix4fv(glGetUniformLocation(quad_shader.programId, "P"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(quad_shader.programId, "V"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(quad_shader.programId, "M"), 1, GL_FALSE, model)
        quad.draw()

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    main()
