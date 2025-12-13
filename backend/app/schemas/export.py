from pydantic import BaseModel
from typing import Optional

class ExportRouteResponse(BaseModel):
    type: str
    url: Optional[str] = None
    download_url: Optional[str] = None
