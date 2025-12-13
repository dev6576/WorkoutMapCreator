import math
from typing import List, Tuple

LatLng = Tuple[float, float]


def hausdorff_lite(a: List[LatLng], b: List[LatLng]) -> float:
    """
    Lower distance = better match.
    """
    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    total = 0.0
    for p in a:
        total += min(dist(p, q) for q in b)

    return total / max(len(a), 1)
