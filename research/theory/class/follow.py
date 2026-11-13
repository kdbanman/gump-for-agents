"""follow.py -- follow-up measurements after the scans (job lists by name; each line is printed and saved).

    python3 follow.py stage4 | weak | gump3 | hulls2d | hulls3d
"""
import sys
import run as RN, theory as TH, lattices as LT


def cap(lat, b, c):
    return TH.capped(b, c, LT.get(lat).K)


def faces(lat, b, c, m, ns, sec, u=None, p=None):
    B, S = cap(lat, b, c)
    for n in ns:
        RN.face(lat, B, S, m, n, sec=sec, u=u, p=p)
        sys.stdout.flush()


def hulls(lat, b, c, Rs, T=200000, p=None):
    B, S = cap(lat, b, c)
    for R in Rs:
        RN.life(lat, B, S, R, T=T, p=p)
        sys.stdout.flush()


if __name__ == "__main__":
    job = sys.argv[1]
    if job == "stage4":
        faces("cross3", 4, 7, 16, [20, 28, 40, 56, 80], 10, p=0.45)
        faces("cross3", 4, 8, 16, [12, 20, 28, 40, 56], 10, p=0.5)
        for c, p in ((7, 0.33), (8, 0.40), (9, 0.44), (10, 0.48), (11, 0.52)):
            faces("cross4", 5, c, 20, [28, 48, 80, 128], 10, p=p)
    elif job == "weak":
        faces("moore", 4, 7, 32, [120, 160, 240, 320], 25, u=(0, 1), p=0.6)
        faces("cross3", 4, 6, 24, [160, 240], 25, p=0.4)
    elif job == "gump3":
        for c, p in ((6, 0.42), (7, 0.48), (8, 0.55)):
            faces("gump", 4, c, 8, [[3, 4], [4, 4], [4, 5], [5, 5]], 30 if c < 8 else 30, p=p)
    elif job == "hulls2d":
        hulls("cross2", 3, 5, [5, 6, 7, 8, 9, 10], p=0.5)
        hulls("cross3", 4, 9, [5, 6, 7, 8, 9], p=0.55)
        hulls("cross3", 4, 6, [8, 12, 16, 20], p=0.4)
        hulls("cross4", 5, 12, [6, 8, 10, 12], p=0.57)
        hulls("moore", 4, 7, [6, 10, 14, 18, 24], p=0.6)
    elif job == "vn":
        faces("vn", 2, 3, 16, [12, 20, 28, 36, 48, 64, 80], 12, p=0.47)
        faces("vn", 2, 3, 32, [48, 80], 12, p=0.47)
        hulls("vn", 2, 3, [4, 6, 8, 10, 12, 14, 16], p=0.47)
        faces("hex12", 6, 11, 16, [40, 64, 96], 10, p=0.62)
        faces("tri18", 8, 15, 16, [40, 64, 96], 10, p=0.58)
    elif job == "more3d":
        faces("fcc", 4, 6, 8, [6, 8], 25, p=0.42)
        faces("fcc", 4, 8, 8, [6, 8], 25, p=0.55)
        faces("bcc8", 3, 5, 8, [6, 7], 40, p=0.5)
        faces("sc6", 2, 3, 8, [6, 7], 40, p=0.4)
        faces("sc6", 2, 4, 8, [6, 7], 40, p=0.52)
    elif job == "hulls3d":
        for lat, b, c, Rs, p in [a.split(":") for a in sys.argv[2:]]:
            hulls(lat, int(b), int(c), [int(x) for x in Rs.split(",")], p=float(p), T=100000)
