from fastapi import FastAPI
from app.api.v1 import routes, export, health
from fastapi.middleware.cors import CORSMiddleware
from app.print_logging import log

app = FastAPI(
    title="Route From Image API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log("FastAPI app instantiated")

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(routes.router, prefix="/api/v1/routes", tags=["routes"])
app.include_router(export.router, prefix="/api/v1/routes", tags=["export"])
