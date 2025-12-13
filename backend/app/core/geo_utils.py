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
