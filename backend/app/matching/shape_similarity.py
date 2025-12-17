import numpy as np


def hausdorff(a, b):
    def dist(p, q):
        return np.linalg.norm(np.array(p) - np.array(q))

    def h(A, B):
        return max(min(dist(a, b) for b in B) for a in A)

    return max(h(a, b), h(b, a))
