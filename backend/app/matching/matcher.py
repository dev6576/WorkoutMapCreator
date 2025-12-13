from typing import List, Tuple, Dict, Optional
from .models import MapMatchCandidate
from .pixel_to_geo import pixel_polyline_to_geo
from .scoring import score_candidate
from .osm_client import OSMClient
from app.print_logging import log


class MapMatcher:
    def __init__(self, osm_client: OSMClient):
        self.osm = osm_client

    def match(
        self,
        pixel_polyline: List[Tuple[int, int]],
        image_size: Tuple[int, int],
        geo_bbox: Dict[str, float],
        anchor_points: Optional[List[Tuple[float, float]]] = None,
        marker_points: Optional[List[Tuple[float, float]]] = None,
        marker_values: Optional[List[int]] = None
    ) -> List[MapMatchCandidate]:

        log(f"MapMatcher.match called points={len(pixel_polyline)} bbox={geo_bbox}")
        geo_polyline = pixel_polyline_to_geo(
            pixel_polyline,
            image_size,
            geo_bbox
        )

        roads = self.osm.get_roads(geo_bbox)
        log(f"MapMatcher: retrieved {len(roads)} roads from OSMClient")
        candidates = []

        for road in roads:
            breakdown = score_candidate(
                geo_polyline,
                road.geometry,
                anchor_points,
                marker_points,
                marker_values
            )

            candidates.append(
                MapMatchCandidate(
                    candidate_id=road.id,
                    polyline=road.geometry,
                    score=breakdown["total"],
                    breakdown=breakdown,
                    metadata={"name": road.name}
                )
            )

        return sorted(candidates, key=lambda c: c.score, reverse=True)
