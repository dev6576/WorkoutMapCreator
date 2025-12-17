from typing import List, Tuple
from PIL import Image

from app.print_logging import log


def extract_image_space_polyline(
    image_path: str
) -> Tuple[List[List[int]], Tuple[int, int]]:
    """
    Extracts a route polyline in IMAGE SPACE (pixel coordinates).

    Returns:
    - polyline: List of [x, y] pixel points
    - image_size: (width, height)
    """

    log(f"extract_image_space_polyline called image_path={image_path}")

    # --- Load image to get dimensions ---
    with Image.open(image_path) as img:
        width, height = img.size

    # --- TEMP CV STUB ---
    # This will later be replaced with:
    # - edge detection
    # - skeletonization
    # - contour tracing
    # - OCR-assisted ordering
    polyline = [
        [int(0.3 * width), int(0.6 * height)],
        [int(0.35 * width), int(0.62 * height)],
        [int(0.45 * width), int(0.7 * height)],
        [int(0.55 * width), int(0.75 * height)],
    ]

    log(f"Extracted {len(polyline)} polyline points")
    log(f"Image size width={width}, height={height}")

    return polyline, (width, height)
