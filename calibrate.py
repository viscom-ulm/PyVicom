#!/usr/bin/env python

'''
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images
usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]
default values:
    --debug:    ./output/
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

# Python 2/3 compatibility
from __future__ import print_function
import os
import numpy as np
import cv2 as cv
import time
import math

# built-in modules
import os

if __name__ == '__main__':
    cap = cv.VideoCapture('')
    img_names = []
    count = 0
    while cap.isOpened():
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret:
            count += 1
            if count % 10 == 0:
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                img_names.append(img)
        else:
            break
    img_names = [cv.imread(os.path.join('media/calibration',path), cv.IMREAD_GRAYSCALE) for path in os.listdir('media/calibration')]
    print(len(img_names))
    square_size = float(1.0)

    pattern_size = (9, 6)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = img_names[0].shape[:2]  # TODO: use imquery call to retrieve results


    def processImage(img):
        assert w == img.shape[1] and h == img.shape[0], ("size: %d x %d ... " % (img.shape[1], img.shape[0]))
        found, corners = cv.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.1)
            cv.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if not found:
            print('chessboard not found')
            return None

        return corners.reshape(-1, 2), pattern_points


    threads_num = int(4)
    if threads_num <= 1:
        chessboards = [processImage(fn) for fn in img_names]
    else:
        print("Run with %d threads..." % threads_num)
        from multiprocessing.dummy import Pool as ThreadPool

        pool = ThreadPool(threads_num)
        chessboards = pool.map(processImage, img_names)

    chessboards = [x for x in chessboards if x is not None]
    for (corners, pattern_points) in chessboards:
        img_points.append(corners)
        obj_points.append(pattern_points)
    print("starting calibration using {} images".format(len(img_points)))
    # calculate camera distortion
    start = time.time()
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, (w, h), None, None)
    print("done calibration after {} seconds".format(time.time() - start))

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())

    cv.destroyAllWindows()
