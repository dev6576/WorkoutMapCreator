from typing import List, Tuple
import math

LatLng = Tuple[float, float]


def anchor_bonus(
    road_polyline: List[LatLng],
    anchors: List[LatLng],
    radius_meters: float = 30.0
) -> float:
    """
    Adds bonus if anchor points lie near the candidate polyline.
    """
    bonus = 0.0

    for anchor in anchors:
        if _point_near_polyline(anchor, road_polyline, radius_meters):
            bonus += 10.0

    return bonus


def _point_near_polyline(point, polyline, radius):
    for p in polyline:
        if _haversine(point, p) <= radius:
            return True
    return False


def _haversine(p1, p2):
    # meters
    R = 6371000
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    return 2 * R * math.asin(math.sqrt(a))
