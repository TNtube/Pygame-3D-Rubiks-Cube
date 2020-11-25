from math import cos, sin


def average_z(dots):
    return sum(dot[2] for dot in dots)/len(dots)


def rot_matrix(a, b, t):
    sa, ca = sin(a), cos(a)
    sb, cb = sin(b), cos(b)
    st, ct = sin(t), cos(t)
    return (
        (cb * ct, -cb * st, sb),
        (ca * st + sa * sb * ct, ca * ct - st * sa * sb, -cb * sa),
        (st * sa - ca * sb * ct, ca * st * sb + sa * ct, ca * cb)
    )


def fit_point(vec, shape):
    return [round(shape.movement[2] / 2 * coordinate + frame / 2)
            for coordinate, frame in zip(vec, shape.movement[:-1])]
