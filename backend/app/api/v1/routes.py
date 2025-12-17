from fastapi import APIRouter, UploadFile, File, HTTPException

from app.print_logging import log

from app.schemas.upload import UploadResponse
from app.schemas.process import ProcessRouteRequest, ProcessRouteResponse
from app.schemas.status import RouteStatusResponse
from app.schemas.route import RoutePreviewResponse, Polyline, ImageSpacePolyline
from app.schemas.refine import RefineRouteRequest, RefineRouteResponse
from app.schemas.common import LatLng

from app.core.storage import ROUTES, JOBS, create_route, create_job
from app.core.image_loader import save_image
from app.core.geo_utils import expand_bbox, normalize_bbox
from app.core.route_extractor import extract_image_space_polyline
from app.matching.pixel_to_geo import pixel_polyline_to_geo
from app.core.polyline_utils import encode_polyline, tuples_to_latlng

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_route_image(file: UploadFile = File(...)):
    log("upload_route_image called")
    route_id = create_route()
    image_path = await save_image(file, route_id)

    ROUTES[route_id]["image_path"] = image_path
    ROUTES[route_id]["status"] = "uploaded"

    return UploadResponse(route_id=route_id, status="uploaded")


@router.post("/{route_id}/process", response_model=ProcessRouteResponse)
async def process_route(route_id: str, payload: ProcessRouteRequest):
    log(f"process_route called route_id={route_id}")
    route = ROUTES.get(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    if not payload.search_scope:
        raise HTTPException(
            status_code=400,
            detail="search_scope (bounding box) is required"
        )

    job_id = create_job(route_id)

    
    raw_bbox = expand_bbox(
        payload.search_scope.bbox.model_dump(),
        payload.search_scope.padding_meters
    )

    expanded_bbox = normalize_bbox(raw_bbox)

    ROUTES[route_id]["search_scope"] = expanded_bbox
    ROUTES[route_id]["status"] = "processing"

    # --- CV PIPELINE ---
    image_polyline, image_size = extract_image_space_polyline(
        route["image_path"]
    )


    geo_polyline_raw = pixel_polyline_to_geo(image_polyline, image_size, expanded_bbox)

    geo_polyline = [LatLng(lat=lat, lng=lng) for lat, lng in geo_polyline_raw]  # Convert tuples to LatLng

    ROUTES[route_id].update({
        "image_polyline": image_polyline,
        "polyline": geo_polyline,
        "encoded_polyline": encode_polyline([(p.lat, p.lng) for p in geo_polyline]),
        "confidence": 0.85,
        "status": "completed"
    })

    JOBS[job_id].update({
        "status": "completed",
        "progress": 1.0
    })

    return ProcessRouteResponse(
        route_id=route_id,
        job_id=job_id,
        status="completed"
    )


@router.get("/{route_id}/status", response_model=RouteStatusResponse)
async def get_route_status(route_id: str):
    log(f"get_route_status called route_id={route_id}")
    route = ROUTES.get(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    progress = 1.0 if route["status"] == "completed" else 0.3

    return RouteStatusResponse(
        route_id=route_id,
        status=route["status"],
        progress=progress
    )


@router.get("/{route_id}/preview", response_model=RoutePreviewResponse)
async def get_route_preview(route_id: str):
    log(f"get_route_preview called route_id={route_id}")
    route = ROUTES.get(route_id)
    if not route or route["status"] != "completed":
        raise HTTPException(status_code=404, detail="Route not ready")
    geo_points = [LatLng(lat=pt[1], lng=pt[3]) if isinstance(pt, tuple) else pt for pt in route["polyline"]]

    return RoutePreviewResponse(
        route_id=route_id,
        confidence=route["confidence"],
        polyline={
            "geo": geo_points,
            "encoded": route.get("encoded_polyline")
        },
        polyline_image_space={
            "points": route.get("image_polyline", [])
        }
    )



@router.post("/{route_id}/refine", response_model=RefineRouteResponse)
async def refine_route(route_id: str, payload: RefineRouteRequest):
    log(f"refine_route called route_id={route_id}")
    if route_id not in ROUTES:
        raise HTTPException(status_code=404, detail="Route not found")

    # Placeholder: refinement comes later
    return RefineRouteResponse(status="refinement_not_enabled")
