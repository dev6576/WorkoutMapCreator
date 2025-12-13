from typing import List, Tuple
import math

LatLng = Tuple[float, float]


def project_markers_onto_path(
    markers: List[Tuple[int, int]],
    marker_values: List[int],
    geo_path: List[LatLng]
) -> List[Tuple[int, float]]:
    """
    Projects markers onto path and returns (marker_value, path_distance).
    """
    projections = []

    for (lat, lon), value in zip(markers, marker_values):
        dist = _closest_distance_along_path((lat, lon), geo_path)
        projections.append((value, dist))

    return projections


def _closest_distance_along_path(point, path):
    cumulative = 0.0
    best = float("inf")
    traveled = 0.0

    for i in range(len(path) - 1):
        p1, p2 = path[i], path[i + 1]
        seg_len = _dist(p1, p2)

        d = _point_to_segment_dist(point, p1, p2)
        if d < best:
            best = d
            traveled = cumulative

        cumulative += seg_len

    return traveled


def _point_to_segment_dist(p, a, b):
    # Euclidean approximation (sufficient locally)
    ax, ay = a
    bx, by = b
    px, py = p

    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return math.hypot(px - ax, py - ay)

    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)))
    proj = (ax + t * dx, ay + t * dy)
    return math.hypot(px - proj[0], py - proj[1])


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
