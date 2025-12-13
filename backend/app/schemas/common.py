from pydantic import BaseModel

class LatLng(BaseModel):
    lat: float
    lng: float
