import cv2
import numpy as np
from typing import List
from .models import RouteComponent, CVExtractionResult
from .utils import skeletonize, compute_polyline_length, order_skeleton_points
from app.print_logging import log


class RouteCVExtractor:
    def __init__(self, config: dict | None = None, debug: bool = False, debug_dir: str | None = None):
        self.config = config or {}
        self.debug = debug
        self.debug_dir = debug_dir

    def _draw_components(self, img, components, primary_id=None):
        vis = img.copy()
        for c in components:
            color = (0, 255, 0) if c.id == primary_id else (0, 0, 255)
            for x, y in c.pixel_polyline:
                cv2.circle(vis, (x, y), 1, color, -1)
        return vis

    def extract(self, image_path: str) -> CVExtractionResult:
        log(f"CV extract start: {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image")

        h, w = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = self._segment_route(hsv)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/01_mask.png", mask)

        mask = self._cleanup(mask)
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/02_cleaned.png", mask)

        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

        skel = skeletonize(mask.copy())
        if self.debug:
            cv2.imwrite(f"{self.debug_dir}/03_skeleton.png", skel * 255)

        components = self._extract_components(skel)

        primary_id, confidence = self._select_primary(components)
        if self.debug:
            comp_img = self._draw_components(img, components, primary_id)
            cv2.imwrite(f"{self.debug_dir}/04_components.png", comp_img)
        return CVExtractionResult(
            image_width=w,
            image_height=h,
            components=components,
            primary_candidate_id=primary_id,
            confidence=confidence,
            debug_artifacts={}
        )

    def _segment_route(self, hsv):
        blue = cv2.inRange(hsv, (90, 50, 50), (130, 255, 255))
        red1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        return cv2.bitwise_or(blue, red1 | red2)

    def _cleanup(self, mask):
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, 2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, 1)
        return mask

    def _extract_components(self, skel) -> List[RouteComponent]:
        num_labels, labels = cv2.connectedComponents(skel)
        components = []

        for label in range(1, num_labels):
            ys, xs = np.where(labels == label)
            raw = list(zip(xs.tolist(), ys.tolist()))
            if len(raw) < 20:
                continue

            points = order_skeleton_points(raw)
            length = compute_polyline_length(points)
            endpoints = self._find_endpoints(points)
            loops = len(endpoints) == 0

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
                    bounding_box=(
                        min(xs), min(ys), max(xs), max(ys)
                    )
                )
            )

        return components

    def _find_endpoints(self, points):
        s = set(points)
        return [
            p for p in points
            if sum(
                (p[0] + dx, p[1] + dy) in s
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                if (dx, dy) != (0, 0)
            ) == 1
        ]

    def _select_primary(self, components):
        if not components:
            return None, 0.0

        scores = []
        for c in components:
            score = int(c.pixel_length > 300) * 2 + int(not c.loops)
            scores.append(score)

        idx = int(np.argmax(scores))
        components[idx].is_candidate_route = True
        confidence = scores[idx] / max(sum(scores), 1)
        return components[idx].id, confidence
