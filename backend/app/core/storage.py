import uuid
from typing import Dict, Any

ROUTES: Dict[str, Dict[str, Any]] = {}
JOBS: Dict[str, Dict[str, Any]] = {}


def create_route() -> str:
    route_id = f"rt_{uuid.uuid4().hex[:8]}"
    ROUTES[route_id] = {
        "status": "uploaded",
        "image_path": None,
        "polyline": None,
        "confidence": None,
        "search_scope": None
    }
    return route_id


def create_job(route_id: str) -> str:
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    JOBS[job_id] = {
        "route_id": route_id,
        "status": "processing",
        "progress": 0.0
    }
    return job_id
