import requests


OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def query_roads(bbox):
    query = f"""
    [out:json];
    way["highway"]({bbox});
    out geom;
    """
    res = requests.post(OVERPASS_URL, data=query)
    return res.json()
