from pydantic import BaseModel
from typing import Optional

class RouteStatusResponse(BaseModel):
    route_id: str
    status: str
    progress: Optional[float] = None
    message: Optional[str] = None
