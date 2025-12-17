from shapely.geometry import box
from shapely.affinity import scale

METERS_PER_DEGREE = 111_320  # approx at equator


def expand_bbox(bbox: dict, padding_meters: int) -> dict:
    if padding_meters <= 0:
        return bbox

    lat_pad = padding_meters / METERS_PER_DEGREE
    lng_pad = padding_meters / METERS_PER_DEGREE

    return {
        "north": bbox["north"] + lat_pad,
        "south": bbox["south"] - lat_pad,
        "east": bbox["east"] + lng_pad,
        "west": bbox["west"] - lng_pad
    }

def normalize_bbox(bbox: dict) -> dict:
    """
    Normalize bbox keys to:
    min_lat, min_lon, max_lat, max_lon
    """
    if "min_lat" in bbox and "min_lon" in bbox:
        return bbox

    # common frontend format
    if {"north", "south", "east", "west"}.issubset(bbox):
        return {
            "min_lat": bbox["south"],
            "max_lat": bbox["north"],
            "min_lon": bbox["west"],
            "max_lon": bbox["east"],
        }

    # lat/lng naming
    if {"min_lat", "max_lat", "min_lng", "max_lng"}.issubset(bbox):
        return {
            "min_lat": bbox["min_lat"],
            "max_lat": bbox["max_lat"],
            "min_lon": bbox["min_lng"],
            "max_lon": bbox["max_lng"],
        }

    raise ValueError(f"Unsupported bbox format: {bbox}")
