import cv2
import numpy as np
from math import hypot


def skeletonize(mask: np.ndarray) -> np.ndarray:
    """
    Morphological skeletonization.
    Input must be binary {0,255}.
    Output is binary {0,255}.
    """
    mask = mask.copy()
    skel = np.zeros(mask.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    while True:
        eroded = cv2.erode(mask, element)
        opened = cv2.dilate(eroded, element)
        temp = cv2.subtract(mask, opened)
        skel = cv2.bitwise_or(skel, temp)
        mask = eroded.copy()

        if cv2.countNonZero(mask) == 0:
            break

    return skel


def skeleton_degrees(skel: np.ndarray) -> np.ndarray:
    deg = np.zeros_like(skel, dtype=np.uint8)
    ys, xs = np.where(skel > 0)
    points = set(zip(xs, ys))

    for x, y in points:
        deg[y, x] = sum(
            (x + dx, y + dy) in points
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        )
    return deg


def prune_skeleton(skel: np.ndarray, min_branch_length: int = 20) -> np.ndarray:
    """
    Removes small dangling branches (text, borders, noise).
    """
    deg = skeleton_degrees(skel)
    pruned = skel.copy()

    ys, xs = np.where((deg == 1) & (skel > 0))
    endpoints = list(zip(xs, ys))
    ys, xs = np.where(skel > 0)
    points = set(zip(xs, ys))

    for ep in endpoints:
        path = [ep]
        cur = ep
        prev = None

        while True:
            x, y = cur
            neighbors = [
                (x + dx, y + dy)
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                if (dx, dy) != (0, 0)
                and (x + dx, y + dy) in points
                and (x + dx, y + dy) != prev
            ]

            if len(neighbors) != 1:
                break

            prev = cur
            cur = neighbors[0]
            path.append(cur)

            if deg[cur[1], cur[0]] >= 3:
                break

        if len(path) < min_branch_length:
            for x, y in path:
                pruned[y, x] = 0

    return pruned

from collections import deque

def order_skeleton_points(points):
    """
    Orders skeleton pixels by extracting the longest path
    using BFS. Guaranteed to terminate.
    """
    point_set = set(points)

    # Build adjacency
    adj = {p: [] for p in point_set}
    for x, y in point_set:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                q = (x + dx, y + dy)
                if q in point_set:
                    adj[(x, y)].append(q)

    # Find endpoints (degree == 1)
    endpoints = [p for p, nbrs in adj.items() if len(nbrs) == 1]

    # If no endpoints (loop), just return sorted
    if len(endpoints) < 2:
        return sorted(points)

    # BFS from one endpoint to find longest path
    start = endpoints[0]
    visited = set([start])
    parent = {start: None}
    queue = deque([start])

    last = start
    while queue:
        cur = queue.popleft()
        last = cur
        for nb in adj[cur]:
            if nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                queue.append(nb)

    # Reconstruct path
    path = []
    cur = last
    while cur:
        path.append(cur)
        cur = parent[cur]

    return path[::-1]


def compute_polyline_length(points):
    return sum(
        hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        for i in range(len(points) - 1)
    )
