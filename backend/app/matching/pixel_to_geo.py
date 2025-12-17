from typing import List, Tuple


def pixel_polyline_to_geo(
    pixel_polyline: List[Tuple[int, int]],
    image_size: Tuple[int, int],
    bbox: dict
) -> List[Tuple[float, float]]:
    """
    bbox = {
      min_lon, min_lat, max_lon, max_lat
    }
    """
    img_w, img_h = image_size
    min_lon = bbox["min_lon"]
    min_lat = bbox["min_lat"]
    max_lon = bbox["max_lon"]
    max_lat = bbox["max_lat"]

    geo = []

    for x, y in pixel_polyline:
        lon = min_lon + (x / img_w) * (max_lon - min_lon)
        lat = max_lat - (y / img_h) * (max_lat - min_lat)
        geo.append((lat, lon))

    return geo
