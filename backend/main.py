# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import disease, crops, weather
# from routes.weather import weather_router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SowWell-API")

app = FastAPI(
    title="SowWell Smart Agriculture API",
    description="Backend for Smart Soil Monitoring & Scientific Farming Guidance Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Log every incoming request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Include routers
app.include_router(disease.router, prefix="/api/disease", tags=["Disease Detection"])
app.include_router(crops.router, prefix="/api/crops", tags=["Crop Advisor"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather Info"])

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to SowWell Smart Agriculture API"}