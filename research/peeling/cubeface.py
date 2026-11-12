"""Face area of the regular octahedral hull |p - c|_1 <= R (c = cube centre (0,0,0) or vertex (1,1,1))."""
import itertools


def face_area(R, vertex=False):
    c = (1, 1, 1) if vertex else (0, 0, 0)
    n = 0
    for x in range(c[0], c[0] + R + 1):
        for y in range(c[1], c[1] + R + 1):
            z = R + c[0] + c[1] + c[2] - x - y
            p = (x, y, z)
            if z < c[2] or sum(v % 2 for v in p) != 1:
                continue
            n += 1
    return n


if __name__ == '__main__':
    print([(R, face_area(R)) for R in range(21, 44, 2)])
    print([(R, face_area(R, True)) for R in range(22, 44, 2)])
