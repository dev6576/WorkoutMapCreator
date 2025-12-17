from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class MapMatchCandidate:
    osm_way_id: int
    geo_polyline: List[Tuple[float, float]]
    score: float
