from typing import List, Tuple, Dict

LatLng = Tuple[float, float]


def encode_polyline(points: List[LatLng]) -> str:
    """
    Encodes a polyline using Google's polyline encoding algorithm.
    Compatible with Google Maps, Strava, Garmin, etc.
    """
    result = []
    prev_lat = 0
    prev_lng = 0

    for lat, lng in points:
        lat_i = int(round(lat * 1e5))
        lng_i = int(round(lng * 1e5))

        d_lat = lat_i - prev_lat
        d_lng = lng_i - prev_lng

        result.append(_encode_value(d_lat))
        result.append(_encode_value(d_lng))

        prev_lat = lat_i
        prev_lng = lng_i

    return "".join(result)


def _encode_value(value: int) -> str:
    value = value << 1
    if value < 0:
        value = ~value

    encoded = ""
    while value >= 0x20:
        encoded += chr((0x20 | (value & 0x1F)) + 63)
        value >>= 5

    encoded += chr(value + 63)
    return encoded

def tuples_to_latlng(
    polyline: List[Tuple[float, float]]
) -> List[Dict[str, float]]:
    return [{"lat": lat, "lng": lng} for lat, lng in polyline]