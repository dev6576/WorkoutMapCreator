from pydantic import BaseModel
from typing import List, Optional
from app.schemas.common import LatLng

class Polyline(BaseModel):
    geo: List[LatLng]
    encoded: Optional[str] = None


class ImageSpacePolyline(BaseModel):
    points: List[List[int]]  # [[x, y], ...]


class RoutePreviewResponse(BaseModel):
    route_id: str
    confidence: float
    polyline: Polyline
    polyline_image_space: ImageSpacePolyline
