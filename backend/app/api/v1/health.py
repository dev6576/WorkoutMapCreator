from fastapi import APIRouter
from app.print_logging import log

router = APIRouter()


@router.get("/health")
def health_check():
    log("health_check called")
    return {"status": "ok"}
