from typing import Dict, List, Tuple
from .shape_similarity import hausdorff_lite
from .anchors import anchor_bonus
from .marker_projection import project_markers_onto_path

LatLng = Tuple[float, float]


def score_candidate(
    geo_polyline: List[LatLng],
    road_polyline: List[LatLng],
    anchors: List[LatLng] | None = None,
    marker_points: List[LatLng] | None = None,
    marker_values: List[int] | None = None
) -> Dict[str, float]:

    breakdown = {}

    shape_dist = hausdorff_lite(geo_polyline, road_polyline)
    breakdown["shape_similarity"] = -shape_dist

    anchor_score = 0.0
    if anchors:
        anchor_score = anchor_bonus(road_polyline, anchors)
    breakdown["anchor_bonus"] = anchor_score

    marker_score = 0.0
    if marker_points and marker_values:
        marker_score = _marker_order_score(
            marker_points,
            marker_values,
            road_polyline
        )

    breakdown["marker_order"] = marker_score
    breakdown["total"] = breakdown["shape_similarity"] + anchor_score + marker_score
    return breakdown


def _marker_order_score(
    marker_points: List[LatLng],
    marker_values: List[int],
    road_polyline: List[LatLng]
) -> float:
    """
    Rewards monotonic increase of marker values along path.
    """
    projections = project_markers_onto_path(
        marker_points,
        marker_values,
        road_polyline
    )

    projections.sort(key=lambda x: x[1])  # path distance order
    values = [v for v, _ in projections]

    score = 0.0
    for i in range(1, len(values)):
        if values[i] > values[i - 1]:
            score += 5.0
        else:
            score -= 5.0

    return score
