from pydantic import BaseModel
from typing import List
from app.schemas.common import LatLng

class RefineRouteRequest(BaseModel):
    anchor_points: List[LatLng]


class RefineRouteResponse(BaseModel):
    status: str
