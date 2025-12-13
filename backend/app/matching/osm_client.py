from typing import Dict, List
from .models import RoadSegment
from app.print_logging import log


class OSMClient:
    def get_roads(self, bbox: Dict[str, float]) -> List[RoadSegment]:
        """
        Stub for OSM/Overpass integration.

        bbox = {
            north, south, east, west
        }
        """
        log(f"OSMClient.get_roads called bbox={bbox}")
        # TODO: Implement Overpass API call
        return []
