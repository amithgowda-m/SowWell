# backend/routes/weather.py

from fastapi import APIRouter, Query
import httpx
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/weather", tags=["Weather Info"])

# Replace with your actual Ambee API key
AMBEE_API_KEY = ""

@router.get("/forecast")
async def get_weather(place: str = Query(...)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.ambeedata.com/weather/by-place", 
            params={"place": place},
            headers={
                "x-api-key": AMBEE_API_KEY,
                "Content-Type": "application/json"
            }
        )

        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to fetch data from Ambee"}
            )

        # Extract useful data
        data = response.json()["data"]["currentCondition"][0]
        return {
            "temperature": data["temp_C"],
            "humidity": data["humidity"],
            "rainfall": data.get("precipMM", None),
            "description": data["weatherDesc"][0]["value"],
            "timestamp": data.get("observation_time", None)
        }