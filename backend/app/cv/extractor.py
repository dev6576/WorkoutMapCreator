import cv2
import numpy as np
from typing import List

from .models import RouteComponent, CVExtractionResult
from .utils import (
    skeletonize,
    compute_polyline_length,
    order_skeleton_points,
)
from app.print_logging import log


class RouteCVExtractor:
    def __init__(self, config=None, debug: bool = False, debug_dir: str | None = None):
        self.config = config or {}
        self.debug = debug
        self.debug_dir = debug_dir

    def extract(self, image_path: str) -> CVExtractionResult:
        log(f"[CV] extract start: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image path")

        h, w = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # --- 1. Segment route by color ---
        mask = self._segment_route(hsv)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/01_mask.png", mask)

        # --- 2. Morphological cleanup ---
        mask = self._cleanup(mask)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/02_cleaned.png", mask)

        # Ensure binary + slightly thicken before skeleton
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

        # --- 3. Skeletonize ---
        skel = skeletonize(mask)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/03_skeleton.png", skel)

        log(f"[CV] skeleton pixels: {np.count_nonzero(skel)}")

        # --- 4. Extract connected components ---
        components = self._extract_components(skel)

        # --- 5. Select primary route ---
        primary_id, confidence = self._select_primary(components)

        # --- 6. Debug visualization ---
        if self.debug:
            vis = img.copy()
            for c in components:
                color = (0, 255, 0) if c.id == primary_id else (0, 0, 255)
                for x, y in c.pixel_polyline:
                    cv2.circle(vis, (x, y), 1, color, -1)
            cv2.imwrite(f"{self.debug_dir}/04_components.png", vis)

        return CVExtractionResult(
            image_width=w,
            image_height=h,
            components=components,
            primary_candidate_id=primary_id,
            confidence=confidence,
            debug_artifacts={},
        )

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------

    def _segment_route(self, hsv):
        """
        Color-based segmentation.
        Currently supports blue + red routes.
        """
        blue = cv2.inRange(hsv, (90, 50, 50), (130, 255, 255))
        red1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        return cv2.bitwise_or(blue, red1 | red2)

    def _cleanup(self, mask):
        """
        Removes small holes and noise while preserving route continuity.
        """
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

    def _extract_components(self, skel) -> List[RouteComponent]:
        """
        Converts skeleton into ordered polylines.
        Each connected component becomes one RouteComponent.
        """
        num_labels, labels = cv2.connectedComponents(skel)
        components: List[RouteComponent] = []

        for label in range(1, num_labels):
            ys, xs = np.where(labels == label)

            # Skip tiny noise
            if len(xs) < 50:
                continue

            raw_points = list(zip(xs.tolist(), ys.tolist()))

            # Safety: downsample very large skeletons
            if len(raw_points) > 10000:
                raw_points = raw_points[::2]

            ordered = order_skeleton_points(raw_points)
            if len(ordered) < 20:
                continue

            length = compute_polyline_length(ordered)

            components.append(
                RouteComponent(
                    id=label,
                    pixel_polyline=ordered,
                    pixel_length=length,
                    endpoints=[ordered[0], ordered[-1]],
                    loops=False,
                    avg_width=3.0,
                    width_std=0.5,
                    curvature=0.0,
                    self_intersections=0,
                    color_profile={},
                    dominant_color="unknown",
                    is_closed_shape=False,
                    is_candidate_route=False,
                    bounding_box=(
                        min(xs),
                        min(ys),
                        max(xs),
                        max(ys),
                    ),
                )
            )

        log(f"[CV] extracted {len(components)} components")
        return components

    def _select_primary(self, components):
        """
        Selects the longest polyline as the main route.
        """
        if not components:
            return None, 0.0

        lengths = np.array([c.pixel_length for c in components])
        idx = int(np.argmax(lengths))

        components[idx].is_candidate_route = True
        confidence = float(lengths[idx] / max(np.sum(lengths), 1))

        log(
            f"[CV] primary route selected: "
            f"points={len(components[idx].pixel_polyline)} "
            f"confidence={confidence:.2f}"
        )

        return components[idx].id, confidence
