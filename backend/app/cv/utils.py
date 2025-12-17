import numpy as np
import cv2
from scipy.spatial import cKDTree
from math import hypot


def skeletonize(mask):
    # Ensure binary uint8
    mask = (mask > 0).astype(np.uint8) * 255

    skel = np.zeros(mask.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    while True:
        eroded = cv2.erode(mask, element)
        opened = cv2.dilate(eroded, element)
        temp = cv2.subtract(mask, opened)
        skel = cv2.bitwise_or(skel, temp)
        mask = eroded

        if cv2.countNonZero(mask) == 0:
            break

    return skel



def compute_polyline_length(points):
    return sum(
        hypot(x2 - x1, y2 - y1)
        for (x1, y1), (x2, y2) in zip(points, points[1:])
    )


def order_skeleton_points(points):
    if len(points) < 2:
        return points

    tree = cKDTree(points)
    point_set = set(points)

    endpoints = []
    for x, y in points:
        neighbors = sum(
            (x + dx, y + dy) in point_set
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        )
        if neighbors == 1:
            endpoints.append((x, y))

    start = endpoints[0] if endpoints else points[0]
    ordered = [start]
    visited = {start}
    current = start

    while True:
        _, idxs = tree.query(current, k=6)
        next_point = None
        for idx in idxs[1:]:
            p = points[idx]
            if p not in visited:
                next_point = p
                break
        if not next_point:
            break
        ordered.append(next_point)
        visited.add(next_point)
        current = next_point

    return ordered
