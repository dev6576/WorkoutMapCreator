import cv2
import numpy as np
from math import hypot
from collections import deque


# ---------------------------------------------------------------------
# Centerline extraction via distance transform
# ---------------------------------------------------------------------

def extract_centerline(mask: np.ndarray, ridge_frac: float = 0.5) -> np.ndarray:
    """
    Extracts a 1px-wide centerline from a thick route mask
    using distance transform ridge detection.

    Input: binary mask {0,255}
    Output: binary centerline {0,255}
    """
    # Ensure binary
    mask = (mask > 0).astype(np.uint8) * 255

    # Distance to nearest background
    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)

    # Ridge = pixels near max distance (center of route)
    thresh = ridge_frac * dist.max()
    ridge = np.zeros_like(mask)
    ridge[dist >= thresh] = 255

    # Thin ridge to single pixel
    ridge = cv2.ximgproc.thinning(ridge)

    return ridge


# ---------------------------------------------------------------------
# Polyline ordering
# ---------------------------------------------------------------------

def order_points_nearest_neighbor(points):
    """
    Orders points into a single polyline using greedy nearest-neighbor.
    Deterministic and fast for thin centerlines.
    """
    if len(points) < 2:
        return points

    pts = points.copy()
    ordered = [pts.pop(0)]

    while pts:
        last = ordered[-1]
        idx = min(
            range(len(pts)),
            key=lambda i: hypot(pts[i][0] - last[0], pts[i][1] - last[1]),
        )
        ordered.append(pts.pop(idx))

    return ordered


# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------

def compute_polyline_length(points):
    return sum(
        hypot(points[i + 1][0] - points[i][0],
              points[i + 1][1] - points[i][1])
        for i in range(len(points) - 1)
    )
