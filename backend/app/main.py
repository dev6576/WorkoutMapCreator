from fastapi import FastAPI
from app.api.v1 import routes, export, health

app = FastAPI(
    title="Route From Image API",
    version="1.0.0"
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(routes.router, prefix="/api/v1/routes", tags=["routes"])
app.include_router(export.router, prefix="/api/v1/routes", tags=["export"])
