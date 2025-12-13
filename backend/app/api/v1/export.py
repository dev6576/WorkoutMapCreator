from fastapi import APIRouter, Query, HTTPException
from app.print_logging import log
from app.schemas.export import ExportRouteResponse
from app.core.storage import ROUTES

router = APIRouter()


@router.get("/{route_id}/export", response_model=ExportRouteResponse)
async def export_route(
    route_id: str,
    format: str = Query(..., pattern="^(gpx|google_maps|polyline)$")
):
    log(f"export_route called route_id={route_id} format={format}")
    route = ROUTES.get(route_id)
    if not route or not route["polyline"]:
        raise HTTPException(status_code=404, detail="Route not ready")

    if format == "google_maps":
        return ExportRouteResponse(
            type="google_maps",
            url="https://www.google.com/maps/dir/?api=1"
        )

    if format == "gpx":
        return ExportRouteResponse(
            type="gpx",
            download_url=f"/downloads/{route_id}.gpx"
        )

    return ExportRouteResponse(type="polyline")
