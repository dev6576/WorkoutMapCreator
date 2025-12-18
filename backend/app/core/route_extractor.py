from typing import List, Tuple
from pathlib import Path
from app.cv.extractor import RouteCVExtractor
from app.print_logging import log


def extract_image_space_polyline(image_path: str) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    """
    Returns:
      - ordered pixel polyline [(x, y), ...]
      - image_size (width, height)
    """
    log("extract_image_space_polyline called")
    debug_dir = Path(image_path).parent / "debug"
    debug_dir.mkdir(exist_ok=True)

    extractor = RouteCVExtractor(
        debug=True,
        debug_dir=str(debug_dir)
    )
    result = extractor.extract(image_path)

    if result.primary_candidate_id is None:
        raise ValueError("No valid route detected in image")

    primary = next(
        (c for c in result.components
        if c.id == result.primary_candidate_id),
        None
    )

    if primary is None:
        raise ValueError("No valid route extracted from image")


    log(
        f"Primary route selected: "
        f"points={len(primary.pixel_polyline)} "
        f"confidence={result.confidence:.2f}"
    )

    return primary.pixel_polyline, (result.image_width, result.image_height)
