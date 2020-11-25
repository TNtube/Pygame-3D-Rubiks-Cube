from math import cos, sin
import numpy as np


def average_z(dots: tuple[tuple]):
    return sum(dot[2] for dot in dots)/len(dots)


def rot_matrix(a: int, b: int, t: int):
    sa, ca = sin(a), cos(a)
    sb, cb = sin(b), cos(b)
    st, ct = sin(t), cos(t)
    r_x = [[1, 0, 0],
           [0, ca, -sa],
           [0, sa, ca]]

    r_y = [[cb, 0, sb],
           [0, 1, 0],
           [-sb, 0, cb]]

    r_z = [[ct, -st, 0],
           [st, ct, 0],
           [0, 0, 1]]

    return np.dot(r_z, np.dot(r_y, r_x))


def fit_point(vec: tuple[int, int], shape):
    return [round(shape.movement[2] / 2 * coordinate + frame / 2)
            for coordinate, frame in zip(vec, shape.movement[:2])]
