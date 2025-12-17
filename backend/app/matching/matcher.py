from .models import MapMatchCandidate
from .shape_similarity import hausdorff
from .scoring import score_candidate


def match_route(geo_polyline, osm_ways):
    candidates = []

    for way in osm_ways:
        road = [(n["lat"], n["lon"]) for n in way["geometry"]]
        shape = hausdorff(geo_polyline, road)
        score = score_candidate(abs(len(geo_polyline) - len(road)), shape, 0)
        candidates.append(
            MapMatchCandidate(
                osm_way_id=way["id"],
                geo_polyline=road,
                score=score
            )
        )

    return sorted(candidates, key=lambda c: c.score, reverse=True)
