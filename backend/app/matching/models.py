from dataclasses import dataclass
from typing import List, Tuple, Dict

LatLng = Tuple[float, float]


@dataclass
class RoadSegment:
    id: str
    geometry: List[LatLng]
    name: str | None = None


@dataclass
class MapMatchCandidate:
    candidate_id: str
    polyline: List[LatLng]
    score: float
    breakdown: Dict[str, float]
    metadata: Dict
