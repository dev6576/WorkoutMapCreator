npm install @react-google-maps/api axios
npm install --save-dev @types/react @types/react-dom
npm install --save-dev vite @vitejs/plugin-react
npm install react-leaflet-draw leaflet-draw



cd D:\GitHub\WorkoutMapCreator\backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Backend Folder Structure

The `backend/` directory contains the FastAPI-based server for processing route images and handling API requests.

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point, sets up CORS and includes routers
│   ├── print_logging.py        # Simple logging helper for debug prints with timestamps
│   ├── __pycache__/            # Python bytecode cache (ignored)
│   ├── ai/
│   │   ├── llm_client.py       # Client for interacting with Large Language Models (LLMs)
│   │   └── route_reasoner.py   # Logic for reasoning about routes using AI
│   ├── api/
│   │   └── v1/
│   │       ├── export.py       # API endpoints for exporting routes (e.g., GPX, Google Maps)
│   │       ├── health.py       # Health check endpoint for API status
│   │       ├── routes.py       # Main API routes for uploading, processing, and retrieving routes
│   │       └── __pycache__/    # Python bytecode cache (ignored)
│   ├── core/
│   │   ├── geo_utils.py        # Utilities for geographic calculations (e.g., bounding boxes)
│   │   ├── image_loader.py     # Functions to load and handle image files
│   │   ├── map_matching.py     # Core logic for matching extracted routes to real-world maps
│   │   ├── polyline_utils.py   # Utilities for encoding/decoding polylines
│   │   ├── route_extractor.py  # Extracts route data from images (placeholder/stub)
│   │   └── storage.py          # In-memory storage for routes, jobs, etc.
│   ├── cv/
│   │   ├── extractor.py        # Computer vision logic to extract route components from images
│   │   ├── models.py           # Data models for CV results (e.g., RouteComponent, CVExtractionResult)
│   │   ├── ocr.py              # Optical Character Recognition for text in images
│   │   └── utils.py            # Helper functions for CV operations (e.g., skeletonize, polyline length)
│   └── matching/
│       ├── anchors.py          # Calculates bonuses for anchor points in map matching
│       ├── marker_projection.py # Projects markers onto polylines
│       ├── matcher.py          # Main map matching logic using OSM and scoring
│       ├── models.py           # Data models for matching (e.g., MapMatchCandidate)
│       ├── osm_client.py       # Client for querying OpenStreetMap (OSM) data
│       ├── pixel_to_geo.py     # Converts pixel coordinates to geographic coordinates
│       ├── scoring.py          # Scoring functions for evaluating route matches
│       └── shape_similarity.py # Measures shape similarity between polylines
└── uploads/                    # Directory for storing uploaded image files
```

