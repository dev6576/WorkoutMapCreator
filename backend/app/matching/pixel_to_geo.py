from typing import List, Tuple, Dict

LatLng = Tuple[float, float]


def pixel_polyline_to_geo(
    pixel_points: List[Tuple[int, int]],
    image_size: Tuple[int, int],
    bbox: Dict[str, float]
) -> List[LatLng]:
    """
    Affine pixel → geo transform using bounding box.
    """
    img_w, img_h = image_size

    lat_min = bbox["south"]
    lat_max = bbox["north"]
    lon_min = bbox["west"]
    lon_max = bbox["east"]

    geo_points = []

    for x, y in pixel_points:
        lon = lon_min + (x / img_w) * (lon_max - lon_min)
        lat = lat_max - (y / img_h) * (lat_max - lat_min)
        geo_points.append((lat, lon))

    return geo_points
