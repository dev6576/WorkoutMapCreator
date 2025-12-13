from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

Pixel = Tuple[int, int]

@dataclass
class RouteComponent:
    id: int
    pixel_polyline: List[Pixel]

    pixel_length: float
    endpoints: List[Pixel]
    loops: bool

    avg_width: float
    width_std: float

    curvature: float
    self_intersections: int

    color_profile: Dict[str, float]
    dominant_color: str

    is_closed_shape: bool
    is_candidate_route: bool

    bounding_box: Tuple[int, int, int, int]


@dataclass
class CVExtractionResult:
    image_width: int
    image_height: int

    components: List[RouteComponent]
    primary_candidate_id: Optional[int]
    confidence: float

    debug_artifacts: Dict[str, str]
