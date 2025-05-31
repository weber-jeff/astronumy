import sys
import os
from fastapi import FastAPI

# Add the project root directory to the Python path
# This allows imports like 'from api.endpoints import router'
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the router from your api.endpoints module
from api.endpoints import router as api_router # Assuming 'router' is the APIRouter instance in endpoints.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Numerology & Astrology AI API",
    description="API for generating numerology and astrology-based insights with AI integration.",
    version="1.0.0"
)

# CORS settings — adjust for frontend domain if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes
# Use the imported router, and you can add a prefix if all API routes should start with /api
app.include_router(api_router, prefix="/api")
