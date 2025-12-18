import cv2
import numpy as np
from typing import List

from .models import RouteComponent, CVExtractionResult
from .utils import (
    extract_centerline,
    order_points_nearest_neighbor,
    compute_polyline_length,
)
from app.print_logging import log


class RouteCVExtractor:
    def __init__(self, config=None, debug: bool = False, debug_dir: str | None = None):
        self.config = config or {}
        self.debug = debug
        self.debug_dir = debug_dir

    # ------------------------------------------------------------------
    # Public entry
    # ------------------------------------------------------------------

    def extract(self, image_path: str) -> CVExtractionResult:
        log(f"[CV] extract start: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image path")

        h, w = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 1. Color segmentation
        mask = self._segment_route(hsv)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/01_mask.png", mask)

        # 2. Cleanup
        mask = self._cleanup(mask)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/02_cleaned.png", mask)

        # 3. Centerline extraction (KEY CHANGE)
        centerline = extract_centerline(mask)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/03_centerline.png", centerline)

        ys, xs = np.where(centerline > 0)
        points = list(zip(xs.tolist(), ys.tolist()))

        if len(points) < 20:
            log("[CV] centerline too small")
            return self._empty_result(w, h)

        # 4. Order into polyline
        ordered = order_points_nearest_neighbor(points)
        length = compute_polyline_length(ordered)

        component = RouteComponent(
            id=1,
            pixel_polyline=ordered,
            pixel_length=length,
            endpoints=[ordered[0], ordered[-1]],
            loops=False,
            avg_width=3.0,
            width_std=0.5,
            curvature=0.0,
            self_intersections=0,
            color_profile={},
            dominant_color="red",
            is_closed_shape=False,
            is_candidate_route=True,
            bounding_box=(
                min(xs), min(ys), max(xs), max(ys)
            ),
        )

        # Debug overlay
        if self.debug:
            vis = img.copy()
            for x, y in ordered:
                cv2.circle(vis, (x, y), 1, (0, 255, 0), -1)
            cv2.imwrite(f"{self.debug_dir}/04_polyline.png", vis)

        log(f"[CV] extracted route points={len(ordered)} length={length:.1f}")

        return CVExtractionResult(
            image_width=w,
            image_height=h,
            components=[component],
            primary_candidate_id=1,
            confidence=1.0,
            debug_artifacts={},
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _segment_route(self, hsv):
        blue = cv2.inRange(hsv, (90, 50, 50), (130, 255, 255))
        red1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        return cv2.bitwise_or(blue, red1 | red2)

    def _cleanup(self, mask):
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

    def _empty_result(self, w, h):
        return CVExtractionResult(
            image_width=w,
            image_height=h,
            components=[],
            primary_candidate_id=None,
            confidence=0.0,
            debug_artifacts={},
        )
