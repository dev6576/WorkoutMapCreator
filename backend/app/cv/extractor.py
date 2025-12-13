import cv2
import numpy as np
from typing import List
from .models import RouteComponent, CVExtractionResult
from .utils import skeletonize, compute_polyline_length
from app.print_logging import log


class RouteCVExtractor:
    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def extract(self, image_path: str) -> CVExtractionResult:
        log(f"RouteCVExtractor.extract called image_path={image_path}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image path")

        h, w = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = self._segment_route(hsv)
        mask = self._cleanup(mask)
        skel = skeletonize(mask)

        components = self._extract_components(skel, mask, img)

        primary_id, confidence = self._select_primary(components)

        return CVExtractionResult(
            image_width=w,
            image_height=h,
            components=components,
            primary_candidate_id=primary_id,
            confidence=confidence,
            debug_artifacts={}
        )

    def _segment_route(self, hsv):
        # Default: blue + red routes (configurable later)
        blue_mask = cv2.inRange(hsv, (90, 50, 50), (130, 255, 255))
        red_mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red_mask2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        return cv2.bitwise_or(blue_mask, red_mask1 | red_mask2)

    def _cleanup(self, mask):
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

    def _extract_components(self, skel, mask, img) -> List[RouteComponent]:
        num_labels, labels = cv2.connectedComponents(skel)
        components = []

        for label in range(1, num_labels):
            ys, xs = np.where(labels == label)
            points = list(zip(xs.tolist(), ys.tolist()))
            if len(points) < 20:
                continue

            length = compute_polyline_length(points)
            endpoints = self._find_endpoints(points)
            loops = len(endpoints) == 0

            bbox = (
                min(xs), min(ys),
                max(xs), max(ys)
            )

            components.append(
                RouteComponent(
                    id=label,
                    pixel_polyline=points,
                    pixel_length=length,
                    endpoints=endpoints,
                    loops=loops,
                    avg_width=3.0,
                    width_std=0.5,
                    curvature=0.0,
                    self_intersections=0,
                    color_profile={},
                    dominant_color="unknown",
                    is_closed_shape=loops,
                    is_candidate_route=False,
                    bounding_box=bbox
                )
            )

        return components

    def _find_endpoints(self, points):
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

        return endpoints

    def _select_primary(self, components):
        if not components:
            return None, 0.0

        scores = []
        for c in components:
            score = 0
            if c.pixel_length > 300:
                score += 2
            if not c.loops:
                score += 1
            scores.append(score)

        max_idx = int(np.argmax(scores))
        components[max_idx].is_candidate_route = True

        confidence = scores[max_idx] / max(sum(scores), 1)
        return components[max_idx].id, confidence
