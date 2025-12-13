from pydantic import BaseModel
from typing import Optional

class BoundingBox(BaseModel):
    north: float
    south: float
    east: float
    west: float


class SearchScope(BaseModel):
    bbox: BoundingBox
    padding_meters: int = 0


class Assumptions(BaseModel):
    route_type: str = "running"
    prefer_roads: bool = True


class ProcessRouteRequest(BaseModel):
    search_scope: Optional[SearchScope] = None
    assumptions: Optional[Assumptions] = None


class ProcessRouteResponse(BaseModel):
    route_id: str
    job_id: str
    status: str
