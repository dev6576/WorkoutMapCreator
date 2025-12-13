import numpy as np
import cv2

def skeletonize(binary_img: np.ndarray) -> np.ndarray:
    """
    Zhang-Suen thinning using OpenCV ximgproc if available.
    """
    if hasattr(cv2, "ximgproc"):
        return cv2.ximgproc.thinning(binary_img)
    raise RuntimeError("OpenCV ximgproc not available")


def compute_polyline_length(points):
    length = 0.0
    for i in range(1, len(points)):
        p1, p2 = points[i - 1], points[i]
        length += ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    return length
