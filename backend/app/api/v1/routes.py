from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.upload import UploadResponse
from app.schemas.process import ProcessRouteRequest, ProcessRouteResponse
from app.schemas.status import RouteStatusResponse
from app.schemas.route import RoutePreviewResponse
from app.schemas.refine import RefineRouteRequest, RefineRouteResponse

from app.core.storage import ROUTES, JOBS, create_route, create_job
from app.core.image_loader import save_image
from app.core.geo_utils import expand_bbox
from app.core.route_extractor import extract_image_space_polyline
from app.core.map_matching import match_to_map

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_route_image(file: UploadFile = File(...)):
    route_id = create_route()
    image_path = await save_image(file, route_id)

    ROUTES[route_id]["image_path"] = image_path

    return UploadResponse(route_id=route_id, status="uploaded")


@router.post("/{route_id}/process", response_model=ProcessRouteResponse)
async def process_route(route_id: str, payload: ProcessRouteRequest):
    if route_id not in ROUTES:
        raise HTTPException(status_code=404, detail="Route not found")

    job_id = create_job(route_id)

    search_scope = None
    if payload.search_scope:
        expanded = expand_bbox(
            payload.search_scope.bbox.model_dump(),
            payload.search_scope.padding_meters
        )
        search_scope = expanded

    ROUTES[route_id]["search_scope"] = search_scope
    ROUTES[route_id]["status"] = "processing"

    # --- Stub processing pipeline ---
    image_polyline = extract_image_space_polyline(ROUTES[route_id]["image_path"])
    geo_polyline = match_to_map(image_polyline, search_scope)

    ROUTES[route_id]["polyline"] = geo_polyline
    ROUTES[route_id]["confidence"] = 0.86
    ROUTES[route_id]["status"] = "completed"

    JOBS[job_id]["status"] = "completed"
    JOBS[job_id]["progress"] = 1.0

    return ProcessRouteResponse(
        route_id=route_id,
        job_id=job_id,
        status="completed"
    )


@router.get("/{route_id}/status", response_model=RouteStatusResponse)
async def get_route_status(route_id: str):
    if route_id not in ROUTES:
        raise HTTPException(status_code=404, detail="Route not found")

    return RouteStatusResponse(
        route_id=route_id,
        status=ROUTES[route_id]["status"],
        progress=1.0 if ROUTES[route_id]["status"] == "completed" else 0.5
    )


@router.get("/{route_id}/preview", response_model=RoutePreviewResponse)
async def get_route_preview(route_id: str):
    route = ROUTES.get(route_id)
    if not route or not route["polyline"]:
        raise HTTPException(status_code=404, detail="Route not ready")

    return RoutePreviewResponse(
        route_id=route_id,
        confidence=route["confidence"],
        polyline={
            "geo": route["polyline"],
            "encoded": None
        },
        polyline_image_space={
            "points": [[120, 450], [130, 460]]
        }
    )


@router.post("/{route_id}/refine", response_model=RefineRouteResponse)
async def refine_route(route_id: str, payload: RefineRouteRequest):
    if route_id not in ROUTES:
        raise HTTPException(status_code=404, detail="Route not found")

    # Stub: refinement logic will re-run map matching later
    return RefineRouteResponse(status="refinement_applied")
