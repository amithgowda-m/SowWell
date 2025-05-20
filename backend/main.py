# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import disease, crops, auth, weather





app = FastAPI(
    title="SowWell Smart Agriculture API",
    description="Backend for Smart Soil Monitoring & Scientific Farming Guidance Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes
app.include_router(disease.router, prefix="/api/disease", tags=["Disease Detection"])
app.include_router(crops.router, prefix="/api/crops", tags=["Crop Advisor"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather Info"])

# Root endpoint (optional)
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to SowWell Smart Agriculture API"}
