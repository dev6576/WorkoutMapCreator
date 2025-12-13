from pydantic import BaseModel

class UploadResponse(BaseModel):
    route_id: str
    status: str
